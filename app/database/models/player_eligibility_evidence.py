import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base


class PlayerEligibilityEvidence(Base):
    __tablename__ = "player_eligibility_evidences"

    evidence_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    player_name: Mapped[str] = mapped_column(String(150), nullable=False)

    eligibility_country: Mapped[str] = mapped_column(String(100), nullable=False)

    source_name: Mapped[str] = mapped_column(String(100), nullable=False)

    source_section: Mapped[str | None] = mapped_column(String(150))

    evidence_type: Mapped[str] = mapped_column(String(80), nullable=False)

    evidence_text: Mapped[str] = mapped_column(Text, nullable=False)

    confidence: Mapped[str] = mapped_column(String(30), nullable=False)

    raw_ingestion_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scouting.raw_ingestions.id"),
        nullable=True,
    )

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    raw_ingestion = relationship("RawIngestion")