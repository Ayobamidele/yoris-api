from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app import models, schemas
from app.utils.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Post))
    return result.scalars().all()

@router.post("/", response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: AsyncSession = Depends(get_db)):
    # Bug fix: removed unused `request: Request` parameter
    user_result = await db.execute(select(models.User).filter(models.User.id == post.userId))
    if not user_result.scalars().first():
        raise HTTPException(status_code=400, detail="userId does not exist")

    inv_result = await db.execute(select(models.Inventory).limit(1))
    inventory = inv_result.scalars().first()
    if not inventory:
        inventory = models.Inventory(available=100)
        db.add(inventory)
        await db.commit()
        await db.refresh(inventory)

    if inventory.available <= 0:
        raise HTTPException(status_code=400, detail="Inventory empty")

    inventory.available -= 1
    db.add(inventory)  # Bug fix: explicitly mark inventory as dirty so the decrement is persisted

    db_post = models.Post(**post.dict())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Post).filter(models.Post.id == post_id))
    db_post = result.scalars().first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
