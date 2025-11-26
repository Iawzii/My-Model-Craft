from fastapi import FastAPI

from core.config import settings
from db.session import Base, engine
from routers import auth

# Create database tables on startup. In production consider using migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(auth.router, prefix="/api")


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
