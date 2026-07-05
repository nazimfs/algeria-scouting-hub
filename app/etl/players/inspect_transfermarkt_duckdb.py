from pathlib import Path

import duckdb


DUCKDB_PATH = Path("data/external/transfermarkt/transfermarkt-datasets.duckdb")


def main() -> None:
    if not DUCKDB_PATH.exists():
        raise FileNotFoundError(f"DuckDB file not found: {DUCKDB_PATH}")

    connection = duckdb.connect(str(DUCKDB_PATH), read_only=True)

    print("=" * 80)
    print("TABLES")
    print("=" * 80)

    tables = connection.execute("SHOW TABLES").fetchall()

    for table in tables:
        print(f"- {table[0]}")

    print("\n" + "=" * 80)
    print("PLAYERS COLUMNS")
    print("=" * 80)

    columns = connection.execute("DESCRIBE players").fetchall()

    for column in columns:
        print(column)

    print("\n" + "=" * 80)
    print("PLAYERS SAMPLE")
    print("=" * 80)

    sample = connection.execute(
        """
        SELECT *
        FROM players
        LIMIT 10
        """
    ).fetchdf()

    print(sample.to_string())

    print("\n" + "=" * 80)
    print("PLAYERS COUNT")
    print("=" * 80)

    count = connection.execute(
        """
        SELECT COUNT(*) AS total_players
        FROM players
        """
    ).fetchone()

    print(f"Total players: {count[0]}")

    connection.close()


if __name__ == "__main__":
    main()