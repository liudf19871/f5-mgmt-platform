from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
from app.core.database import Base

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum("bigip", "dns"), nullable=False)
    ip_address = Column(String(45), unique=True, nullable=False)
    port = Column(Integer, default=443)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    version = Column(String(20))
    status = Column(Enum("online", "offline", "healthy", "unhealthy"), default="offline")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)