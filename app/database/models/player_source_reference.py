import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base


class PlayerSourceReference(Base):
    __tablename__ = "player_source_references"

    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "source_name",
            name="uq_player_source_reference",
        ),
    )

    reference_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    player_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.players.player_id"),
        nullable=False,
    )

    source_name: Mapped[str] = mapped_column(String(100), nullable=False)

    source_player_id: Mapped[str | None] = mapped_column(String(100))

    source_url: Mapped[str] = mapped_column(Text, nullable=False)

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

    player = relationship("Player")