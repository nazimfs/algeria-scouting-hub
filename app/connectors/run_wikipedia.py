from app.connectors.wikipedia.connector import WikipediaConnector
from app.services.landing_service import LandingService
from app.services.player_service import PlayerService
from app.services.raw_ingestion_service import RawIngestionService


def main() -> None:
    landing_service = LandingService()
    player_service = PlayerService()

    players = player_service.get_players_for_wikipedia_ingestion()

    if not players:
        print("⚠️ No players found for Wikipedia ingestion")
        return

    results = []

    for player_name in players:
        print("=" * 50)
        print(f"Processing: {player_name}")

        connector = WikipediaConnector(player_name=player_name)

        try:
            player_results = connector.run()
            results.extend(player_results)
            print(f"✅ Success: {player_name}")

        except Exception as error:
            print(f"❌ Error processing {player_name}: {error}")

            results.append(
                {
                    "source": "Wikipedia",
                    "source_type": "web",
                    "entity_type": "player",
                    "entity_name": player_name,
                    "status": "failed",
                    "payload": None,
                    "error": str(error),
                }
            )

    filepath = landing_service.save(
        source="wikipedia",
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