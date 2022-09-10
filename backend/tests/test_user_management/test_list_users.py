from http import HTTPStatus
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from database.models import User
from tests.utils import TEST_USER

TEST_USER = TEST_USER[0]


def test_get_list_without_login(client: TestClient, db: Session):
    response = client.get("/user/list")
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text


def test_list_user_with_authorized_normal_user(
    db: Session,
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
):
    response = client.get("/user/list", headers=normal_user_token_headers)
    assert response.status_code == HTTPStatus.FORBIDDEN, response.text


def test_list_users_with_authorized_superuser(
    db: Session,
    client: TestClient,
    test_user: User,
    superuser_token_headers: Dict[str, str],
):
    response = client.get(
        "/user/list",
        headers=superuser_token_headers,
    )
    assert response.status_code == HTTPStatus.OK, response.text
    assert response.json()[0]["username"] == "admin@mozn.sa", response.json()

    assert response.json()[1]["username"] == TEST_USER["username"], response.json()
