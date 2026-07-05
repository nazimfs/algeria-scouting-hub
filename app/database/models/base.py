from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData(schema="scouting")


class Base(DeclarativeBase):
    metadata = metadata