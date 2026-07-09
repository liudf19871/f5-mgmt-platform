from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter()

@router.get("/")
async def query_logs(db: AsyncSession = Depends(get_db)):
    return {"message": "Query logs endpoint"}

@router.get("/analysis")
async def analyze_logs(db: AsyncSession = Depends(get_db)):
    return {"message": "Analyze logs endpoint"}