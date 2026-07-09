from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter()

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    return {"message": "Users endpoint"}

@router.post("/")
async def create_user(db: AsyncSession = Depends(get_db)):
    return {"message": "Create user endpoint"}