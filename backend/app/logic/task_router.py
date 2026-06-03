from fastapi import APIRouter
from database import db 

router = APIRouter(prefix="/task", tags=["task"])

@router.post("/add_task")
async def add_task(from_id: int, to_id: int, title: str, description: str = ""):
    # from_id и to_id - строго внутренние ID базы данных (user_id)
    from_user = await db.check_membership_by_user_id(from_id)
    if not from_user:
        return {"status": "ERR: user not in family"}

    family_id = from_user['family_id']

    if len(title) > 255 or len(description) > 255:
        return {"status": "ERR: data too long"}

    new_task_id = await db.create_task(family_id, from_id, title, description)

    if to_id and to_id != 0:
        await db.assign_task(new_task_id, to_id)

    return {"status": "task_assigned", "task_id": new_task_id}

@router.post("/delete_task")
async def delete_task(task_id: int):
    await db.delete_task(task_id)
    return {"status": "task_deleted", "task_id": task_id}

@router.get("/get_family_tasks")
async def get_family_tasks(user_id: int):
    # user_id - строго внутренний ID
    user = await db.check_membership_by_user_id(user_id)
    if not user:
        return {"status": "ERR: user not in family"}

    family_id = user['family_id']
    tasks = await db.get_family_tasks(family_id)
    members = await db.get_family_members(family_id)
    
    name_map = {m['user_id']: m['name'] for m in members}

    enriched_tasks = []
    for t in tasks:
        enriched_tasks.append({
            "task_id": t['id'],
            "title": t['title'],
            "description": t.get('description', ''),
            "status": t.get('status', 'new'),
            "creator_name": name_map.get(t['creator_id'], "Неизвестный"),
            "assignee_name": name_map.get(t['assigned_to'], "Не назначено") if t['assigned_to'] else "Не назначено",
            "assigned_to_id": t['assigned_to'] # Оставляем внутренний ID для корректной фильтрации на фронте
        })

    return {"tasks": enriched_tasks}
