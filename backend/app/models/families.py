from pydantic import BaseModel

class FamilyCreate(BaseModel):
    name: str
    invite_code: str

class FamilyOut(BaseModel):
    id: int
    name: str
    invite_code: str
