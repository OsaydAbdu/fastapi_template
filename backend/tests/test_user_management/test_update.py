from http import HTTPStatus
from typing import Dict, Union

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from database.models import User
from tests.utils import TEST_USER

from .utils import assert_updated_user_info, get_user_by_username, user_not_in_db


def test_update_user_without_login(client: TestClient, db: Session):
    response = client.put("/user/update", json=TEST_USER[0])
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text
    assert user_not_in_db(db, TEST_USER[0]["username"])


def test_update_user_with_authorized_normal_user(
    db: Session,
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
):
    response = client.put(
        "/user/update", json=TEST_USER[0], headers=normal_user_token_headers
    )
    assert response.status_code == HTTPStatus.FORBIDDEN, response.text
    assert user_not_in_db(db, TEST_USER[0]["username"])


def test_update_user_with_authorized_superuser(
    db: Session,
    client: TestClient,
    test_user: User,
    superuser_token_headers: Dict[str, str],
):
    username = TEST_USER[0]["username"]
    old_user_in_db = get_user_by_username(db, username)
    response = client.put(
        "/user/update", json=TEST_USER[1], headers=superuser_token_headers
    )
    assert response.status_code == HTTPStatus.OK, response.text
    assert_updated_user_info(db, username, TEST_USER[1], old_user_in_db)


def test_authorized_superuser_with_week_password(
    db: Session,
    client: TestClient,
    test_user: User,
    superuser_token_headers: Dict[str, str],
):
    data = TEST_USER[1].copy()
    data["password"] = "weekpassword"
    response = client.put("/user/update", json=data, headers=superuser_token_headers)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text


def test_update_non_existence_user_with_authorized_superuser(
    db: Session,
    client: TestClient,
    test_user: User,
    superuser_token_headers: Dict[str, str],
):
    data = {
        "username": "Random-non-existence-user@mozn.sa",
        "password": "RandomVeryLongPasswordICannotEveryMemorizeIt",
    }
    response = client.put("/user/update", json=data, headers=superuser_token_headers)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text


@pytest.mark.parametrize(
    "udpate_field,update_field_value",
    [
        ("is_superuser", True),
        ("is_superuser", False),
        ("is_active", True),
        ("is_active", False),
        ("password", "VeryVeryVeryStrongPassWordDontChangeEver"),
        ("full_name", "Test_new_user new_full_name"),
    ],
)
def test_update_user_to_superuser_with_authorized_superuser(
    db: Session,
    client: TestClient,
    test_user: User,
    superuser_token_headers: Dict[str, str],
    udpate_field: str,
    update_field_value: Union[bool, int],
):
    username = TEST_USER[0]["username"]
    Update_info_with_superuser = {
        udpate_field: update_field_value,
        "username": username,
    }
    old_user_in_db = get_user_by_username(db, username)
    response = client.put(
        "/user/update", json=Update_info_with_superuser, headers=superuser_token_headers
    )
    assert response.status_code == HTTPStatus.OK, response.text

    assert_updated_user_info(db, username, Update_info_with_superuser, old_user_in_db)
