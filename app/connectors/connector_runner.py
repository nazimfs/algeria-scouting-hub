from app.connectors.base_connector import BaseConnector
from app.services.landing_service import LandingService


class ConnectorRunner:
    def __init__(self, landing_service: LandingService) -> None:
        self.landing_service = landing_service

    def run(
        self,
        connector: BaseConnector,
        entity: str,
    ) -> None:
        data = connector.run()

        filepath = self.landing_service.save(
            source=connector.source_name.lower(),
            entity=entity,
            payload=data,
        )

        print(f"✅ Raw data saved: {filepath}")