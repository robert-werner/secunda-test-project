from pydantic import BaseModel
from app.schemas.common import BaseRead

class BuildingBase(BaseModel):
    address: str
    lat: float | None = None
    lon: float | None = None

class BuildingRead(BuildingBase, BaseRead):
    id: int
