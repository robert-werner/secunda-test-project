from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 3", name="ck_activity_level_1_3"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id"), nullable=True)

    parent: Mapped["Activity | None"] = relationship(
        "Activity",
        remote_side=[id],
        back_populates="children"
    )

    children: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="parent"
    )

    level: Mapped[int] = mapped_column(nullable=False)

class OrganizationActivity(Base):
    __tablename__ = "organization_activities"

    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)
