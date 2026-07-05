from app.connectors.connector_runner import ConnectorRunner
from app.connectors.wikipedia.connector import WikipediaConnector
from app.services.landing_service import LandingService


def main() -> None:
    connector = WikipediaConnector(
        player_name="rayan Cherki"
    )

    landing_service = LandingService()
    runner = ConnectorRunner(landing_service)

    runner.run(
        connector=connector,
        entity="players",
    )


if __name__ == "__main__":
    main()