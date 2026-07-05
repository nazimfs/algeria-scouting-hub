from time import sleep

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.connectors.wikipedia.connector import WikipediaConnector
from app.database.connection import get_engine
from app.database.models import Country, DataSource, Player, RawIngestion
from app.services.landing_service import LandingService
from app.services.raw_ingestion_service import RawIngestionService


LIMIT = 300
SLEEP_SECONDS = 1


def get_france_born_players(limit: int) -> list[str]:
    engine = get_engine()

    with Session(engine) as session:
        already_ingested_players = (
            select(RawIngestion.source_entity_id)
            .join(DataSource, RawIngestion.data_source_id == DataSource.id)
            .where(
                DataSource.name == "Wikipedia",
                RawIngestion.entity_type == "player",
                RawIngestion.source_entity_id.is_not(None),
            )
        )

        statement = (
            select(Player.display_name)
            .join(Country, Player.birth_country_id == Country.country_id)
            .where(
                Country.short_name == "France",
                Player.display_name.not_in(already_ingested_players),
            )
            .order_by(Player.birth_date.desc().nulls_last())
            .limit(limit)
        )

        return list(session.execute(statement).scalars().all())


def main() -> None:
    player_names = get_france_born_players(limit=LIMIT)

    print("=" * 80)
    print("Wikipedia ingestion for France-born players")
    print("=" * 80)
    print(f"Players selected: {len(player_names)}")

    if len(player_names) == 0:
        print("No player to ingest.")
        return

    landing_service = LandingService()
    raw_ingestion_service = RawIngestionService()

    all_results = []

    for index, player_name in enumerate(player_names, start=1):
        print(f"[{index}/{len(player_names)}] Fetching Wikipedia page for: {player_name}")

        try:
            connector = WikipediaConnector(player_name=player_name)
            results = connector.run()
            all_results.extend(results)

            print(f"SUCCESS: {player_name}")

        except Exception as error:
            print(f"FAILED: {player_name} -> {error}")

            all_results.append(
                {
                    "source": "Wikipedia",
                    "source_type": "web",
                    "entity_type": "player",
                    "entity_name": player_name,
                    "status": "failed",
                    "payload": {},
                    "error": str(error),
                }
            )

        sleep(SLEEP_SECONDS)

    filepath = landing_service.save(
        source="wikipedia",
        entity="france_born_players",
        payload=all_results,
    )

    saved_count = raw_ingestion_service.save_batch(all_results)

    print("=" * 80)
    print("Wikipedia ingestion completed")
    print("=" * 80)
    print(f"Landing file: {filepath}")
    print(f"Raw ingestions saved: {saved_count}")


if __name__ == "__main__":
    main()