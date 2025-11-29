import secrets
import smtplib
import string
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.config import settings
from core.security import create_access_token, hash_password, verify_password
from db.models import User, VerificationCode
from db.session import get_db
from schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    MessageResponse,
    RegisterRequest,
    ResetPasswordRequest,
    SendCodeRequest,
    SendCodeResponse,
)
from schemas.user import UserOut


router = APIRouter(prefix="/auth", tags=["auth"])


def _generate_code(length: int) -> str:
    alphabet = string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _send_email(to_email: str, subject: str, content: str) -> None:
    """Send an email via QQ SMTP."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_user
    msg["To"] = to_email
    msg.set_content(content)

    try:
        server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port)
        try:
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
        finally:
            try:
                server.quit()
            except Exception:
                # Ignore errors during quit, as the message might have been sent successfully
                pass
    except Exception as exc:
        import logging
        logging.exception("Failed to send email")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送邮件失败，请稍后重试。错误信息: {exc}",
        ) from exc


@router.post("/send-code", response_model=SendCodeResponse)
def send_verification_code(payload: SendCodeRequest, db: Session = Depends(get_db)):
    # Avoid sending verification codes for emails that already belong to a user.
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    code = _generate_code(settings.verification_code_length)
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.verification_code_exp_minutes
    )
    
    body = (
        f"验证码: {code}\n"
        f"请在{settings.verification_code_exp_minutes}分钟内完成注册。"
    )
    _send_email(payload.email, "您的验证码", body)
    
    # 邮件发送成功后再创建数据库记录
    try:
        print(f"Attempting to insert verification code for {payload.email}")
        record = VerificationCode(email=payload.email, code=code, expires_at=expires_at)
        db.add(record)
        db.commit()
        db.refresh(record)
        print(f"Successfully inserted verification code with ID: {record.id}")
    except Exception as exc:
        print(f"Database insertion failed: {exc}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {exc}",
        ) from exc

    return SendCodeResponse(email=payload.email, code=code, expiresAt=expires_at)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email exists.")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken."
        )

    verification = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.email == payload.email,
            VerificationCode.code == payload.code,
            VerificationCode.is_used.is_(False),
        )
        .order_by(VerificationCode.created_at.desc())
        .first()
    )
    now = datetime.now(timezone.utc)
    if not verification or verification.expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code.",
        )

    hashed_password = hash_password(payload.password)
    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hashed_password,
        avatar_url=payload.avatarUrl,
        bio=payload.bio,
    )
    db.add(user)
    verification.is_used = True
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password."
        )

    token = create_access_token({"sub": str(user.id)})
    return LoginResponse(access_token=token, user=user)


@router.post("/forgot", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email was not found.",
        )

    code = _generate_code(settings.verification_code_length)
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.verification_code_exp_minutes
    )
    body = (
        f"验证码: {code}\n"
        f"请在{settings.verification_code_exp_minutes}分钟内完成密码重置。"
    )
    _send_email(payload.email, "密码重置验证码", body)

    record = VerificationCode(email=payload.email, code=code, expires_at=expires_at)
    db.add(record)
    db.commit()

    return MessageResponse(detail="Password reset code sent to your email.")


@router.post("/reset", response_model=MessageResponse)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email was not found.",
        )

    verification = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.email == payload.email,
            VerificationCode.code == payload.code,
            VerificationCode.is_used.is_(False),
        )
        .order_by(VerificationCode.created_at.desc())
        .first()
    )

    now = datetime.now(timezone.utc)
    if not verification or verification.expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code.",
        )

    user.password_hash = hash_password(payload.newPassword)
    verification.is_used = True
    db.commit()

    return MessageResponse(detail="Password reset successfully.")


