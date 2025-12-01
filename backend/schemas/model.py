from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class AuthorSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    username: str
    avatarUrl: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("avatarUrl", "avatar_url"),
        serialization_alias="avatarUrl",
    )
    bio: Optional[str] = None


class ModelBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    fileUrl: str = Field(
        validation_alias=AliasChoices("fileUrl", "file_url"),
        serialization_alias="fileUrl",
    )
    thumbnailUrl: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("thumbnailUrl", "thumbnail_url"),
        serialization_alias="thumbnailUrl",
    )
    previewUrls: List[str] = Field(
        default_factory=list,
        validation_alias=AliasChoices("previewUrls", "preview_urls"),
        serialization_alias="previewUrls",
    )


class ModelCreate(ModelBase):
    pass


class ModelOut(ModelBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    authorId: UUID = Field(
        validation_alias=AliasChoices("authorId", "author_id"),
        serialization_alias="authorId",
    )
    authorName: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("authorName", "author_name"),
        serialization_alias="authorName",
    )
    author: Optional[AuthorSummary] = None
    likeCount: int = Field(
        validation_alias=AliasChoices("likeCount", "like_count"),
        serialization_alias="likeCount",
        default=0,
    )
    collectCount: int = Field(
        validation_alias=AliasChoices("collectCount", "collect_count"),
        serialization_alias="collectCount",
        default=0,
    )
    createdAt: datetime = Field(alias="created_at")
