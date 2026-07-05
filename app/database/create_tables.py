from app.database.connection import get_engine
from app.database.models import Base


def create_tables() -> None:
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès")


if __name__ == "__main__":
    create_tables()