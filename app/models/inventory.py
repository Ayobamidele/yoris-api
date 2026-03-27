from sqlalchemy import Column, Integer
from app.utils.database import Base

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, index=True)
    available = Column(Integer, default=100)
