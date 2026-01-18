from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api.deps import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityRead

router = APIRouter()


@router.get("", response_model=list[ActivityRead])
async def get_activities(
        level: int | None = None,
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
