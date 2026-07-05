from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import Country


CSV_PATH = Path("data/external/iso_countries/all.csv")


def normalize_string(value: Any) -> str | None:
    if value is None:
        return None

    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value or value.lower() in {"nan", "none", "nat", "<na>"}:
        return None

    return value


def get_existing_country_by_iso3(
    session: Session,
    iso3_code: str,
) -> Country | None:
    statement = select(Country).where(
        Country.iso3_code == iso3_code,
    )

    return session.execute(statement).scalar_one_or_none()


def get_iso_countries() -> list[dict[str, Any]]:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    dataframe = pd.read_csv(CSV_PATH)

    return dataframe.to_dict(orient="records")


def main() -> None:
    rows = get_iso_countries()

    print(f"ISO countries found: {len(rows)}")

    engine = get_engine()

    inserted_count = 0
    updated_count = 0
    skipped_count = 0

    with Session(engine) as session:
        for row in rows:
            name = normalize_string(row.get("name"))
            alpha_2 = normalize_string(row.get("alpha-2"))
            alpha_3 = normalize_string(row.get("alpha-3"))
            region = normalize_string(row.get("region")) or "Unknown"

            if name is None or alpha_2 is None or alpha_3 is None:
                skipped_count += 1
                continue

            existing_country = get_existing_country_by_iso3(
                session=session,
                iso3_code=alpha_3,
            )

            if existing_country is not None:
                existing_country.iso2_code = alpha_2
                existing_country.iso3_code = alpha_3
                existing_country.fifa_code = alpha_3
                existing_country.official_name = name
                existing_country.short_name = name
                existing_country.continent = region
                existing_country.is_fifa_member = True
                updated_count += 1
                continue

            country = Country(
                iso2_code=alpha_2,
                iso3_code=alpha_3,
                fifa_code=alpha_3,
                official_name=name,
                short_name=name,
                continent=region,
                is_fifa_member=True,
            )

            session.add(country)
            inserted_count += 1

        session.commit()

    print("=" * 80)
    print("ISO countries import completed")
    print("=" * 80)
    print(f"Inserted countries: {inserted_count}")
    print(f"Updated countries: {updated_count}")
    print(f"Skipped countries: {skipped_count}")


if __name__ == "__main__":
    main()