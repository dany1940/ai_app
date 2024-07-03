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
    POSTGRES_TEST_USER = os.getenv("POSTGRES_TEST_USER")
    POSTGRES_TEST_PASSWORD = os.getenv("POSTGRES_TEST_PASSWORD")
    POSTGRES_TEST_DB = os.getenv("POSTGRES_TEST_DB")
    POSTGRES_TEST_HOST = os.getenv("POSTGRES_TEST_HOST")
    POSTGRES_TEST_PORT = os.getenv("POSTGRES_TEST_PORT")
    # https://cloud.google.com/apigee/docs/api-platform/antipatterns/oauth-long-expiration
    # Access tokens expire after 30 minutes.
    # Refresh tokens expire after 24 hours (1,440 minutes).
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1_440
    HASH_ALGORITHM: str = "HS256"
    DB_CONFIG = os.getenv(
        "DATABASE_URL",
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    DB_TEST_URL = os.getenv(
        "DATABASE_TEST_URL",
        f"postgresql+asyncpg://{POSTGRES_TEST_USER}:{POSTGRES_TEST_PASSWORD}@{POSTGRES_TEST_HOST}:{POSTGRES_TEST_PORT}/{POSTGRES_TEST_DB}"
    )


config = Config




