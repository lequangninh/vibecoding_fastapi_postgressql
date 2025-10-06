from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=schemas.PostOut, status_code=201)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    post = models.Post(title=payload.title, content=payload.content, owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return schemas.PostOut(
        id=post.id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        owner_id=post.owner_id,
    )

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    post = db.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden: not the post owner")
    db.delete(post)
    db.commit()
    return None
