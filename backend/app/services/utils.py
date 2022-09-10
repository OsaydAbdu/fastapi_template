from datetime import datetime, timedelta

from database.db_session import SessionLocal
from database.models import Label


class GetLabelsList:
    """
    Singleton class to retrieve labels list
    Description:
        This is a class dedicated to provide up-to-date labels list to be used,
        the goal of making this singleton is to reduce the amount of calls to
        the database.
    """

    labels = None
    refresh_time = None
    __refresh_time = timedelta(days=1)
    __refresh_hour = 8

    def __new__(cls):
        if cls.labels is None or (
            cls.refresh_time is not None and datetime.utcnow() >= cls.refresh_time
        ):
            cls.refresh_time = datetime.utcnow() + cls.__refresh_time
            if cls.__refresh_hour:
                cls.refresh_time = cls.refresh_time.replace(hour=cls.__refresh_hour)

            with SessionLocal() as db:
                labels = db.query(Label).all()
                cls.labels = {label.name.strip().upper(): label.id for label in labels}
        return cls.labels
