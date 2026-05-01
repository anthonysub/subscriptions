import strawberry
from app.models.user import User
from app.schemas.user import UserSchema
from app.graphql.user_types import UserType
from app.graphql.user_inputs import UserInput
from app.database.sqlalchemy import get_db

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_user(self, data: UserInput) -> UserType:
        db = next(get_db())

        new_user = User(
            id=data.id,
            name=data.name,
            email=data.email,
            puesto=data.puesto,
            antiguedad=data.antiguedad,
            area=data.area
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return UserType.from_pydantic(UserSchema.model_validate(new_user))

    @strawberry.mutation
    def update_user(self, id: int, data: UserInput) -> UserType:
        db = next(get_db())

        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise Exception("User not found")

        user.name = data.name
        user.email = data.email
        user.puesto = data.puesto
        user.antiguedad = data.antiguedad
        user.area = data.area

        db.commit()
        db.refresh(user)

        return UserType.from_pydantic(UserSchema.model_validate(user))

    @strawberry.mutation
    def delete_user(self, id: int) -> bool:
        db = next(get_db())

        user = db.query(User).filter(User.id == id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()

        return True
