from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models, schemas
from app.utils.database import get_db

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.WalletResponse)
async def get_wallet(user_id: int, db: AsyncSession = Depends(get_db)):
    """Return the wallet belonging to the given user."""
    result = await db.execute(
        select(models.Wallet).filter(models.Wallet.userId == user_id)
    )
    wallet = result.scalars().first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.post("/transfer", response_model=dict)
async def transfer_funds(
    transfer: schemas.TransferRequest, db: AsyncSession = Depends(get_db)
):
    """Transfer funds between two wallets."""
    if transfer.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    sender_result = await db.execute(
        select(models.Wallet).filter(models.Wallet.userId == transfer.senderId)
    )
    sender_wallet = sender_result.scalars().first()
    if not sender_wallet:
        raise HTTPException(status_code=404, detail="Sender wallet not found")

    receiver_result = await db.execute(
        select(models.Wallet).filter(models.Wallet.userId == transfer.receiverId)
    )
    receiver_wallet = receiver_result.scalars().first()
    if not receiver_wallet:
        raise HTTPException(status_code=404, detail="Receiver wallet not found")

    if sender_wallet.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    sender_wallet.balance -= transfer.amount
    receiver_wallet.balance += transfer.amount

    await db.commit()
    await db.refresh(sender_wallet)
    await db.refresh(receiver_wallet)

    return {
        "message": "Transfer successful",
        "sender_balance": sender_wallet.balance,
        "receiver_balance": receiver_wallet.balance,
    }
