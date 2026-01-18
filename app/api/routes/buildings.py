from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.models.building import Building
from app.schemas.building import BuildingRead

router = APIRouter()

@router.get(
    "",
    response_model=list[BuildingRead],
    summary="Список всех зданий",
    description="Возвращает полный список зданий с их адресами и географическими координатами (lat/lon).",
)
async def get_buildings(db: AsyncSession = Depends(get_db)):
    """
    Получить все здания из базы данных.
    """
    result = await db.execute(select(Building))
    return result.scalars().all()
