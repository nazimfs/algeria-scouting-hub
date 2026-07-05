from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.etl.players.import_transfermarkt_players import get_country_id_by_name


def main() -> None:
    engine = get_engine()

    countries_to_test = [
        "Algeria",
        "France",
        "Germany",
        "Brazil",
        "Netherlands",
        "England",
        "Réunion",
        "East Germany (GDR)",
    ]

    with Session(engine) as session:
        for country_name in countries_to_test:
            country_id = get_country_id_by_name(
                session=session,
                country_name=country_name,
            )

            print(f"{country_name} -> {country_id}")


if __name__ == "__main__":
    main()