from datetime import date, datetime
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import Country, Player, PlayerSourceReference


DUCKDB_PATH = Path("data/external/transfermarkt/transfermarkt-datasets.duckdb")
SOURCE_NAME = "Transfermarkt"

COUNTRY_NAME_ALIASES = {
    "England": "United Kingdom of Great Britain and Northern Ireland",
    "Scotland": "United Kingdom of Great Britain and Northern Ireland",
    "Wales": "United Kingdom of Great Britain and Northern Ireland",
    "Northern Ireland": "United Kingdom of Great Britain and Northern Ireland",

    "Netherlands": "Netherlands, Kingdom of the",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "Russia": "Russian Federation",
    "Iran": "Iran, Islamic Republic of",
    "Syria": "Syrian Arab Republic",
    "Moldova": "Moldova, Republic of",
    "Bolivia": "Bolivia, Plurinational State of",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Vietnam": "Viet Nam",
    "Tanzania": "Tanzania, United Republic of",
    "DR Congo": "Congo, Democratic Republic of the",
    "Congo DR": "Congo, Democratic Republic of the",
    "Congo": "Congo",
    "Cape Verde": "Cabo Verde",
    "Ivory Coast": "Côte d'Ivoire",
    "Czech Republic": "Czechia",
    "Turkey": "Türkiye",
    "East Germany (GDR)": "Germany",
}


def normalize_string(value: Any) -> str | None:
    if value is None:
        return None

    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value or value.lower() in {"nan", "none", "nat", "<na>"}:
        return None

    return value


def normalize_date(value: Any) -> date | None:
    if value is None:
        return None

    if pd.isna(value):
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    value = str(value).strip()

    if not value or value.lower() in {"nan", "none", "nat", "<na>"}:
        return None

    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


def normalize_int(value: Any) -> int | None:
    if value is None:
        return None

    if pd.isna(value):
        return None

    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def get_transfermarkt_players() -> list[dict[str, Any]]:
    if not DUCKDB_PATH.exists():
        raise FileNotFoundError(f"DuckDB file not found: {DUCKDB_PATH}")

    connection = duckdb.connect(str(DUCKDB_PATH), read_only=True)

    query = """
        SELECT
            player_id,
            first_name,
            last_name,
            name,
            country_of_birth,
            city_of_birth,
            date_of_birth,
            height_in_cm,
            url
        FROM players
        WHERE name IS NOT NULL
        ORDER BY player_id
    """

    rows = connection.execute(query).fetchdf().to_dict(orient="records")
    connection.close()

    return rows


def get_country_id_by_name(
    session: Session,
    country_name: str | None,
):
    country_name = normalize_string(country_name)

    if country_name is None:
        return None

    mapped_country_name = COUNTRY_NAME_ALIASES.get(country_name, country_name)

    statement = select(Country.country_id).where(
        Country.short_name == mapped_country_name,
    )

    return session.execute(statement).scalar_one_or_none()


def get_existing_reference(
    session: Session,
    source_player_id: str,
) -> PlayerSourceReference | None:
    statement = select(PlayerSourceReference).where(
        PlayerSourceReference.source_name == SOURCE_NAME,
        PlayerSourceReference.source_player_id == source_player_id,
    )

    return session.execute(statement).scalar_one_or_none()


def create_player_from_transfermarkt_row(
    session: Session,
    row: dict[str, Any],
) -> Player:
    display_name = normalize_string(row.get("name"))

    first_name = normalize_string(row.get("first_name"))
    last_name = normalize_string(row.get("last_name"))

    if first_name is None:
        first_name = display_name

    if last_name is None:
        last_name = display_name

    return Player(
        first_name=first_name,
        last_name=last_name,
        display_name=display_name,
        birth_date=normalize_date(row.get("date_of_birth")),
        birth_city=normalize_string(row.get("city_of_birth")),
        birth_country_id=get_country_id_by_name(
            session=session,
            country_name=row.get("country_of_birth"),
        ),
        height_cm=normalize_int(row.get("height_in_cm")),
    )


def update_player_missing_fields(
    session: Session,
    player: Player,
    row: dict[str, Any],
) -> bool:
    was_updated = False

    birth_date = normalize_date(row.get("date_of_birth"))
    birth_city = normalize_string(row.get("city_of_birth"))
    birth_country_id = get_country_id_by_name(
        session=session,
        country_name=row.get("country_of_birth"),
    )
    height_cm = normalize_int(row.get("height_in_cm"))

    if birth_date is not None and player.birth_date is None:
        player.birth_date = birth_date
        was_updated = True

    if birth_city is not None and player.birth_city is None:
        player.birth_city = birth_city
        was_updated = True

    if birth_country_id is not None and player.birth_country_id is None:
        player.birth_country_id = birth_country_id
        was_updated = True

    if height_cm is not None and player.height_cm is None:
        player.height_cm = height_cm
        was_updated = True

    return was_updated


def create_reference(
    session: Session,
    player: Player,
    row: dict[str, Any],
) -> None:
    source_player_id = str(row["player_id"])
    source_url = normalize_string(row.get("url"))

    reference = PlayerSourceReference(
        player_id=player.player_id,
        source_name=SOURCE_NAME,
        source_player_id=source_player_id,
        source_url=source_url,
    )

    session.add(reference)


def main() -> None:
    rows = get_transfermarkt_players()

    print(f"Transfermarkt players found: {len(rows)}")

    engine = get_engine()

    inserted_players = 0
    updated_players = 0
    inserted_references = 0
    skipped_players = 0

    with Session(engine) as session:
        for index, row in enumerate(rows, start=1):
            source_player_id = str(row["player_id"])

            existing_reference = get_existing_reference(
                session=session,
                source_player_id=source_player_id,
            )

            if existing_reference is not None:
                player = existing_reference.player

                if update_player_missing_fields(
                    session=session,
                    player=player,
                    row=row,
                ):
                    updated_players += 1

                if index % 1000 == 0:
                    print(f"Processed {index}/{len(rows)} players...")

                continue

            display_name = normalize_string(row.get("name"))

            if display_name is None:
                skipped_players += 1
                continue

            player = create_player_from_transfermarkt_row(
                session=session,
                row=row,
            )

            session.add(player)
            session.flush()

            create_reference(
                session=session,
                player=player,
                row=row,
            )

            inserted_players += 1
            inserted_references += 1

            if index % 1000 == 0:
                print(f"Processed {index}/{len(rows)} players...")

        session.commit()

    print("=" * 80)
    print("Transfermarkt import completed")
    print("=" * 80)
    print(f"Inserted players: {inserted_players}")
    print(f"Updated players: {updated_players}")
    print(f"Inserted references: {inserted_references}")
    print(f"Skipped players: {skipped_players}")


if __name__ == "__main__":
    main()