from sqlalchemy import text

from app.database.connection import get_engine


def main() -> None:
    print("=" * 40)
    print("     Algeria Scouting Hub")
    print("=" * 40)

    engine = get_engine()

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("✅ PostgreSQL connecté")


if __name__ == "__main__":
    main()