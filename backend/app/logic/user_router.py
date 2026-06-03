from fastapi import APIRouter, HTTPException
from database import db
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter(prefix="/user", tags=["user"])

# вход пользователя в приложение. Возвращает данные о пользователе, если он уже зарегестрирован в бд,
# либо регистрирует его, если он не бд
@router.post("/register")
async def register(vk_id: int, name: str):
    is_in_db = await db.get_user_by_vk_id(vk_id)
    if is_in_db:
        # Убираем "Пользователь XX", если фронт прислал нормальное имя
        if is_in_db['name'] != name and not is_in_db['name'].startswith(name):
            await db.update_user_name(vk_id, name)
            is_in_db = await db.get_user_by_vk_id(vk_id) 

        return {
            "status": "already_exist",
            "id": is_in_db['id'],
            "vk_id": is_in_db['vk_id'],
            "name": is_in_db['name']
        }
    else:
        await db.create_user(vk_id, name)
        db_answer = await db.get_user_by_vk_id(vk_id)
        return {
            "status": "user_created",
            "id": db_answer['id'],
            "vk_id": db_answer['vk_id'],
            "name": db_answer['name']
        }

@router.get("/load_user_family")
async def load_users_family(vk_id: int):
    user = await db.get_user_by_vk_id(vk_id)
    if not user:
        return {"status": "ERR: invalid_user"}

    user_id = user['id']
    has_family = await db.check_membership_by_user_id(user_id)
    
    if has_family:
        family_id = has_family['family_id']
        family_data = await db.get_family_by_id(family_id)
        
        return {
            "status": "family_found",
            "vk_id": vk_id,
            "user_id": user_id,
            "family_id": family_id,
            "invite_code": family_data['invite_code'] if family_data else None,
            "family_name": family_data['name'] if family_data else "Семья"
        }
    else:
        return {
            "status": "family_not_found",
            "vk_id": vk_id,
            "user_id": user_id
        }
        
# поиск бд-шнего айди юзера
@router.get("/get_user_id")
async def get_user_id(vk_id: int):
    user = await db.get_user_by_vk_id(vk_id)
    if user:
        user_id = user['id']
        return {
            "status": "success",
            "user_id" : user_id
        }
    else:
        return {
            "status": "ERR: invalid_user",
        }

