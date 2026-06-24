from fastapi import Request

from fastapi.responses import JSONResponse

from ..errors.base import BaseApplicationException


async def app_exception_handler(
    request: Request,
    exception: BaseApplicationException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.detail,
        },
    )
