import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base
from app.database.models.mixins import TimestampMixin, UUIDMixin


class PlayerNationality(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "player_nationalities"

    player_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.players.player_id"),
        nullable=False,
    )

    nationality_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.nationalities.nationality_id"),
        nullable=False,
    )

    acquisition_type: Mapped[str | None] = mapped_column(String(50))
    confidence_level: Mapped[str | None] = mapped_column(String(30))

    player = relationship("Player")
    nationality = relationship("Nationality")