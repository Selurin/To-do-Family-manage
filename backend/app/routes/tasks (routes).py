from fastapi import APIRouter
from ..models.tasks import TaskCreate, TaskAssign
from ..main import db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("")
async def create_task(data: TaskCreate):
    task_id = await db.create_task(
        data.family_id,
        data.creator_id,
        data.title,
        data.description,
    )
    return {"id": task_id}

@router.post("/assign")
async def assign_task(data: TaskAssign):
    await db.assign_task(data.task_id, data.user_id)
    return {"status": "ok"}

@router.get("/family/{family_id}")
async def get_family_tasks(family_id: int):
    rows = await db.get_family_tasks(family_id)
    return [dict(r) for r in rows]
