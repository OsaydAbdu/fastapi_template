import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from database.db_session.session import SessionLocal

logger = logging.getLogger(__name__)

max_tries = 60 * 10  # 10 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        with SessionLocal() as db:
            db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Backend Pre-Start: Initializing service")
    init()
    logger.info("Backend Pre-Start: Service finished initializing")


if __name__ == "__main__":
    main()
