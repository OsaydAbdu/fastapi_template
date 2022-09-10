from datetime import datetime
from typing import Optional

from fastapi import Form
from pydantic import BaseModel


class OAuth2PasswordRequestForm:
    """
    This is same as fastapi's OAuth2PasswordRequestForm but only with email
    and password (no grant_type, scope, client_id and client_secret).
    """

    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
    ):
        self.username = username
        self.password = password


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    exp: datetime
    sub: Optional[int] = None
