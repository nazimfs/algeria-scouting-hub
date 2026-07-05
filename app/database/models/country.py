import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class Country(Base):
    __tablename__ = "countries"

    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    iso2_code: Mapped[str] = mapped_column(String(2), unique=True, nullable=False)

    iso3_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)

    fifa_code: Mapped[str | None] = mapped_column(String(3))

    official_name: Mapped[str] = mapped_column(String(100), nullable=False)

    short_name: Mapped[str] = mapped_column(String(60), nullable=False)

    continent: Mapped[str] = mapped_column(String(30), nullable=False)

    is_fifa_member: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

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