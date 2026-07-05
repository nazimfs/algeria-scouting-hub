from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import Player


class PlayerEnrichmentService:
    def __init__(self) -> None:
        self.engine = get_engine()

    def enrich_players(self, player_payloads: list[dict[str, Any]]) -> int:
        updated_count = 0

        with Session(self.engine) as session:
            for payload in player_payloads:
                player = self._get_player_by_display_name(
                    session=session,
                    display_name=payload["display_name"],
                )

                if player is None:
                    continue

                was_updated = self._update_player_from_payload(
                    player=player,
                    payload=payload,
                )

                if was_updated:
                    updated_count += 1

            session.commit()

        return updated_count

    def _get_player_by_display_name(
        self,
        session: Session,
        display_name: str,
    ) -> Player | None:
        statement = select(Player).where(
            Player.display_name == display_name,
        )

        return session.execute(statement).scalar_one_or_none()

    def _update_player_from_payload(
        self,
        player: Player,
        payload: dict[str, Any],
    ) -> bool:
        was_updated = False

        if payload.get("birth_date") and player.birth_date is None:
            player.birth_date = date.fromisoformat(payload["birth_date"])
            was_updated = True

        if payload.get("height_cm") and player.height_cm is None:
            player.height_cm = payload["height_cm"]
            was_updated = True

        if payload.get("weight_kg") and player.weight_kg is None:
            player.weight_kg = payload["weight_kg"]
            was_updated = True

        if payload.get("preferred_foot") and player.preferred_foot is None:
            player.preferred_foot = payload["preferred_foot"]
            was_updated = True

        if payload.get("photo_url") and player.photo_url is None:
            player.photo_url = payload["photo_url"]
            was_updated = True

        return was_updated