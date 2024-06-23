import os
import secrets

from dotenv import load_dotenv


class Config:
    load_dotenv()
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # https://cloud.google.com/apigee/docs/api-platform/antipatterns/oauth-long-expiration
    # Access tokens expire after 30 minutes.
    # Refresh tokens expire after 24 hours (1,440 minutes).
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1_440
    HASH_ALGORITHM: str = "HS256"


config = Config()
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
REFRESH_TOKEN_EXPIRE_MINUTES: int = 1_440
HASH_ALGORITHM: str = "HS256"
