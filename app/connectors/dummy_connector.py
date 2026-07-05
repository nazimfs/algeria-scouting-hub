from typing import Any

from app.connectors.base_connector import BaseConnector


class DummyConnector(BaseConnector):
    source_name = "Dummy"
    source_type = "test"

    def fetch(self) -> list[dict[str, Any]]:
        return [
            {
                "source_entity_id": "dummy_001",
                "entity_type": "player",
                "payload": {
                    "full_name": "Rayan Cherki",
                    "birth_date": "2003-08-17",
                    "nationalities": ["France", "Algeria"],
                },
            }
        ]

    def parse(self, raw_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return raw_data

    def run(self) -> list[dict[str, Any]]:
        raw_data = self.fetch()
        return self.parse(raw_data)