import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base
from app.database.models.mixins import TimestampMixin, UUIDMixin


class ClubCompetition(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "club_competitions"

    club_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.clubs.club_id"),
        nullable=False,
    )

    competition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.competitions.competition_id"),
        nullable=False,
    )

    season_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.seasons.season_id"),
        nullable=True,
    )

    club = relationship("Club")
    competition = relationship("Competition")
    season = relationship("Season")