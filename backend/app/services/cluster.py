from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cluster import Cluster, ClusterMember
from app.schemas.cluster import ClusterCreate, ClusterMemberCreate

async def get_clusters(db: AsyncSession):
    result = await db.execute(select(Cluster))
    return result.scalars().all()

async def get_cluster_by_id(db: AsyncSession, cluster_id: int):
    result = await db.execute(select(Cluster).where(Cluster.id == cluster_id))
    return result.scalar_one_or_none()

async def create_cluster(db: AsyncSession, cluster: ClusterCreate):
    db_cluster = Cluster(name=cluster.name, type=cluster.type)
    db.add(db_cluster)
    await db.commit()
    await db.refresh(db_cluster)
    return db_cluster

async def add_member(db: AsyncSession, cluster_id: int, member: ClusterMemberCreate):
    result = await db.execute(select(Cluster).where(Cluster.id == cluster_id))
    cluster = result.scalar_one_or_none()
    if not cluster:
        return None
    
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

async def remove_member(db: AsyncSession, cluster_id: int, member_id: int):
    result = await db.execute(select(ClusterMember).where(
        ClusterMember.id == member_id,
        ClusterMember.cluster_id == cluster_id
    ))
    member = result.scalar_one_or_none()
    if not member:
        return False
    
    await db.delete(member)
    await db.commit()
    return True

async def failover(db: AsyncSession, cluster_id: int):
    result = await db.execute(select(Cluster).where(Cluster.id == cluster_id))
    cluster = result.scalar_one_or_none()
    if not cluster:
        return False
    
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
    return True