from pydantic import BaseModel

class CommentBase(BaseModel):
    name: str
    email: str
    body: str
class CommentCreate(CommentBase):
    postId: int
class CommentResponse(CommentBase):
    id: int
    postId: int
    class Config:
        from_attributes = True
