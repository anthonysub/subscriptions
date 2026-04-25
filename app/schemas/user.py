from pydantic import BaseModel, ConfigDict

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    puesto: str
    antiguedad: str
    area: str

    model_config = ConfigDict(from_attributes=True)
