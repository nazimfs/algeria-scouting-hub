from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import DataSource, RawIngestion


class RawIngestionService:
    SOURCE_METADATA = {
        "Wikipedia": {
            "base_url": "https://fr.wikipedia.org/wiki/",
            "description": "French Wikipedia player pages",
        },
        "Transfermarkt": {
            "base_url": "https://www.transfermarkt.fr/",
            "description": "Transfermarkt player profile pages",
        },
    }

    def __init__(self) -> None:
        self.engine = get_engine()

    def save_batch(self, items: list[dict[str, Any]]) -> int:
        saved_count = 0

        with Session(self.engine) as session:
            for item in items:
                data_source = self._get_or_create_data_source(
                    session=session,
                    source_name=item["source"],
                    source_type=item["source_type"],
                )

                raw_ingestion = RawIngestion(
                    data_source_id=data_source.id,
                    entity_type=item["entity_type"],
                    source_entity_id=item.get("source_entity_id")
                    or item.get("entity_name"),
                    payload=item,
                    ingested_at=datetime.now(timezone.utc),
                )

                session.add(raw_ingestion)
                saved_count += 1

            session.commit()

        return saved_count

    def _get_or_create_data_source(
        self,
        session: Session,
        source_name: str,
        source_type: str,
    ) -> DataSource:
        statement = select(DataSource).where(DataSource.name == source_name)
        data_source = session.execute(statement).scalar_one_or_none()

        metadata = self.SOURCE_METADATA.get(
            source_name,
            {
                "base_url": None,
                "description": None,
            },
        )

        if data_source is not None:
            data_source.source_type = source_type
            data_source.base_url = metadata["base_url"]
            data_source.description = metadata["description"]
            return data_source

        data_source = DataSource(
            name=source_name,
            source_type=source_type,
            base_url=metadata["base_url"],
            description=metadata["description"],
            is_active=True,
        )

        session.add(data_source)
        session.flush()

        return data_source