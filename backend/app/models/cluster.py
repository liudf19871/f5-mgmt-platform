from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Cluster(Base):
    __tablename__ = "clusters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum("active-standby", "n-plus-m"), nullable=False)
    status = Column(Enum("healthy", "warning", "critical"), default="healthy")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    members = relationship("ClusterMember", back_populates="cluster")

class ClusterMember(Base):
    __tablename__ = "cluster_members"
    
    id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    role = Column(Enum("primary", "secondary"), nullable=False)
    priority = Column(Integer, default=100)
    status = Column(Enum("active", "standby", "failed"), default="standby")
    
    cluster = relationship("Cluster", back_populates="members")