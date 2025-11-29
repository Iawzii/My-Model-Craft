from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from schemas.user import UserCreate, UserOut


class SendCodeRequest(BaseModel):
    email: EmailStr


class SendCodeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    email: EmailStr
    code: str
    expiresAt: datetime


class RegisterRequest(UserCreate):
    pass


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str
    newPassword: str


class MessageResponse(BaseModel):
    detail: str
