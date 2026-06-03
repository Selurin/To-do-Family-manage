from fastapi import APIRouter, HTTPException
from ..models.families import FamilyCreate, FamilyOut
from ..database import db

router = APIRouter(prefix="/families", tags=["families"])

@router.post("", response_model=FamilyOut)
async def create_family(data: FamilyCreate):
    family_id = await db.create_family(data.name, data.invite_code)
    return FamilyOut(id=family_id, name=data.name, invite_code=data.invite_code)

@router.get("/{invite_code}", response_model=FamilyOut)
async def get_family(invite_code: str):
    family = await db.get_family_by_code(invite_code)
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return FamilyOut(
        id=family["id"],
        name=family["name"],
        invite_code=family["invite_code"],
    )
