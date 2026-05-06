# как принимать данные с фронтенда
from pydantic import BaseModel

class UserCreate(BaseModel):
    vk_id: int
    name: str

class UserOut(BaseModel):
    id: int
    vk_id: int
    name: str
