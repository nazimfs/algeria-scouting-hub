from app.connectors.connector_runner import ConnectorRunner
from app.connectors.wikipedia.connector import WikipediaConnector
from app.services.landing_service import LandingService


PLAYERS = [
    "Rayan Cherki",
    "Michael Olise",
    "Maghnes Akliouche",
]


def main() -> None:
    landing_service = LandingService()
    runner = ConnectorRunner(landing_service)

    for player_name in PLAYERS:
        print("=" * 50)
        print(f"Processing: {player_name}")

        connector = WikipediaConnector(player_name=player_name)

        runner.run(
            connector=connector,
            entity="players",
        )


if __name__ == "__main__":
    main()