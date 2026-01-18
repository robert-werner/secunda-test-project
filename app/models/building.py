from sqlalchemy import String, func, cast
from sqlalchemy.orm import Mapped, mapped_column, column_property
from geoalchemy2 import Geography, Geometry
from app.models.base import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String, nullable=False)

    location: Mapped[object] = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=False)

    lat: Mapped[float] = column_property(
        func.ST_Y(cast(location, Geometry))
    )

    lon: Mapped[float] = column_property(
        func.ST_X(cast(location, Geometry))
    )
