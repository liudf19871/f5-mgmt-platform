from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.device import Device
from app.schemas.device import DeviceCreate

async def get_devices(db: AsyncSession):
    result = await db.execute(select(Device))
    return result.scalars().all()

async def get_device_by_id(db: AsyncSession, device_id: int):
    result = await db.execute(select(Device).where(Device.id == device_id))
    return result.scalar_one_or_none()

async def get_device_by_ip(db: AsyncSession, ip_address: str):
    result = await db.execute(select(Device).where(Device.ip_address == ip_address))
    return result.scalar_one_or_none()

async def create_device(db: AsyncSession, device: DeviceCreate):
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

async def update_device(db: AsyncSession, device_id: int, device: DeviceCreate):
    result = await db.execute(select(Device).where(Device.id == device_id))
    db_device = result.scalar_one_or_none()
    if not db_device:
        return None
    
    db_device.name = device.name
    db_device.type = device.type
    db_device.ip_address = str(device.ip_address)
    db_device.port = device.port
    db_device.username = device.username
    db_device.password = device.password
    
    await db.commit()
    await db.refresh(db_device)
    return db_device

async def delete_device(db: AsyncSession, device_id: int):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        return False
    
    await db.delete(device)
    await db.commit()
    return True