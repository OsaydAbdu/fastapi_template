from typing import Dict

from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.services.user_service import get_user_by_username  # noqa
from database.models import User


def user_in_db(db: Session, username: str) -> bool:
    user = db.query(User).filter_by(username=username).one_or_none()
    return user is not None


def user_not_in_db(db: Session, username: str) -> bool:
    return not user_in_db(db, username)


def assert_updated_user_info(
    db: Session,
    username: str,
    new_user_info: Dict[str, str],
    old_user_info: User,
):
    old_user_info_dict = old_user_info.to_dict()
    db.refresh(old_user_info)
    user_in_db = old_user_info
    assert user_in_db is not None, f"Update user {username} is not in db"
    # Check all new desired values are updated in db
    for key in new_user_info.keys():
        _compare_field(key, new_user_info, user_in_db)

    # Check old values are unchanged
    for key in old_user_info_dict.keys():
        if key not in new_user_info:
            _compare_field(key, old_user_info.to_dict(), user_in_db)


def _compare_field(key, user_info, db_obj):
    if key == "password":
        assert verify_password(user_info[key], db_obj.hashed_password)
    else:
        field = user_info[key]
        if isinstance(user_info[key], str) and key != "hashed_password":
            field = field.lower()
        assert field == getattr(
            db_obj, key
        ), f"feild ({key}) is not updated to value ({field}) from ({getattr(db_obj, key)})"
