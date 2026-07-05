from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config.settings import DB_CONFIG


def get_engine() -> Engine:
    """
    Create and return a SQLAlchemy engine.
    """

    connection_string = (
        f"postgresql+psycopg2://"
        f"{DB_CONFIG['user']}:"
        f"{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:"
        f"{DB_CONFIG['port']}/"
        f"{DB_CONFIG['database']}"
    )

    return create_engine(
        connection_string,
        echo=False,
        future=True
    )