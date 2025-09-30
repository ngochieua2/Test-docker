from typing import List
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    status: int
    message: str


class ErrorResponse(BaseModel):
    status: int
    errors: List[ErrorDetail]

def bad_request(status_code: int, error_code: int, message: str) -> JSONResponse:
    """
    Helper to return a standardized bad request JSON response.
    """
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            status=status_code,
            errors=[ErrorDetail(status=error_code, message=message)]
        ).model_dump()
    )
