from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from database.db_alembic.utils import get_db_url

# logger = logging_setup.basic_logger("sqlalchemy_session")

# NOTE: The default isolation_level of PostgreSQL is READ COMMITTED while
# MySQL's default is REPEATABLE READ. So we explicitly set READ COMMITTED
# when using MySQL
engine = create_engine(
    get_db_url(),
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,
    isolation_level="READ COMMITTED",
    # by defualt mysql closes open connections after 8 hours (28800 sec) of inactivity
    pool_recycle=28800,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialize_db(db: Session):
    """
    This function attempts to create the database if it does not exist
    NOTE: This is required because the MySQL OCI resource does not provide
        the ability to create the database on resource creation while AWS does.
    """
    with SessionLocal() as db:
        db.execute(f"CREATE DATABASE IF NOT EXISTS `{settings.MYSQL_DATABASE}`")


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db
