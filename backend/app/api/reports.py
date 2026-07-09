from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter()

@router.get("/traffic")
async def get_traffic_report(db: AsyncSession = Depends(get_db)):
    return {"message": "Traffic report endpoint"}

@router.get("/performance")
async def get_performance_report(db: AsyncSession = Depends(get_db)):
    return {"message": "Performance report endpoint"}

@router.get("/availability")
async def get_availability_report(db: AsyncSession = Depends(get_db)):
    return {"message": "Availability report endpoint"}