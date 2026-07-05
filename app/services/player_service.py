from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import Player


class PlayerService:
    def __init__(self) -> None:
        self.engine = get_engine()

    def get_players_for_wikipedia_ingestion(self) -> list[str]:
        with Session(self.engine) as session:
            statement = (
                select(Player.display_name)
                .where(Player.display_name.is_not(None))
                .order_by(Player.display_name)
            )

            players = session.execute(statement).scalars().all()

            return list(players)