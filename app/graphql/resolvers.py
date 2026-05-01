from app.models.user import User
from app.schemas.user import UserSchema
from app.graphql.user_types import UserType
from app.database.sqlalchemy import get_db

def resolve_users():
    db = next(get_db())
    users = db.query(User).all()

    # Convertimos SQLAlchemy → Pydantic → GraphQL
    return [
        UserType.from_pydantic(UserSchema.model_validate(u))
        for u in users
    ]


def resolve_user(id: int):
    db = next(get_db())
    user = db.query(User).filter(User.id == id).first()

    if not user:
        return None

    return UserType.from_pydantic(UserSchema.model_validate(user))
