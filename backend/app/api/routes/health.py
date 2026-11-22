from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.api.deps import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db:AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT version()"))
    version = result.scalar_one()

    return {
        "status":"healthy",
        "database":"connected",
        "postgres_version":version
        }