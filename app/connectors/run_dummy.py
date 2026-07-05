from app.connectors.connector_runner import ConnectorRunner
from app.connectors.dummy_connector import DummyConnector
from app.services.landing_service import LandingService


def main() -> None:
    connector = DummyConnector()
    landing_service = LandingService()
    runner = ConnectorRunner(landing_service)

    runner.run(
        connector=connector,
        entity="players",
    )


if __name__ == "__main__":
    main()