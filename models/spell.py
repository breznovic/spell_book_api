from pydantic import BaseModel
from typing import Optional


class Spell(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    level: int
    school: str
    image_url: Optional[str] = None
