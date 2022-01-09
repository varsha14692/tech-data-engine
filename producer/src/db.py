"""Postgres interaction."""
import dataclasses
import logging
import os
from sqlalchemy import Table, Column, String, Float, MetaData
from sqlalchemy.engine import create_engine
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)

DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DATABASE_URI = os.getenv("DATABASE_URI", "localhost:5432/postgres")

db_string = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URI}"
db = create_engine(db_string)
meta = MetaData(db)

ARTICLES_TABLE = Table(
    "articles",
    meta,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("price", Float),
    Column("currency", String),
)

USERS_TABLE = Table(
    "users",
    meta,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("address", String),
    Column("number", String),
    Column("email", String),
)

PURCHASES_TABLE = Table(
    "purchases",
    meta,
    Column("id", String),
    Column("timestamp", String),
    Column("user_id", String),
    Column("article_id", String),
    Column("quantity", Integer)
)

def setup_database() -> None:
    """Create database table if missing."""
    logger.debug("Create db tables if missing.")
    with db.connect():
        ARTICLES_TABLE.create(checkfirst=True)
        USERS_TABLE.create(checkfirst=True)
        PURCHASES_TABLE.create(checkfirst=True)


def insert_records(data, table):
    """Insert data into db.

    :param data:    List of records to add to db.
    :param table:   Name of the table in which to add records.
    """
    setup_database()
    logger.info("Insert %d records into table '%s'", len(data), table)
    table = ARTICLES_TABLE if table == "articles" else USERS_TABLE

    with db.connect() as conn:
        for d in data:
            record = dataclasses.asdict(d)
            record["id"] = record.pop("id_")

            insert_statement = (
                insert(table)
                .values(**record)
                .on_conflict_do_nothing(index_elements=["id"])
            )
            conn.execute(insert_statement)
