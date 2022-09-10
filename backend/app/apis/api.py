from fastapi import APIRouter

from .login_endpoints import login_router
from .user_endpoints import user_router

api_router = APIRouter()
api_router.include_router(login_router, prefix="/login", tags=["User authentication"])
api_router.include_router(user_router, prefix="/user", tags=["User management"])
