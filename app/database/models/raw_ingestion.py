import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base
from app.database.models.mixins import TimestampMixin, UUIDMixin


class RawIngestion(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "raw_ingestions"

    data_source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.data_sources.id"),
        nullable=False,
    )

    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)

    source_entity_id: Mapped[str | None] = mapped_column(String(150))

    payload: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    data_source = relationship("DataSource")