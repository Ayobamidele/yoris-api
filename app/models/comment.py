from sqlalchemy import Column, Integer, String, ForeignKey
from app.utils.database import Base

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    postId = Column(Integer, ForeignKey('posts.id'))
    name = Column(String)
    email = Column(String)
    body = Column(String)
