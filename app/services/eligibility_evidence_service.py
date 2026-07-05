from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import Player, PlayerEligibilityEvidence, RawIngestion


class EligibilityEvidenceService:
    def __init__(self) -> None:
        self.engine = get_engine()

    def extract_from_raw_ingestions(self) -> int:
        inserted_count = 0

        with Session(self.engine) as session:
            raw_ingestions = self._get_successful_wikipedia_player_ingestions(session)

            for raw_ingestion in raw_ingestions:
                inserted_count += self._extract_evidences_from_raw_ingestion(
                    session=session,
                    raw_ingestion=raw_ingestion,
                )

            session.commit()

        return inserted_count

    def _get_successful_wikipedia_player_ingestions(
        self,
        session: Session,
    ) -> list[RawIngestion]:
        statement = select(RawIngestion).where(
            RawIngestion.entity_type == "player",
        )

        return list(session.execute(statement).scalars().all())

    def _extract_evidences_from_raw_ingestion(
        self,
        session: Session,
        raw_ingestion: RawIngestion,
    ) -> int:
        payload: dict[str, Any] = raw_ingestion.payload

        if payload.get("status") != "success":
            return 0

        inner_payload = payload.get("payload", {})
        eligibility_analysis = inner_payload.get("eligibility_analysis", {})

        evidences = eligibility_analysis.get("evidences", [])

        inserted_count = 0
        player_name = payload.get("entity_name")
        player_id = self._get_player_id_by_display_name(
                session=session,
                display_name=player_name,
            )

        for evidence in evidences:  
            eligibility_country = evidence.get("target_country")
            source_name = payload.get("source")
            source_section = evidence.get("source_section")
            evidence_type = evidence.get("evidence_type")
            evidence_text = evidence.get("text")
            confidence = evidence.get("confidence")
            if self._evidence_already_exists(
                session=session,
                
                player_name=player_name,
                eligibility_country=eligibility_country,
                source_name=source_name,
                source_section=source_section,
                evidence_type=evidence_type,
                evidence_text=evidence_text,
            ):
                continue
            player_evidence = PlayerEligibilityEvidence(
                player_id=player_id,
                player_name=player_name,
                eligibility_country=eligibility_country,
                source_name=source_name,
                source_section=source_section,
                evidence_type=evidence_type,
                evidence_text=evidence_text,
                confidence=confidence,
                raw_ingestion_id=raw_ingestion.id,
            )

            session.add(player_evidence)
            inserted_count += 1

        return inserted_count
    

    def _evidence_already_exists(
        self,
        session: Session,
        player_name: str,
        eligibility_country: str,
        source_name: str,
        source_section: str | None,
        evidence_type: str,
        evidence_text: str,
    ) -> bool:
        statement = select(PlayerEligibilityEvidence).where(            
            PlayerEligibilityEvidence.player_name == player_name,
            PlayerEligibilityEvidence.eligibility_country == eligibility_country,
            PlayerEligibilityEvidence.source_name == source_name,
            PlayerEligibilityEvidence.source_section == source_section,
            PlayerEligibilityEvidence.evidence_type == evidence_type,
            PlayerEligibilityEvidence.evidence_text == evidence_text,
        )

        existing_evidence = session.execute(statement).scalar_one_or_none()

        return existing_evidence is not None
    
    def _get_player_id_by_display_name(self, session: Session, display_name: str):
        if display_name is None:
            return None

        statement = (
        select(Player.player_id)
        .where(Player.display_name == display_name)
        .order_by(Player.created_at.asc())
        .limit(1)
        )

        return session.execute(statement).scalar_one_or_none()