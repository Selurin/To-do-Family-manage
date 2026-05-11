from fastapi import APIRouter, HTTPException

from ..database import db
import random
import string

router = APIRouter(prefix="/family", tags=["family"])


async def code_generator():
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(10))
        existing = await db.get_family_by_invite_code(code)
        if not existing:
            return code


# создание семьи
@router.post("/create")
async def create_family(name: str, user_id: int):
    #ограничение на длину имени
    if len(name) > 45:
        return {"error": "name too long"}

    invite_code = await code_generator()

    await db.create_family(name, invite_code)
    family = await db.get_family_by_code(invite_code)
    family_id = family['id']

    await db.add_member(user_id, family_id, 'owner')

    return {
        "status": "family created",
        "invite_code": family['invite_code'],
        "family_id": family_id,
        "name": family['name'],
    }


# присоединение к семье по коду
@router.post("/join")
async def join_family(invite_code: str, user_id: int):
    family = await db.get_family_by_invite_code(invite_code)
    if family:
        user = await db.check_membership_by_user_id(user_id)
        if user and user['family_id'] == family['id']:
            return {
                "status": "ERR: user is already in this family",
            }
        elif user and user['family_id'] != family['id']:
            return {
                "status": "ERR: user is in another family",
            }
        else:
            await db.add_member(user_id, family['id'], 'child')
            return {
                "status": "member added",
                "family_id": family['id'],
                "invite_code": family['invite_code'],
            }
    else:
        return {
            "status": "ERR: wrong invite code",
        }


# выход из семьи
@router.post("/leave")
async def leave_family(user_id: int):
    await db.delete_member(user_id)
    return {
        "status": "member deleted",
        "user_id": user_id,
    }


# получение данных семьи по коду
@router.get("/get-by-code")
async def get_family_by_code(invite_code: str):
    family = await db.get_family_by_code(invite_code)
    if family:
        return {
            "id": family['id'],
            "name": family['name'],
            "invite_code": family['invite_code']
        }
    raise HTTPException(status_code=404, detail="Family not found")
#поменять роль