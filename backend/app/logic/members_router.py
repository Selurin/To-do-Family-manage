from fastapi import APIRouter
from ..database import db 

router = APIRouter(prefix="/members", tags=["members"])

@router.get("/family/{family_id}")
async def get_family_members(family_id: int):
    # Вызываем функцию из database.py
    members = await db.get_family_members(family_id)
    
    return [dict(row) for row in members]