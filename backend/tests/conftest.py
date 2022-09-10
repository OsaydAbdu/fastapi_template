from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.main import app
from app.services import DataSets, query_service
from app.services.user_service import (
    create_user_in_db,
    get_user_by_username,
    update_user_in_db,
)
from database.db_session import SessionLocal
from database.models import User

from .utils import TEST_USER


@pytest.fixture(scope="session", autouse=True)
def load_models():
    file_name = "/backend/tests/test_files/sample.xlsx"
    es_index_name = DataSets.sample.value
    if not query_service.use_index(es_index_name=es_index_name):
        query_service.create_index(file_name, es_index_name)
        query_service.use_index(es_index_name=es_index_name)


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Return a database session that can only support flushing and no commits,
    and rollback all transaction at the teardown phase and close the session.
    This is useful to keep tests without side effects.
    """
    with SessionLocal() as session:
        yield session
        session.rollback()
        session.query(User).filter(User.id > 1).delete()
        session.commit()


@pytest.fixture(scope="function")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return superuser_authentication_headers(client)


@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    username = TEST_USER[2]["username"]
    password = TEST_USER[2]["password"]
    full_name = TEST_USER[2]["full_name"]
    user = get_user_by_username(db, username=username)
    if not user:
        user, _ = create_user_in_db(
            db=db, username=username, password=password, full_name=full_name
        )
    else:
        user, _ = update_user_in_db(
            db, username=username, password=password, full_name=full_name
        )
    return user_authentication_headers(
        db, client=client, username=username, password=password
    )


@pytest.fixture(scope="function")
def test_user(db: Session):
    user, _ = create_user_in_db(
        db=db,
        username=TEST_USER[0]["username"],
        password=TEST_USER[0]["password"],
        full_name=TEST_USER[0]["full_name"],
    )
    yield user


def superuser_authentication_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post("/login/access-token", data=login_data).json()
    a_token = response["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def user_authentication_headers(
    db, *, client: TestClient, username: str, password: str
) -> Dict[str, str]:
    login_data = {
        "username": username.lower(),
        "password": password,
    }
    response = client.post("/login/access-token", data=login_data).json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
