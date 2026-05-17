import os
from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["dev"])

DEV_PASSWORD = os.getenv("DEV_PASSWORD")

if not DEV_PASSWORD:
    raise RuntimeError("Переменная DEV_PASSWORD не задана в .env!")


@router.post("/check-password")
async def check_password(payload: dict):
    password = payload.get("password", "")
    if not password or password != DEV_PASSWORD:
        return {"valid": False}
    return {"valid": True}
