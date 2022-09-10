from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserGet(BaseModel):
    username: str


# Properties to receive via API on creation
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None


# Properties to receive via API on update
class UserUpdate(BaseModel):
    username: str
    password: str = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None


class UserInDBBase(UserBase):
    username: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UsersList(BaseModel):
    __root__: List[UserInDBBase]

    class Config:
        orm_mode = True


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
