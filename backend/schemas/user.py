from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatarUrl: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    password: str
    code: str


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID = Field(alias="_id")
    followers: list[UUID] = Field(default_factory=list)
    following: list[UUID] = Field(default_factory=list)
    createdAt: datetime = Field(alias="created_at")
