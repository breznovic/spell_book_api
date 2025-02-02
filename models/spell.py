from pydantic import BaseModel

class Spell(BaseModel):
    id: int
    name: str
    level: int
    school: str
    description: str
