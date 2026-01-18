from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.building import Building
    from app.models.activity import Activity


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    # One-to-Many: Organization -> Building
    building: Mapped["Building"] = relationship(backref="organizations")

    # One-to-Many: Organization -> Phones
    phones: Mapped[list["OrganizationPhone"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    # Many-to-Many: Organization <-> Activities
    # Используем строковое имя таблицы "organization_activities", определенной в activity.py
    activities: Mapped[list["Activity"]] = relationship(
        secondary="organization_activities",
        backref="organizations"
    )


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"

    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)

    organization: Mapped["Organization"] = relationship(back_populates="phones")
