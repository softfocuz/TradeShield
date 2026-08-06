from typing import Any, Optional

from pydantic import BaseModel


class ResponseSchema(BaseModel):

    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    details: Optional[Any] = None


def success_response(data: Any = None, message: Optional[str] = None) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message: str, details: Any = None) -> dict:
    return {
        "success": False,
        "message": message,
        "details": details,
    }
