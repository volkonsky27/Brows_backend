from src.config import settings
from fastapi import Request, HTTPException, status


async def check_admin_token(request: Request) -> bool:
    token = request.headers.get("Token")
    if token == settings.SECRET_TOKEN:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong token")


async def check_public_token(request: Request) -> bool:
    token = request.headers.get("Token")
    if token == settings.PUBLIC_TOKEN:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong token")
