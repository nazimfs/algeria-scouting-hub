from pathlib import Path

import duckdb


DUCKDB_PATH = Path("data/external/transfermarkt/transfermarkt-datasets.duckdb")


def main() -> None:
    connection = duckdb.connect(str(DUCKDB_PATH), read_only=True)

    print("=" * 80)
    print("COUNTRIES COLUMNS")
    print("=" * 80)

    columns = connection.execute("DESCRIBE countries").fetchall()

    for column in columns:
        print(column)

    print("\n" + "=" * 80)
    print("COUNTRIES SAMPLE")
    print("=" * 80)

    sample = connection.execute(
        """
        SELECT *
        FROM countries
        LIMIT 30
        """
    ).fetchdf()

    print(sample.to_string())

    print("\n" + "=" * 80)
    print("COUNTRIES COUNT")
    print("=" * 80)

    count = connection.execute(
        """
        SELECT COUNT(*)
        FROM countries
        """
    ).fetchone()

    print(f"Total countries: {count[0]}")

    connection.close()


if __name__ == "__main__":
    main()