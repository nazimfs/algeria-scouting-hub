from typing import Any

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import RawIngestion
from app.services.player_enrichment_service import PlayerEnrichmentService


def get_latest_transfermarkt_enrichment_payloads() -> list[dict[str, Any]]:
    engine = get_engine()
    payloads = []
    already_seen_players = set()

    with Session(engine) as session:
        statement = (
            select(RawIngestion)
            .where(
                RawIngestion.payload["source"].astext == "Transfermarkt",
                RawIngestion.payload["status"].astext == "success",
            )
            .order_by(desc(RawIngestion.ingested_at))
        )

        raw_ingestions = session.execute(statement).scalars().all()

        for raw_ingestion in raw_ingestions:
            payload = raw_ingestion.payload

            display_name = payload.get("entity_name")

            if display_name in already_seen_players:
                continue

            inner_payload = payload.get("payload", {})
            normalized_data = inner_payload.get("normalized_data", {})

            if not normalized_data:
                continue

            enrichment_payload = {
                "display_name": display_name,
                "birth_date": normalized_data.get("birth_date"),
                "birth_city": normalized_data.get("birth_city"),
                "height_cm": normalized_data.get("height_cm"),
                "preferred_foot": normalized_data.get("preferred_foot"),
                "photo_url": normalized_data.get("photo_url"),
            }

            payloads.append(enrichment_payload)
            already_seen_players.add(display_name)

    return payloads


def main() -> None:
    payloads = get_latest_transfermarkt_enrichment_payloads()

    if not payloads:
        print("⚠️ No Transfermarkt enrichment payloads found")
        return

    print("Transfermarkt enrichment payloads:")
    for payload in payloads:
        print(payload)

    service = PlayerEnrichmentService()
    updated_count = service.enrich_players(payloads)

    print(f"✅ Players enriched from Transfermarkt: {updated_count}")


if __name__ == "__main__":
    main()