from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import Player


PLAYERS = [
    {
        "first_name": "Rayan",
        "last_name": "Cherki",
        "display_name": "Rayan Cherki",
    },
    {
        "first_name": "Michael",
        "last_name": "Olise",
        "display_name": "Michael Olise",
    },
    {
        "first_name": "Maghnes",
        "last_name": "Akliouche",
        "display_name": "Maghnes Akliouche",
    },
    {
        "first_name": "Amine",
        "last_name": "Gouiri",
        "display_name": "Amine Gouiri",
    },
]


def player_exists(session: Session, display_name: str) -> bool:
    statement = select(Player).where(Player.display_name == display_name)
    existing_player = session.execute(statement).scalar_one_or_none()

    return existing_player is not None


def main() -> None:
    engine = get_engine()
    inserted_count = 0

    with Session(engine) as session:
        for player_data in PLAYERS:
            if player_exists(session, player_data["display_name"]):
                continue

            player = Player(
                first_name=player_data["first_name"],
                last_name=player_data["last_name"],
                display_name=player_data["display_name"],
            )

            session.add(player)
            inserted_count += 1

        session.commit()

    print(f"✅ Players inserted: {inserted_count}")


if __name__ == "__main__":
    main()