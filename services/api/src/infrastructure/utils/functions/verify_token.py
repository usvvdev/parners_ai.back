# packages

from pathlib import Path

from fastapi import (
    Depends,
    HTTPException,
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

# application dependencies

from libs.infrastructure.factories.common import ApplicationConfigFactory


config = ApplicationConfigFactory.create(
    service_dir=Path(__file__).parents[4],
)

security = HTTPBearer()


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials

    if token != config.access_token:
        raise HTTPException(status_code=401)

    return token
