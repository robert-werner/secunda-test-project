from pydantic import BaseModel
from app.schemas.common import BaseRead

class ActivityBase(BaseModel):
    name: str
    level: int
    parent_id: int | None = None

class ActivityRead(ActivityBase, BaseRead):
    id: int
    children: list["ActivityRead"] = []

class ActivitySimple(ActivityBase, BaseRead):
    id: int
