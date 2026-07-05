import uuid
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base
from app.database.models.mixins import TimestampMixin, UUIDMixin


class PlayerClub(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "player_clubs"

    player_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.players.player_id"),
        nullable=False,
    )

    club_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.clubs.club_id"),
        nullable=False,
    )

    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)

    shirt_number: Mapped[int | None] = mapped_column(Integer)

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    player = relationship(
    "Player",
    back_populates="clubs",
    )

    club = relationship(
    "Club",
    back_populates="players",)