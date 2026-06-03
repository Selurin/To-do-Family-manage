from fastapi import APIRouter, HTTPException
from ..models.users import UserCreate, UserOut
from ..main import db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserOut)
async def create_user(data: UserCreate):
    existing = await db.get_user_by_vk_id(data.vk_id)
    if existing:
        return UserOut(id=existing["id"], vk_id=existing["vk_id"], name=existing["name"])

    user_id = await db.create_user(data.vk_id, data.name)
    return UserOut(id=user_id, vk_id=data.vk_id, name=data.name)
