from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatarUrl: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("avatarUrl", "avatar_url"),
        serialization_alias="avatarUrl",
    )
    bio: Optional[str] = None


class UserCreate(UserBase):
    password: str
    code: str


class UserProfileUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatarUrl: Optional[str] = None
    bio: Optional[str] = None


class UsernameUpdate(BaseModel):
    username: str


class EmailUpdate(BaseModel):
    email: EmailStr


class AvatarUpdate(BaseModel):
    avatarUrl: Optional[str] = None


class BioUpdate(BaseModel):
    bio: Optional[str] = None


class AvatarUploadResponse(BaseModel):
    url: str


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID = Field(
        validation_alias=AliasChoices("id", "_id"),
        serialization_alias="id",
    )
    followers: list[UUID] = Field(default_factory=list)
    following: list[UUID] = Field(default_factory=list)
    createdAt: datetime = Field(alias="created_at")


class UserProfileResponse(UserOut):
    followersCount: int
    followingCount: int
    modelCount: int
    isSelf: bool = False
    isFollowing: bool = False
