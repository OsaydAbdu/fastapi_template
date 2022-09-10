from typing import Optional

from sqlalchemy.orm import Session

from database.models import User

from ..core.security import verify_password
from .user_service import get_user_by_username


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if user is None:
        return None
    if verify_password(password, user.hashed_password):
        return user
    return None
