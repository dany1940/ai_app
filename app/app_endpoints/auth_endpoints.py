from typing import cast

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError  # type: ignore
from jose import jwt  # type: ignore

from app import conf, models, schemas
from app.commons import Token, UserAuthorisation
from app.dependencies import CurrentUser, Database, authenticate_user
from app.security import (create_access_token, create_refresh_token,
                          refresh_token_valid, revoke_refresh_token)

router = APIRouter(
    prefix="/auth",
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    database: Database,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(database, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": create_access_token(cast(str, user.username)),
        "refresh_token": create_refresh_token(cast(str, user.username)),
        "expires_in": conf.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        "token_type": "bearer",
        "role": (UserAuthorisation.ADMIN if user.can_edit else UserAuthorisation.USER),
    }


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    database: Database,
    refresh_token: str = Form(...),
    grant_type: str = Form(...),
):
    bad_request_exception = HTTPException(
        status.HTTP_400_BAD_REQUEST,
        detail="The provided access grant is invalid, expired, or revoked",
    )
    # grant_type
    #     REQUIRED. Value MUST be set to "refresh_token".
    # https://www.rfc-editor.org/rfc/rfc6749#page-47
    if grant_type != "refresh_token":
        raise bad_request_exception

    # check that the provided refresh token is a well formed
    # JWT token.
    try:
        payload = jwt.decode(
            refresh_token, conf.SECRET_KEY, algorithms=[conf.HASH_ALGORITHM]
        )
    except JWTError as error:
        raise bad_request_exception from error

    # check that the provided refresh token has not been
    # revoked.
    if not refresh_token_valid(refresh_token):
        raise bad_request_exception

    # if the payload type is not "refresh", then the
    # provided access grant is invalid.
    if payload.get("type") != "refresh":
        raise bad_request_exception

    username = cast(str | None, payload.get("sub"))
    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if username is None:
        raise invalid_credentials_exception
    user: models.User | None = (
        database.query(models.User)
        .filter(models.User.username == username)
        .one_or_none()
    )
    if user is None:
        raise invalid_credentials_exception

    # revoke the existing refresh token since a new one will
    # be created and returned in the response.
    revoke_refresh_token(refresh_token)

    return {
        "access_token": create_access_token(username, fresh=False),
        "refresh_token": create_refresh_token(username, fresh=False),
        "token_type": "bearer",
        "expires_in": conf.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        "role": (
            schemas.UserAuthorisation.ADMIN
            if user.can_edit
            else schemas.UserAuthorisation.USER
        ),
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: CurrentUser):
    """
    Revoke the user's currently active refresh token.

    NOTE: This function does not revoke the user's active *access token*.
          This will expire naturally after the exp time.
    """
    revoke_refresh_token(current_user.username)
