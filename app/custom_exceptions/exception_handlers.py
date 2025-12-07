from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.custom_exceptions.custom_exceptions import (
    ServiceError,
)


async def service_error_handler(
    request: Request,
    exc: ServiceError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": f"ServiceError: {str(exc)}",
        },
    )
