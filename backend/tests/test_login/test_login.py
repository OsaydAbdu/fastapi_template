from http import HTTPStatus
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from database.models import User
from tests.utils import TEST_USER

TEST_USER = TEST_USER[0]


def test_failed_login(client: TestClient):
    # Non-existence user
    data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"],
    }
    response = client.post("/login/access-token", data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST, response.text

    # Wrong password
    data["username"] = settings.FIRST_SUPERUSER
    response = client.post("/login/access-token", data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST, response.text


def test_inactive_user_login(client: TestClient, db: Session):
    data = {
        "username": "TEST_USER@TEST_USER.com",
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    new_user = User(
        username=data["username"],
        hashed_password=get_password_hash(data["password"]),
        is_active=False,
    )
    db.add(new_user)
    db.commit()
    response = client.post("/login/access-token", data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST, response.text


def test_successful_login(client: TestClient):
    data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post("/login/access-token", data=data)
    assert response.status_code == HTTPStatus.OK, response.text
    assert "access_token" in response.json()


def test_test_login_endpoint_without_login(client: TestClient):
    data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"],
    }
    response = client.post("/login/test-token")
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text


def test_test_login_endpoint_with_superuser_login(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
):
    response = client.post("/login/test-token", headers=superuser_token_headers)
    assert response.status_code == HTTPStatus.OK, response.text


def test_test_login_endpoint_with_normal_login(
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
):
    response = client.post("/login/test-token", headers=normal_user_token_headers)
    assert response.status_code == HTTPStatus.OK, response.text


from datetime import datetime, timedelta, timezone
from unittest.mock import patch


def test_access_token_expiry(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        f"/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == HTTPStatus.OK

    time_token_expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    with patch("app.apis.deps.get_datetime_utc_now", lambda: time_token_expires):
        r = client.post(
            f"/login/test-token",
            headers=superuser_token_headers,
        )
        result = r.json()
        assert r.status_code == HTTPStatus.FORBIDDEN
