import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base
from app.database.models.mixins import TimestampMixin, UUIDMixin


class CompetitionSeason(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "competition_seasons"

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

    competition = relationship("Competition")
    season = relationship("Season")