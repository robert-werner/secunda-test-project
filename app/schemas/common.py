from pydantic import BaseModel, ConfigDict

class BaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
