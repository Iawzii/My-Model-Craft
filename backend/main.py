from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import settings
from db.session import Base, engine
from routers import (
    auth,
    models as models_router,
    settings as settings_router,
    upload,
    users as users_router,
)

# Create database tables on startup. In production consider using migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_dir = Path(__file__).resolve().parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

app.include_router(auth.router, prefix="/api")
app.include_router(settings_router.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(models_router.router, prefix="/api")
app.include_router(users_router.router, prefix="/api")


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
