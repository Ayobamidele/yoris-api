from sqlalchemy import Column, Integer, String, DateTime, func
from app.utils.database import Base


class RequestLog(Base):
    """Logs every inbound HTTP request for audit/analytics."""
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, nullable=False)
    path = Column(String, nullable=False)
    status_code = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SystemStatus(Base):
    """Key-value store for system-wide status flags."""
    __tablename__ = "system_status"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
