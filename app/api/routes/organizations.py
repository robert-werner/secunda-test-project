from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, literal_column, or_
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.models.organization import Organization
from app.models.building import Building
from app.models.activity import Activity, OrganizationActivity
from app.schemas.organization import OrganizationRead, OrganizationList

router = APIRouter()


@router.get(
    "/{org_id}",
    response_model=OrganizationRead,
    summary="Получить организацию по ID",
    description="Возвращает полную карточку организации, включая телефоны, здание и все виды деятельности.",
    responses={404: {"description": "Организация не найдена"}}
)
async def get_organization(
    org_id: int,
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Organization)
        .where(Organization.id == org_id)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities)
        )
    )
    result = await db.execute(query)
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return org


@router.get(
    "",
    response_model=list[OrganizationList],
    summary="Поиск организаций",
    description=(
        "Поиск организаций по различным критериям: название, здание, вид деятельности. "
        "Поддерживает рекурсивный поиск по дереву деятельности (например, искать все 'Еда' -> найдутся и 'Мясные')."
    )
)
async def search_organizations(
    name: str | None = Query(None, description="Частичное совпадение названия (case-insensitive)"),
    building_id: int | None = Query(None, description="ID здания для фильтрации"),
    activity_id: int | None = Query(None, description="ID вида деятельности"),
    recursive: bool = Query(
        False,
        description="Если true, ищет также во всех дочерних категориях выбранной деятельности."
    ),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Organization)
        .options(selectinload(Organization.building))
        .join(Organization.building)
    )

    if name:
        query = query.where(Organization.name.ilike(f"%{name}%"))

    if building_id:
        query = query.where(Organization.building_id == building_id)

    if activity_id:
        if recursive:
            cte_query = (
                select(Activity.id)
                .where(Activity.id == activity_id)
                .cte(name="activity_tree", recursive=True)
            )

            recursive_part = (
                select(Activity.id)
                .join(cte_query, Activity.parent_id == cte_query.c.id)
            )

            cte = cte_query.union_all(recursive_part)

            query = (
                query
                .join(Organization.activities)
                .where(Activity.id.in_(select(cte.c.id)))
            )
        else:
            query = (
                query
                .join(Organization.activities)
                .where(Activity.id == activity_id)
            )

    result = await db.execute(query)
    return result.scalars().unique().all()


@router.get(
    "/geo/radius",
    response_model=list[OrganizationList],
    summary="Поиск организаций в радиусе",
    description="Находит все организации, здания которых находятся в пределах заданного радиуса (в метрах) от точки."
)
async def search_organizations_by_radius(
    lat: Annotated[float, Query(ge=-90, le=90, description="Широта центра поиска")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Долгота центра поиска")],
    radius_m: Annotated[float, Query(gt=0, description="Радиус поиска в метрах")],
    db: AsyncSession = Depends(get_db)
):
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

    query = (
        select(Organization)
        .join(Organization.building)
        .options(selectinload(Organization.building))
        .where(
            func.ST_DWithin(
                Building.location,
                func.Geography(point),
                radius_m
            )
        )
    )

    result = await db.execute(query)
    return result.scalars().all()


@router.get(
    "/geo/box",
    response_model=list[OrganizationList],
    summary="Поиск организаций в прямоугольной области",
    description="Находит организации внутри заданного прямоугольника координат (bounding box)."
)
async def search_organizations_by_box(
    min_lat: Annotated[float, Query(ge=-90, le=90, description="Минимальная широта (юг)")],
    min_lon: Annotated[float, Query(ge=-180, le=180, description="Минимальная долгота (запад)")],
    max_lat: Annotated[float, Query(ge=-90, le=90, description="Максимальная широта (север)")],
    max_lon: Annotated[float, Query(ge=-180, le=180, description="Максимальная долгота (восток)")],
    db: AsyncSession = Depends(get_db)
):
    bbox = func.ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)

    query = (
        select(Organization)
        .join(Organization.building)
        .options(selectinload(Organization.building))
        .where(
            func.ST_Intersects(
                func.ST_GeomFromWKB(Building.location),
                bbox
            )
        )
    )

    result = await db.execute(query)
    return result.scalars().all()
