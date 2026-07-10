from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.device import Device
from app.services.f5_manager import F5Manager

router = APIRouter()


@router.get("/devices")
async def get_device_status(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device))
    devices = result.scalars().all()
    
    status_list = []
    for device in devices:
        f5 = F5Manager(device)
        status = await f5.get_device_status()
        status_list.append({
            "device_id": device.id,
            "name": device.name,
            "ip_address": device.ip_address,
            "status": "online" if status.get("online") else "offline",
            "version": status.get("version", device.version),
            "hostname": status.get("hostname", ""),
            "cpu": status.get("cpu", {}),
            "memory": status.get("memory", {})
        })
    
    return status_list


@router.get("/metrics/{device_id}")
async def get_device_metrics(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    f5 = F5Manager(device)
    return await f5.get_device_status()


@router.get("/alerts")
async def get_alerts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device))
    devices = result.scalars().all()
    
    alerts = []
    for device in devices:
        f5 = F5Manager(device)
        status = await f5.get_device_status()
        if not status.get("online"):
            alerts.append({
                "device_id": device.id,
                "device_name": device.name,
                "type": "device_offline",
                "severity": "critical",
                "message": f"设备 {device.name} ({device.ip_address}) 离线",
                "timestamp": "now"
            })
    
    return alerts


@router.get("/traffic/{device_id}")
async def get_device_traffic(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    f5 = F5Manager(device)
    return await f5.get_traffic_stats()