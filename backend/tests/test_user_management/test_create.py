from http import HTTPStatus
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from database.models import User
from tests.utils import TEST_USER

from .utils import user_in_db, user_not_in_db

TEST_USER = TEST_USER[0]


def test_create_without_login(client: TestClient, db: Session):
    response = client.post("/user/create", json=TEST_USER)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text
    assert user_not_in_db(db, TEST_USER["username"])


def test_authorized_normal_user(
    db: Session,
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
):
    response = client.post(
        "/user/create", json=TEST_USER, headers=normal_user_token_headers
    )
    assert response.status_code == HTTPStatus.FORBIDDEN, response.text
    assert user_not_in_db(db, TEST_USER["username"])


def test_authorized_superuser(
    db: Session,
    client: TestClient,
    superuser_token_headers: Dict[str, str],
):
    response = client.post(
        "/user/create", json=TEST_USER, headers=superuser_token_headers
    )
    assert response.status_code == HTTPStatus.OK, response.text
    assert user_in_db(db, TEST_USER["username"])


def test_authorized_superuser_with_week_password(
    db: Session,
    client: TestClient,
    superuser_token_headers: Dict[str, str],
):
    data = TEST_USER.copy()
    data["password"] = "weekpassword"
    response = client.post("/user/create", json=data, headers=superuser_token_headers)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text
    assert user_not_in_db(db, data["username"])


def test_add_duplicate_user(
    db: Session,
    client: TestClient,
    superuser_token_headers: Dict[str, str],
):
    response = client.post(
        "/user/create", json=TEST_USER, headers=superuser_token_headers
    )
    assert response.status_code == HTTPStatus.OK, response.text
    assert user_in_db(db, TEST_USER["username"])
    count_before = db.query(User).count()
    response = client.post(
        "/user/create", json=TEST_USER, headers=superuser_token_headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    count_after = db.query(User).count()
    assert count_before == count_after
