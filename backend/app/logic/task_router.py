from fastapi import APIRouter
from ..database import db 

router = APIRouter(prefix="/task", tags=["task"])

#Создание задачи: теперь берём ID сразу из create_task, без поиска по названию
@router.post("/add_task")
async def add_task(from_id: int, to_id: int, title: str, description: str):
    from_user = await db.check_membership_by_user_id(from_id)
    if not from_user:
        return {"status": "ERR: user not in family"}

    family_id = from_user['family_id']

    if len(title) > 255:
        return {"status": "ERR: title too long"}
    if len(description) > 255:
        return {"status": "ERR: description too long"}

    # create_task уже возвращает ID новой задачи (RETURNING id)
    new_task_id = await db.create_task(family_id, from_id, title, description)

    # Назначаем исполнителя, если он выбран (0 или пусто = не назначено)
    if to_id and to_id != 0:
        await db.assign_task(new_task_id, to_id)

    return {
        "status": "task_assigned",
        "task_id": new_task_id,
        "creator_id": from_id,
        "assigned_to_id": to_id
    }

#Удаление задачи
@router.post("/delete_task")
async def delete_task(task_id: int):
    await db.delete_task(task_id)
    return {"status": "task_deleted", "task_id": task_id}

#получение задач: ОДИН запрос возвращает массив готовых объектов с именами
@router.get("/get_family_tasks")
async def get_family_tasks(user_id: int):
    user = await db.check_membership_by_user_id(user_id)
    if not user:
        return {"status": "ERR: user not in family"}

    family_id = user['family_id']
    
    # Получаем все задачи семьи
    tasks = await db.get_family_tasks(family_id)
    # Получаем всех участников для ID -> Имя
    members = await db.get_family_members(family_id)
    
    name_map = {m['user_id']: m['name'] for m in members}

    enriched_tasks = []
    for t in tasks:
        enriched_tasks.append({
            "task_id": t['id'],
            "title": t['title'],
            "description": t['description'],
            "status": t['status'],
            "creator_name": name_map.get(t['creator_id'], 'Пользователь'),
            "assignee_name": name_map.get(t['assigned_to'], 'Не назначено') if t['assigned_to'] else 'Не назначено',
            "assigned_to_id": t['assigned_to']
        })

    return {"tasks": enriched_tasks}