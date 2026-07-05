from sqlalchemy import select
from sqlalchemy.orm import Session

from app.connectors.transfermarkt.connector import TransfermarktConnector
from app.database.connection import get_engine
from app.database.models import Player, PlayerSourceReference
from app.services.landing_service import LandingService
from app.services.raw_ingestion_service import RawIngestionService


def get_transfermarkt_references() -> list[dict]:
    engine = get_engine()

    with Session(engine) as session:
        statement = (
            select(PlayerSourceReference, Player)
            .join(Player, PlayerSourceReference.player_id == Player.player_id)
            .where(PlayerSourceReference.source_name == "Transfermarkt")
            .order_by(Player.display_name)
        )

        rows = session.execute(statement).all()

        references = []

        for source_reference, player in rows:
            references.append(
                {
                    "entity_name": player.display_name,
                    "source_player_id": source_reference.source_player_id,
                    "source_url": source_reference.source_url,
                }
            )

        return references


def main() -> None:
    references = get_transfermarkt_references()

    if not references:
        print("⚠️ No Transfermarkt references found")
        return

    landing_service = LandingService()
    results = []

    for reference in references:
        entity_name = reference["entity_name"]
        source_url = reference["source_url"]
        source_player_id = reference["source_player_id"]

        print("=" * 50)
        print(f"Processing: {entity_name}")

        connector = TransfermarktConnector(
            entity_name=entity_name,
            source_url=source_url,
            source_player_id=source_player_id,
        )

        try:
            player_results = connector.run()
            results.extend(player_results)
            print(f"✅ Success: {entity_name}")

        except Exception as error:
            print(f"❌ Error processing {entity_name}: {error}")

            results.append(
                {
                    "source": "Transfermarkt",
                    "source_type": "web",
                    "entity_type": "player",
                    "entity_name": entity_name,
                    "source_entity_id": source_player_id,
                    "source_url": source_url,
                    "status": "failed",
                    "payload": None,
                    "error": str(error),
                }
            )

    filepath = landing_service.save(
        source="transfermarkt",
        entity="players_batch",
        payload=results,
    )

    print("=" * 50)
    print(f"✅ Batch saved: {filepath}")
    print(f"Players processed: {len(results)}")

    raw_ingestion_service = RawIngestionService()
    saved_count = raw_ingestion_service.save_batch(results)

    print(f"✅ Raw ingestions saved to PostgreSQL: {saved_count}")


if __name__ == "__main__":
    main()