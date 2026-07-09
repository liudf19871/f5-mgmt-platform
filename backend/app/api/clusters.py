from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.cluster import Cluster, ClusterMember
from app.schemas.cluster import ClusterCreate, ClusterResponse, ClusterMemberCreate, ClusterMemberResponse

router = APIRouter()

@router.get("/", response_model=list[ClusterResponse])
async def get_clusters(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cluster))
    return result.scalars().all()

@router.post("/", response_model=ClusterResponse, status_code=status.HTTP_201_CREATED)
async def create_cluster(cluster: ClusterCreate, db: AsyncSession = Depends(get_db)):
    db_cluster = Cluster(name=cluster.name, type=cluster.type)
    db.add(db_cluster)
    await db.commit()
    await db.refresh(db_cluster)
    return db_cluster

@router.get("/{cluster_id}", response_model=ClusterResponse)
async def get_cluster(cluster_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cluster).where(Cluster.id == cluster_id))
    cluster = result.scalar_one_or_none()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return cluster

@router.post("/{cluster_id}/members", response_model=ClusterMemberResponse)
async def add_member(cluster_id: int, member: ClusterMemberCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cluster).where(Cluster.id == cluster_id))
    cluster = result.scalar_one_or_none()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    db_member = ClusterMember(
        cluster_id=cluster_id,
        device_id=member.device_id,
        role=member.role,
        priority=member.priority
    )
    db.add(db_member)
    await db.commit()
    await db.refresh(db_member)
    return db_member

@router.delete("/{cluster_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(cluster_id: int, member_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ClusterMember).where(
        ClusterMember.id == member_id,
        ClusterMember.cluster_id == cluster_id
    ))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    await db.delete(member)
    await db.commit()

@router.post("/{cluster_id}/failover")
async def failover(cluster_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cluster).where(Cluster.id == cluster_id))
    cluster = result.scalar_one_or_none()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    result = await db.execute(select(ClusterMember).where(ClusterMember.cluster_id == cluster_id))
    members = result.scalars().all()
    
    primary = next((m for m in members if m.role == "primary"), None)
    if primary:
        primary.status = "failed"
    
    secondary = next((m for m in members if m.role == "secondary"), None)
    if secondary:
        secondary.role = "primary"
        secondary.status = "active"
    
    await db.commit()
    return {"message": "Failover executed successfully"}