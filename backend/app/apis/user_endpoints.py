import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.models import User

from .. import schemas
from ..services.user_service import create_user_in_db, get_all_users, update_user_in_db
from . import deps

logger = logging.getLogger(__name__)
user_router = APIRouter()


@user_router.get("/list", response_model=schemas.UsersList)
def list_all_users(
    superuser: User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    return get_all_users(db)


@user_router.put("/update", response_model=schemas.User)
def update_user(
    user_input: schemas.UserUpdate,
    superuser: User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):
    user, error_msg = update_user_in_db(
        db,
        user_input.username,
        user_input.password,
        user_input.full_name,
        user_input.is_active,
        user_input.is_superuser,
    )
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=error_msg,
        )
    return user


@user_router.post("/create", response_model=schemas.User)
def create_user(
    user_input: schemas.UserCreate,
    superuser: User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
):

    user, error_msg = create_user_in_db(
        db,
        user_input.username,
        user_input.password,
        user_input.full_name,
    )
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=error_msg,
        )
    return user
