from typing import Any

from app.connectors.base_connector import BaseConnector
from app.connectors.wikipedia.client import WikipediaClient
from app.connectors.wikipedia.parser import WikipediaParser
from app.connectors.wikipedia.validator import WikipediaValidator
from app.services.eligibility_analyzer import EligibilityAnalyzer


class WikipediaConnector(BaseConnector):
    source_name = "Wikipedia"
    source_type = "web"

    def __init__(self, player_name: str) -> None:
        self.player_name = player_name
        self.client = WikipediaClient()
        self.validator = WikipediaValidator()
        self.parser = WikipediaParser()
        self.analyzer = EligibilityAnalyzer()

    def fetch(self) -> str:
        return self.client.fetch_player_page(self.player_name)

    def validate(self, raw_data: str) -> bool:
        return self.validator.validate(raw_data)

    def parse(self, raw_data: str) -> dict[str, Any]:
        wikipedia_data = self.parser.parse(raw_data)
        eligibility_analysis = self.analyzer.analyze(wikipedia_data)

        return {
            "wikipedia_data": wikipedia_data,
            "eligibility_analysis": eligibility_analysis,
        }

    def run(self) -> list[dict[str, Any]]:
        raw_data = self.fetch()

        if not self.validate(raw_data):
            raise ValueError(f"Invalid Wikipedia page for {self.player_name}")

        parsed_data = self.parse(raw_data)

        return [parsed_data]