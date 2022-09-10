from sqlalchemy import VARCHAR, Boolean, Column, Integer

from .base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True, unique=True)
    full_name = Column(VARCHAR(length=256))
    username = Column(VARCHAR(length=256), unique=True, index=True, nullable=False)
    hashed_password = Column(
        VARCHAR(length=256),
        nullable=False,
    )
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
