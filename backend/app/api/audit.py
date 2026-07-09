from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter()

@router.get("/logs")
async def get_audit_logs(db: AsyncSession = Depends(get_db)):
    return {"message": "Audit logs endpoint"}