from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api.deps import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityRead

router = APIRouter()


@router.get(
    "",
    response_model=list[ActivityRead],
    summary="Справочник видов деятельности",
    description=(
        "Возвращает дерево видов деятельности. "
        "Можно фильтровать по уровню вложенности. "
        "Структура возвращается рекурсивно (родитель -> дети)."
    )
)
async def get_activities(
    level: int | None = Query(
        None,
        description="Фильтр по уровню вложенности (1 - корни, 2 - подкатегории, 3 - виды).",
        ge=1, le=3
    ),
    db: AsyncSession = Depends(get_db)
):

    query = select(Activity).options(
        selectinload(Activity.children)
        .selectinload(Activity.children)
        .selectinload(Activity.children)
    )

    if level:
        query = query.where(Activity.level == level)

    result = await db.execute(query)
    return result.scalars().unique().all()
