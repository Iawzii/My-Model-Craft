from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from db.models import Model, User
from db.session import get_db
from schemas.model import ModelCreate, ModelOut

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=list[ModelOut])
def list_models(
    limit: int = Query(12, ge=1, le=48),
    author_id: Optional[UUID] = Query(None, alias="authorId"),
    db: Session = Depends(get_db),
):
    query = db.query(Model).order_by(Model.created_at.desc())
    if author_id:
        query = query.filter(Model.author_id == author_id)
    models = query.limit(limit).all()
    return models


@router.get("/{model_id}", response_model=ModelOut)
def get_model(model_id: UUID, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found.")
    return model


@router.post("", response_model=ModelOut, status_code=status.HTTP_201_CREATED)
def create_model(
    payload: ModelCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required.")
    if not payload.fileUrl:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fileUrl is required.")

    normalized_tags = [tag.strip() for tag in payload.tags if tag.strip()]

    model = Model(
        title=title,
        description=payload.description,
        category=(payload.category or None),
        tags=normalized_tags,
        file_url=payload.fileUrl,
        thumbnail_url=payload.thumbnailUrl,
        preview_urls=payload.previewUrls,
        author_id=current_user.id,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
