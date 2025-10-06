from __future__ import annotations
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import models, schemas
from .routers import auth as auth_router, posts as posts_router
from .dependencies import get_current_user, get_db
from .config import settings
from .database import engine
from .models import Base

app = FastAPI(title="Minimal FastAPI + PostgreSQL + JWT")

app.include_router(auth_router.router)
app.include_router(posts_router.router)

@app.get("/me", response_model=schemas.MeOut)
def me(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    posts = (
        db.query(models.Post)
        .filter(models.Post.owner_id == user.id)
        .order_by(models.Post.created_at.desc())
        .all()
    )
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at,
        },
        "posts": [
            {
                "id": p.id,
                "title": p.title,
                "content": p.content,
                "created_at": p.created_at,
                "owner_id": p.owner_id,
            }
            for p in posts
        ],
    }

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.on_event("startup")
def ensure_schema_in_debug():
    if settings.app_debug:
        Base.metadata.create_all(bind=engine)
