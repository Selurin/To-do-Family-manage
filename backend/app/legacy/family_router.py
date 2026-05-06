from fastapi import APIRouter, HTTPException
from watchfiles import awatch

from database import db
from datetime import datetime, timedelta
from collections import defaultdict
import random
import string

router = APIRouter(prefix="/family", tags=["family"])

#создание семьи
@router.post("/create")
async def create_family(name: str, user_id: int):
    #ограничение на длину имени
    if len(name) > 45:
        return {"error": "name too long"}
    else:
        #функция для генерации кода приглашения
        def code_generator():
            chars = string.ascii_letters + string.digits
            code = ''.join(random.choice(chars) for i in range(10))

            if db.get_family_by_invite_code(code):
                return code_generator()
            else:
                return code

        #генерация кода и создание семьи
        invite_code = await code_generator()

        await db.create_family(name, invite_code)
        #добавление создателя семьи в... семью
        family = await db.get_family_by_code(invite_code)
        family_id = family['id']

        await db.add_member(user_id, family_id, 'owner')

        return {
            "status": "family created",
            "invite_code": family['invite_code'],
            "family_id": family_id,
            "name": family['name'],
        }

#присоединение к семье по коду
@router.post("/join")
async def join_family(invite_code: str, user_id: int):
    family = await db.get_family_by_invite_code(invite_code)
    #проверка на существования кода
    if family:
        #проверка на то что пользователь не состоит в семье
        user = await db.check_membership_by_user_id(user_id)
        if user and user['family_id'] == family['id']:
            return {
                "status": "ERR: user is already in this family",
            }
        elif user and user['family_id'] != family['id']:
            return {
                "status": "ERR: user is in another family",
            }
        #добавление
        else:
            await db.add_member(user_id, family['invite_code'], 'child')
            return {
                "status": "member added",
            }
    else:
        return {
            "status": "ERR: wrong invite code",
        }

#выйти\удалить члена семьи
@router.post("/leave")
async def leave_family(user_id: int):
    await db.delete_member(user_id)
    return {
        "status": "member deleted",
        "user_id": user_id,
    }

#поменять роль