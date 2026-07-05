from typing import Any

from app.connectors.base_connector import BaseConnector
from app.connectors.transfermarkt.client import TransfermarktClient
from app.connectors.transfermarkt.parser import TransfermarktParser
from app.connectors.transfermarkt.validator import TransfermarktValidator
from app.services.transfermarkt_normalizer import TransfermarktNormalizer


class TransfermarktConnector(BaseConnector):
    source_name = "Transfermarkt"
    source_type = "web"

    def __init__(
        self,
        entity_name: str,
        source_url: str,
        source_player_id: str | None = None,
    ) -> None:
        self.entity_name = entity_name
        self.source_url = source_url
        self.source_player_id = source_player_id

        self.client = TransfermarktClient()
        self.validator = TransfermarktValidator()
        self.parser = TransfermarktParser()
        self.normalizer = TransfermarktNormalizer()

    def fetch(self) -> str:
        return self.client.fetch_player_page(self.source_url)

    def validate(self, raw_data: str) -> bool:
        return self.validator.validate(raw_data)

    def parse(self, raw_data: str) -> dict[str, Any]:
        parsed_data = self.parser.parse(raw_data)
        normalized_data = self.normalizer.normalize(parsed_data)

        return {
            "parsed_data": parsed_data,
            "normalized_data": normalized_data,
        }

    def run(self) -> list[dict[str, Any]]:
        raw_data = self.fetch()

        if not self.validate(raw_data):
            raise ValueError(f"Invalid Transfermarkt page for {self.entity_name}")

        parsed_data = self.parse(raw_data)

        return [
            {
                "source": self.source_name,
                "source_type": self.source_type,
                "entity_type": "player",
                "entity_name": self.entity_name,
                "source_entity_id": self.source_player_id,
                "source_url": self.source_url,
                "status": "success",
                "payload": parsed_data,
                "error": None,
            }
        ]