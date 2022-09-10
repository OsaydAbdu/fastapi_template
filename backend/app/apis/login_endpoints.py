import logging
from datetime import timedelta
from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.apis.deps import get_current_user, get_db
from app.core import security
from app.core.config import settings
from app.services.login_service import authenticate_user
from database import models

login_router = APIRouter()

logger = logging.getLogger(__name__)


@login_router.post(
    "/access-token",
    response_model=schemas.Token,
)
def login_access_token(
    form_data: schemas.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password"
        )
    elif not user.is_active:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@login_router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user
