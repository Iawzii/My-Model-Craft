from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from core.dependencies import get_current_user, get_optional_current_user
from db.models import Model, User
from db.session import get_db
from schemas.user import UserProfileResponse, UserSummary

router = APIRouter(prefix="/users", tags=["users"])


def _get_user_or_404(user_id: UUID, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


def _build_profile_response(
    target_user: User,
    db: Session,
    viewer: User | None,
) -> UserProfileResponse:
    follower_ids = list(target_user.followers or [])
    following_ids = list(target_user.following or [])
    model_count = (
        db.query(func.count(Model.id))
        .filter(Model.author_id == target_user.id)
        .scalar()
        or 0
    )

    is_self = viewer.id == target_user.id if viewer else False
    is_following = bool(viewer and not is_self and viewer.id in follower_ids)

    return UserProfileResponse(
        id=target_user.id,
        username=target_user.username,
        email=target_user.email,
        avatarUrl=target_user.avatar_url,
        bio=target_user.bio,
        followers=follower_ids,
        following=following_ids,
        createdAt=target_user.created_at,
        followersCount=len(follower_ids),
        followingCount=len(following_ids),
        modelCount=int(model_count),
        isSelf=is_self,
        isFollowing=is_following,
    )


@router.get("/me", response_model=UserProfileResponse)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _build_profile_response(current_user, db, current_user)


@router.get("/lookup", response_model=list[UserSummary])
def lookup_users(
    ids: list[str] | None = Query(default=None, description="User IDs to lookup"),
    db: Session = Depends(get_db),
):
    if not ids:
        return []

    parsed_ids: list[UUID] = []
    for raw in ids:
        parts = [part.strip() for part in raw.split(",")]
        for part in parts:
            if not part:
                continue
            try:
                parsed_ids.append(UUID(part))
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid user id: {part}",
                ) from exc

    if not parsed_ids:
        return []

    users = (
        db.query(User)
        .filter(User.id.in_(parsed_ids))
        .all()
    )
    user_map = {user.id: user for user in users}
    ordered_users: list[User] = []
    for user_id in parsed_ids:
        user = user_map.get(user_id)
        if user:
            ordered_users.append(user)
    return ordered_users


@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user_profile(
    user_id: UUID,
    db: Session = Depends(get_db),
    viewer: User | None = Depends(get_optional_current_user),
):
    user = _get_user_or_404(user_id, db)
    return _build_profile_response(user, db, viewer)


@router.post("/{user_id}/follow", response_model=UserProfileResponse)
def follow_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target_user = _get_user_or_404(user_id, db)
    if target_user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself."
        )

    follower_set = set(target_user.followers or [])
    if current_user.id not in follower_set:
        follower_set.add(current_user.id)
        target_user.followers = list(follower_set)

    following_set = set(current_user.following or [])
    if target_user.id not in following_set:
        following_set.add(target_user.id)
        current_user.following = list(following_set)

    db.commit()
    db.refresh(target_user)
    db.refresh(current_user)

    return _build_profile_response(target_user, db, current_user)


@router.delete("/{user_id}/follow", response_model=UserProfileResponse)
def unfollow_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target_user = _get_user_or_404(user_id, db)
    if target_user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot unfollow yourself."
        )

    follower_set = set(target_user.followers or [])
    if current_user.id in follower_set:
        follower_set.remove(current_user.id)
        target_user.followers = list(follower_set)

    following_set = set(current_user.following or [])
    if target_user.id in following_set:
        following_set.remove(target_user.id)
        current_user.following = list(following_set)

    db.commit()
    db.refresh(target_user)
    db.refresh(current_user)

    return _build_profile_response(target_user, db, current_user)
