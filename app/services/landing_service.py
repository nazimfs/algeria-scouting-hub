import json
from datetime import datetime
from pathlib import Path


class LandingService:
    """
    Responsible for storing raw data exactly as received from external sources.
    """

    RAW_FOLDER = Path("data/raw")

    def save(
        self,
        source: str,
        entity: str,
        payload: list[dict],
    ) -> Path:

        self.RAW_FOLDER.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"{source}_{entity}_{timestamp}.json"

        filepath = self.RAW_FOLDER / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4, ensure_ascii=False)

        return filepath