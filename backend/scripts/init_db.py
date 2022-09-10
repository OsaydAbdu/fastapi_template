import logging

from app.core.config import settings
from app.core.security import get_password_hash
from database.db_session.session import SessionLocal
from database.models import User

logger = logging.getLogger(__name__)


def fill_db_with_initial_data() -> None:
    with SessionLocal() as db:
        try:
            super_user = User(
                full_name=settings.FIRST_SUPERUSER_FULL_NAME,
                username=settings.FIRST_SUPERUSER,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_active=True,
                is_superuser=True,
            )
            db.add(super_user)
            db.commit()
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    logger.info("Inserting default user into db")
    fill_db_with_initial_data()
