from pydantic import BaseModel

class MemberAdd(BaseModel):
    user_id: int
    family_id: int
    role: str  # 'owner' | 'parent' | 'child'
