from abc import ABC, abstractmethod
from typing import Any


class BaseConnector(ABC):
    """
    Base interface for all external data connectors.

    A connector can be:
    - a scraper
    - an API client
    - a CSV importer
    - an Excel importer
    """

    source_name: str
    source_type: str

    @abstractmethod
    def fetch(self) -> Any:
        """
        Fetch raw data from the external source.
        """
        pass

    @abstractmethod
    def parse(self, raw_data: Any) -> list[dict]:
        """
        Parse raw data into a list of dictionaries.
        """
        pass

    @abstractmethod
    def run(self) -> list[dict]:
        """
        Execute the full connector pipeline.
        """
        pass