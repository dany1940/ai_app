from typing import TypeVar

from fastapi import HTTPException, status

T = TypeVar("T")


def scalar(value: list[T]) -> T:
    return value[0]


def expect(
    value: T | None,
    error_msg: str | None = None,
    status_code: int = status.HTTP_404_NOT_FOUND,
) -> T:
    """
    Unwrap a value or raise an HTTPException if the value is None.
    """
    if value is None:
        raise HTTPException(
            status_code=status_code,
            detail=error_msg,
        )
    return value
