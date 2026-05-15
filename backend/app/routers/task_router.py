from fastapi import APIRouter, HTTPException
from starlette import status

from database import db
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter(prefix="/task", tags=["task"])

#добавление заданий
@router.post("/add_task")
async def add_task(from_id: int, to_id: int, title: str, description: str):
    #используем семью автрора
    from_user = await db.check_membership_by_user_id(from_id)
    family_id = from_user['family_id']

    #проверяем длину
    if len(title) > 100:
        return {
            "status": "ERR: title too long",
        }
    if len(description) > 1000:
        return {
            "status": "ERR: description too long",
        }

    #создаём задание
    await db.create_task(family_id, from_id, title, description)
    task = await db.get_task_by_title(title)
    #предписываем задание
    await db.assign_task(task['id'], to_id)
    return {
        "status": "task assigned",
        "task_id": task['id'],
        "family_id": family_id,
        "creator_id": from_user['user_id'],
        "assigned_to_id": to_id,
    }

#удаление задачи из бд
@router.post("/delete_task")
async def delete_task(task_id: int):
    await db.delete_task(task_id)
    return {
        "status": "task deleted",
        "task_id": task_id,
    }

#получение всех задач семьи по пользователю
@router.get("/get_family_tasks")
async def get_family_tasks(user_id: int):
    user = await db.check_membership_by_user_id(user_id)
    family_id = user['family_id']
    task_ids = await db.get_family_task_ids(family_id)
    return {
        "family_id": family_id,
        "task_ids": task_ids,
        "count": len(task_ids),
    }

#получение всех задач пользователя
@router.get("/get_user_tasks")
async def get_user_tasks(user_id: int):
    task_ids = await db.get_user_task_ids(user_id)
    return {
        "user_id": user_id,
        "task_ids": task_ids,
        "count": len(task_ids),
    }

#получение задания по ид
@router.get("/get_task_by_id")
async def get_task_by_id(task_id: int):
    task = await db.get_task_by_id(task_id)
    return {
        "task_id": task['id'],
        "family_id": task['family_id'],
        "creator_id": task['creator_id'],
        "assigned_to_id": task['assigned_to'],
        "title": task['title'],
        "description": task['description'],
        "status": task['status'],
    }

