from sqlalchemy import Column, Integer, String, ForeignKey
from app.utils.database import Base

class DeliveryJob(Base):
    __tablename__ = 'delivery_jobs'
    id = Column(Integer, primary_key=True, index=True)
    riderId = Column(Integer, ForeignKey('users.id'))
    postId = Column(Integer, ForeignKey('posts.id'))
    state = Column(String, default='PENDING')
