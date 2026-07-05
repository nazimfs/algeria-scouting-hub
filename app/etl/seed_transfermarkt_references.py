from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import Player, PlayerSourceReference


TRANSFERMARKT_REFERENCES = [
    {
        "display_name": "Rayan Cherki",
        "source_player_id": "607223",
        "source_url": "https://www.transfermarkt.fr/rayan-cherki/profil/spieler/607223",
    },
    {
        "display_name": "Michael Olise",
        "source_player_id": "566723",
        "source_url": "https://www.transfermarkt.fr/michael-olise/profil/spieler/566723",
    },
    {
        "display_name": "Maghnes Akliouche",
        "source_player_id": "745200",
        "source_url": "https://www.transfermarkt.fr/maghnes-akliouche/profil/spieler/745200",
    },
    {
        "display_name": "Amine Gouiri",
        "source_player_id": "418659",
        "source_url": "https://www.transfermarkt.com/amine-gouiri/profil/spieler/418659",
    },
    {
        "display_name": "Zineddine Belaïd",
        "source_player_id": "625142",
        "source_url": "https://www.transfermarkt.fr/zineddine-belaid/profil/spieler/625142",
    },
]


def get_player_by_display_name(session: Session, display_name: str) -> Player | None:
    statement = select(Player).where(Player.display_name == display_name)
    return session.execute(statement).scalar_one_or_none()


def reference_exists(session: Session, player_id, source_name: str) -> bool:
    statement = select(PlayerSourceReference).where(
        PlayerSourceReference.player_id == player_id,
        PlayerSourceReference.source_name == source_name,
    )

    existing_reference = session.execute(statement).scalar_one_or_none()

    return existing_reference is not None


def main() -> None:
    engine = get_engine()
    inserted_count = 0

    with Session(engine) as session:
        for reference_data in TRANSFERMARKT_REFERENCES:
            player = get_player_by_display_name(
                session=session,
                display_name=reference_data["display_name"],
            )

            if player is None:
                print(f"⚠️ Player not found: {reference_data['display_name']}")
                continue

            if reference_exists(
                session=session,
                player_id=player.player_id,
                source_name="Transfermarkt",
            ):
                continue

            reference = PlayerSourceReference(
                player_id=player.player_id,
                source_name="Transfermarkt",
                source_player_id=reference_data["source_player_id"],
                source_url=reference_data["source_url"],
            )

            session.add(reference)
            inserted_count += 1

        session.commit()

    print(f"✅ Transfermarkt references inserted: {inserted_count}")


if __name__ == "__main__":
    main()