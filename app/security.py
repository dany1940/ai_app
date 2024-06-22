import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal

from app.conf import config

#context = CryptContext(schemes=["bcrypt"], deprecated="auto")
context = []
denylist = set()


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password against a hashed password.
    """
    return context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return context.hash(password)


def allowed_password(password: str) -> bool:
    """
    Return true if the password is a valid password
    """

    # TODO:
    # Add more complex password checking i.e. ensure that the password is above
    # a certain length, contains a number, contains a special character etc.

    return password != ""  # nosec: B105


def create_access_token(subject: str, fresh: bool = True) -> str:
    """
    Create an access_token for a given user.
    """
    return _create_token(  # nosec B106
        subject=subject,
        expires_at=datetime.now(tz=timezone.utc)
        + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
        fresh=fresh,
    )


def create_refresh_token(subject: str, fresh: bool = True) -> str:
    """
    Create a refresh_token for a given user.
    """
    return _create_token(  # nosec B106
        subject=subject,
        expires_at=datetime.now(tz=timezone.utc)
        + timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES),
        token_type="refresh",
        fresh=fresh,
    )


def _create_token(
    subject: str,
    expires_at: datetime,
    token_type: Literal["access", "refresh"],
    fresh: bool,
) -> str:
    token_data = {
        # The "sub" (subject) claim identifies the principal that is the
        # subject of the JWT.
        # https://www.rfc-editor.org/rfc/rfc7519#section-4.1.2
        "sub": subject,
        # The "exp" (expiration time) claim identifies the expiration time on
        # or after which the JWT MUST NOT be accepted for processing.
        # https://www.rfc-editor.org/rfc/rfc7519#section-4.1.4
        "exp": expires_at,
        # The "iat" (issued at) claim identifies the time at which the JWT was
        # issued.
        # https://www.rfc-editor.org/rfc/rfc7519#section-4.1.6
        "iat": datetime.now(tz=timezone.utc),
        # The "nbf" (not before) claim identifies the time before which the JWT
        # MUST NOT be accepted for processing.
        # https://www.rfc-editor.org/rfc/rfc7519#section-4.1.5
        "nbf": datetime.now(tz=timezone.utc),
        # The "jti" (JWT ID) claim provides a unique identifier for the JWT.
        # The identifier value MUST be assigned in a manner that ensures that
        # there is a negligible probability that the same value will be
        # accidentally assigned to a different data object
        # https://www.rfc-editor.org/rfc/rfc7519#section-4.1.7
        "jti": str(uuid.uuid4()),
        "type": token_type,
        "fresh": fresh,
    }

    return jwt.encode(
        claims=token_data,
        key=config.SECRET_KEY,
        algorithm=config.HASH_ALGORITHM,
    )


def revoke_refresh_token(token: str):
    """
    Revoke a refresh token from a given user.
    """
    denylist.add(token)


def refresh_token_valid(token: str):
    """
    Check if a given token is valid.
    """
    return token not in denylist
