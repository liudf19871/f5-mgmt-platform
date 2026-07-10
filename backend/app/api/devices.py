from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceResponse
from app.services.f5_manager import discover_device, sync_device_config, F5Manager

router = APIRouter()

@router.get("/", response_model=list[DeviceResponse])
async def get_devices(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device))
    return result.scalars().all()

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(device: DeviceCreate, db: AsyncSession = Depends(get_db)):
    db_device = Device(
        name=device.name,
        type=device.type,
        ip_address=str(device.ip_address),
        port=device.port,
        username=device.username,
        password=device.password
    )
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device

@router.post("/{device_id}/discover")
async def discover_device_api(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    result = await discover_device(device)
    if result["success"]:
        if "version" in result:
            device.version = result["version"]
        device.status = "online"
        await db.commit()
    
    return result

@router.post("/{device_id}/sync")
async def sync_device_config_api(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return await sync_device_config(device)

@router.post("/{device_id}/test-connection")
async def test_connection_api(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    f5 = F5Manager(device)
    return await f5.test_connection()

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: int, device: DeviceCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    db_device = result.scalar_one_or_none()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db_device.name = device.name
    db_device.type = device.type
    db_device.ip_address = str(device.ip_address)
    db_device.port = device.port
    db_device.username = device.username
    db_device.password = device.password
    
    await db.commit()
    await db.refresh(db_device)
    return db_device

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    await db.delete(device)
    await db.commit()