import mimetypes
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status

from core.dependencies import get_current_user
from db.models import User

router = APIRouter(prefix="/upload", tags=["upload"])

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_ROOT = BASE_DIR / "uploads"
MODEL_DIR = UPLOAD_ROOT / "models"
THUMBNAIL_DIR = UPLOAD_ROOT / "thumbnails"
PREVIEW_DIR = UPLOAD_ROOT / "previews"

for directory in (MODEL_DIR, THUMBNAIL_DIR, PREVIEW_DIR):
    directory.mkdir(parents=True, exist_ok=True)


ALLOWED_MODEL_EXTENSIONS = {".glb"}
ALLOWED_IMAGE_MIME_PREFIX = "image/"


def _save_upload(file: UploadFile, directory: Path, allowed_extensions: set[str] | None = None) -> str:
    suffix = (Path(file.filename or "").suffix or "").lower()
    if allowed_extensions is not None and suffix not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {suffix or 'unknown'}",
        )

    if not suffix:
        guessed = mimetypes.guess_extension(file.content_type or "")
        if guessed:
            suffix = guessed
        else:
            suffix = ".dat"

    filename = f"{uuid.uuid4().hex}{suffix}"
    destination = directory / filename

    try:
        contents = file.file.read()
        destination.write_bytes(contents)
    except Exception as exc:  # pragma: no cover - filesystem issues
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded file.",
        ) from exc
    finally:
        file.file.close()

    return destination.relative_to(UPLOAD_ROOT).as_posix()


def _build_url(request: Request, relative_path: str) -> str:
    return str(request.url_for("uploads", path=relative_path.replace("\\", "/")))


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_model_file(
    request: Request,
    file: UploadFile = File(...),
    _: User = Depends(get_current_user),
):
    """Handle primary .glb model uploads."""
    relative_path = _save_upload(file, MODEL_DIR, ALLOWED_MODEL_EXTENSIONS)
    return {"url": _build_url(request, relative_path), "path": relative_path}


@router.post("/thumbnail", status_code=status.HTTP_201_CREATED)
async def upload_thumbnail(
    request: Request,
    file: UploadFile = File(...),
    _: User = Depends(get_current_user),
):
    if not (file.content_type or "").startswith(ALLOWED_IMAGE_MIME_PREFIX):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed for thumbnails.",
        )
    relative_path = _save_upload(file, THUMBNAIL_DIR)
    return {"url": _build_url(request, relative_path), "path": relative_path}


@router.post("/previews", status_code=status.HTTP_201_CREATED)
async def upload_previews(
    request: Request,
    files: List[UploadFile] = File(...),
    _: User = Depends(get_current_user),
):
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No preview files provided.")

    urls = []
    paths = []
    for upload in files:
        if not (upload.content_type or "").startswith(ALLOWED_IMAGE_MIME_PREFIX):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Preview files must be images.",
            )
        relative_path = _save_upload(upload, PREVIEW_DIR)
        urls.append(_build_url(request, relative_path))
        paths.append(relative_path)

    return {"urls": urls, "paths": paths}
