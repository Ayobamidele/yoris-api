from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app import models, schemas
from app.utils.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.CommentResponse])
async def get_comments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Comment))
    return result.scalars().all()

@router.post("/", response_model=schemas.CommentResponse)
async def create_comment(comment: schemas.CommentCreate, db: AsyncSession = Depends(get_db)):
    post_result = await db.execute(select(models.Post).filter(models.Post.id == comment.postId))
    if not post_result.scalars().first():
        raise HTTPException(status_code=400, detail="postId does not exist")
        
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

@router.get("/{comment_id}", response_model=schemas.CommentResponse)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Comment).filter(models.Comment.id == comment_id))
    db_comment = result.scalars().first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment
