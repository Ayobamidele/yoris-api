from pydantic import BaseModel, Field

class PostBase(BaseModel):
    userId: int
    title: str
    body: str
class PostCreate(PostBase):
    amount: float = Field(..., description='Cost')
class PostResponse(PostBase):
    id: int
    amount: float
    class Config:
        from_attributes = True
