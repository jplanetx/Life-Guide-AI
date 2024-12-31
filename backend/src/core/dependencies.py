from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from typing import Annotated
from .config import Settings

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(
    api_key: Annotated[str, Depends(api_key_header)],
    settings: Annotated[Settings, Depends()]
):
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=403,
            detail="Could not validate API key"
        )
    return api_key

def get_settings():
    return Settings()

# Example of how to use in routes:
# @router.get("/protected-endpoint", dependencies=[Depends(verify_api_key)])