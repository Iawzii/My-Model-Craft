import mimetypes
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from core.security import hash_password, verify_password
from db.models import User
from db.session import get_db
from schemas.auth import ChangePasswordRequest, MessageResponse
from schemas.user import (
    AvatarUpdate,
    AvatarUploadResponse,
    BioUpdate,
    EmailUpdate,
    UserOut,
    UserProfileUpdate,
    UsernameUpdate,
)

BASE_DIR = Path(__file__).resolve().parent.parent
AVATAR_DIR = BASE_DIR / "uploads" / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/settings/user", tags=["user-settings"])


@router.patch("", response_model=UserOut)
def update_user_settings(
    payload: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Legacy endpoint that allows updating multiple fields at once."""
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No updates provided.")

    if "username" in update_data:
        return update_username(UsernameUpdate(username=update_data["username"]), current_user, db)
    if "email" in update_data:
        return update_email(EmailUpdate(email=update_data["email"]), current_user, db)
    if "avatarUrl" in update_data:
        return update_avatar(AvatarUpdate(avatarUrl=update_data["avatarUrl"]), current_user, db)
    if "bio" in update_data:
        return update_bio(BioUpdate(bio=update_data["bio"]), current_user, db)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported update field.")


@router.patch("/username", response_model=UserOut)
def update_username(
    payload: UsernameUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_username = payload.username.strip()
    if not new_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username cannot be empty.",
        )

    username_exists = (
        db.query(User)
        .filter(User.username == new_username, User.id != current_user.id)
        .first()
    )
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken.",
        )

    current_user.username = new_username
    db.commit()
    db.refresh(current_user)
    return current_user


@router.patch("/email", response_model=UserOut)
def update_email(
    payload: EmailUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_email = payload.email
    email_exists = (
        db.query(User)
        .filter(User.email == new_email, User.id != current_user.id)
        .first()
    )
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    current_user.email = new_email
    db.commit()
    db.refresh(current_user)
    return current_user


@router.patch("/avatar", response_model=UserOut)
def update_avatar(
    payload: AvatarUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    avatar_url = payload.avatarUrl or None
    if avatar_url and len(avatar_url) > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar URL is too long.",
        )

    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user


@router.patch("/bio", response_model=UserOut)
def update_bio(
    payload: BioUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.bio = payload.bio
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/avatar/upload", response_model=AvatarUploadResponse)
async def upload_avatar_file(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    content_type = file.content_type or ""
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are supported.",
        )

    extension = mimetypes.guess_extension(content_type) or os.path.splitext(file.filename or "")[1]
    if not extension:
        extension = ".png"

    filename = f"{uuid.uuid4().hex}{extension}"
    destination = AVATAR_DIR / filename

    try:
        contents = await file.read()
        destination.write_bytes(contents)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save avatar.",
        ) from exc

    relative_path = f"avatars/{filename}"
    avatar_url = request.url_for("uploads", path=relative_path)
    return AvatarUploadResponse(url=str(avatar_url))


@router.post("/password", response_model=MessageResponse)
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.currentPassword, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )
    if payload.currentPassword == payload.newPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from the current password.",
        )

    current_user.password_hash = hash_password(payload.newPassword)
    db.commit()

    return MessageResponse(detail="Password updated successfully.")
