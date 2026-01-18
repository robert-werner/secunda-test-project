from pydantic import BaseModel
from app.schemas.common import BaseRead
from app.schemas.building import BuildingRead
from app.schemas.activity import ActivitySimple

class PhoneRead(BaseRead):
    id: int
    phone: str

class OrganizationBase(BaseModel):
    name: str

class OrganizationList(OrganizationBase, BaseRead):
    id: int
    building: BuildingRead

class OrganizationRead(OrganizationList):
    phones: list[PhoneRead] = []
    activities: list[ActivitySimple] = []
