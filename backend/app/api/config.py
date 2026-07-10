from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.device import Device
from app.services.f5_manager import F5Manager

router = APIRouter()


@router.get("/virtual-servers/{device_id}")
async def get_virtual_servers(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    f5 = F5Manager(device)
    return await f5.get_virtual_servers()


@router.get("/pools/{device_id}")
async def get_pools(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    f5 = F5Manager(device)
    return await f5.get_pools()


@router.get("/nodes/{device_id}")
async def get_nodes(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    f5 = F5Manager(device)
    return await f5.get_nodes()


@router.get("/certificates/{device_id}")
async def get_certificates(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    f5 = F5Manager(device)
    return await f5.get_certificates()


@router.get("/full-config/{device_id}")
async def get_full_config(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    f5 = F5Manager(device)
    return {
        "virtual_servers": await f5.get_virtual_servers(),
        "pools": await f5.get_pools(),
        "nodes": await f5.get_nodes(),
        "certificates": await f5.get_certificates()
    }