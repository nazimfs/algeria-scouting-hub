import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base


class Competition(Base):
    __tablename__ = "competitions"

    competition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    country_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.countries.country_id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(50))
    competition_type: Mapped[str] = mapped_column(String(50), nullable=False)
    level: Mapped[str | None] = mapped_column(String(50))

    country = relationship("Country")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )