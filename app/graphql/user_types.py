import strawberry
from strawberry.experimental.pydantic import type as pydantic_type
from app.schemas.user import UserSchema

@pydantic_type(model=UserSchema, all_fields=True)
class UserType:
    pass
