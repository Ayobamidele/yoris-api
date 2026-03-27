from pydantic import BaseModel

class WalletResponse(BaseModel):
    id: int
    userId: int
    balance: float
    class Config:
        from_attributes = True
class TransferRequest(BaseModel):
    senderId: int
    receiverId: int
    amount: float
