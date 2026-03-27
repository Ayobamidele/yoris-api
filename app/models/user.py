from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.utils.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    status = Column(String, default='IDLE')
    posts = relationship('Post', back_populates='user')
    wallet = relationship('Wallet', back_populates='user', uselist=False)
