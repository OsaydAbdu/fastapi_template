import logging
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "vote"
    VERSION: str = "0.1.0"
    ROOT_PATH: str = "/backend"
    LOG_LEVEL: int = logging.INFO

    # Security configs
    # 60 minutes/hour * 24 hours/day * 7 days = 7 days in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PASSWORD_ENTROPY_BITS: int = 50
    DEFAULT_DB_VARCHAR_SIZE: int = 255

    FIRST_SUPERUSER: str = "osaydabdu@gmail.com"
    FIRST_SUPERUSER_FULL_NAME: str = "Admin Superuser"
    FIRST_SUPERUSER_PASSWORD: str = (
        "StRoNg_PaSsWoRd_DoNt_ChAnGe_EvEr_UnLeSs_YoU_aRe_InSaNe"
    )


settings = Settings()
