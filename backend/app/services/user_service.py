import logging
from typing import List, Optional, Tuple

from password_strength import PasswordPolicy
from sqlalchemy.orm import Session

from database.models import User

from ..core.config import settings
from ..core.security import get_password_hash

logger = logging.getLogger(__name__)
policy = PasswordPolicy.from_names(entropybits=settings.PASSWORD_ENTROPY_BITS)
PASSWORD_MSG = "Password is not strong enough, maybe make it longer"
USER_NOT_FOUND_MSG = "User with username ({username}) not found"


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter_by(username=username.lower()).one_or_none()


def get_user_by_id(db: Session, id: int) -> Optional[User]:
    return db.query(User).filter_by(id=id).one_or_none()


def update_user_in_db(
    db: Session,
    username: str,
    password: Optional[str] = None,
    full_name: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_superuser: Optional[bool] = None,
) -> Tuple[Optional[User], Optional[str]]:
    user_in_db = get_user_by_username(db, username.lower())
    if user_in_db is None:
        return None, USER_NOT_FOUND_MSG.format(username=username.lower())
    if password is not None:
        if policy.test(password):
            return None, PASSWORD_MSG
        user_in_db.hashed_password = get_password_hash(password)
    if full_name is not None:
        user_in_db.full_name = full_name.lower()
    if is_active is not None:
        user_in_db.is_active = is_active
    if is_superuser is not None:
        user_in_db.is_superuser = is_superuser
    db.commit()
    return user_in_db, None


def create_user_in_db(
    db: Session,
    username: str,
    password: str,
    full_name: Optional[str] = None,
) -> Tuple[Optional[User], Optional[str]]:
    user_in_db = get_user_by_username(db, username.lower())
    if user_in_db is not None:
        return None, f"User with username ({username.lower()}) already exists"
    if policy.test(password):
        return None, PASSWORD_MSG
    new_user = User(
        username=username.lower(),
        hashed_password=get_password_hash(password),
        full_name=full_name.lower() if full_name is not None else None,
    )
    db.add(new_user)
    db.commit()
    return new_user, None


def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()
