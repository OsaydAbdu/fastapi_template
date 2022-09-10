import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.apis.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    root_path=settings.ROOT_PATH,
    version=settings.VERSION,
)

app.include_router(api_router)


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
