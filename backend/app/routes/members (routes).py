from fastapi import APIRouter
from ..models.members import MemberAdd
from ..main import db

router = APIRouter(prefix="/members", tags=["members"])

@router.post("")
async def add_member(data: MemberAdd):
    member_id = await db.add_member(data.user_id, data.family_id, data.role)
    return {"id": member_id}

@router.get("/family/{family_id}")
async def get_members(family_id: int):
    rows = await db.get_family_members(family_id)
    return [
        {
            "id": r["id"],
            "user_id": r["user_id"],
            "family_id": r["family_id"],
            "role": r["role"],
            "name": r["name"],
            "vk_id": r["vk_id"],
        }
        for r in rows
    ]
