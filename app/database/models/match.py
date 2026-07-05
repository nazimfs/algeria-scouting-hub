import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base
from app.database.models.mixins import TimestampMixin, UUIDMixin


class Match(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "matches"

    competition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.competitions.competition_id"),
        nullable=False,
    )

    season_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.seasons.season_id"),
        nullable=False,
    )

    match_date: Mapped[date] = mapped_column(Date, nullable=False)

    home_club_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.clubs.club_id"),
        nullable=False,
    )

    away_club_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.clubs.club_id"),
        nullable=False,
    )

    home_score: Mapped[int | None] = mapped_column(Integer)
    away_score: Mapped[int | None] = mapped_column(Integer)

    competition = relationship("Competition")
    season = relationship("Season")
    home_club = relationship("Club", foreign_keys=[home_club_id])
    away_club = relationship("Club", foreign_keys=[away_club_id])