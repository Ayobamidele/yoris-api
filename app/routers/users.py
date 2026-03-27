from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app import models, schemas
from app.utils.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    return result.scalars().all()

@router.post("/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Initialize wallet
    wallet = models.Wallet(userId=db_user.id, balance=1000.0)
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)  # Bug fix: was missing - wallet.id could be None after commit
    return db_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/{user_id}/deliveries")
async def create_delivery(
    user_id: int,
    post_id: int = Body(..., embed=True),  # Bug fix: was a bare query param, now explicit body field
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    rider = result.scalars().first()
    if not rider:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify the post exists
    post_result = await db.execute(select(models.Post).filter(models.Post.id == post_id))
    if not post_result.scalars().first():
        raise HTTPException(status_code=404, detail="Post not found")

    delivery = models.DeliveryJob(riderId=rider.id, postId=post_id)
    rider.status = "BUSY"
    db.add(delivery)
    await db.commit()
    await db.refresh(delivery)

    return {"message": "Delivery created", "delivery_id": delivery.id, "rider_status": rider.status}
