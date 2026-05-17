from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    family_id: int
    creator_id: int
    title: str
    description: Optional[str] = None

class TaskAssign(BaseModel):
    task_id: int
    user_id: int
