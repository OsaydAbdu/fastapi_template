from datetime import datetime, timezone
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from database import models
from database.db_session.session import get_db

from .. import schemas
from ..core import security
from ..core.config import settings
from ..services.user_service import get_user_by_id

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/backend/login/access-token")


def get_datetime_utc_now():
    return datetime.now(timezone.utc)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Could not validate credentials",
        )
    if token_data.exp < get_datetime_utc_now():
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Expired token",
        )
    user = get_user_by_id(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
