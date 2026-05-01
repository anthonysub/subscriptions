import strawberry
from app.models.user import User
from app.schemas.user import UserSchema
from app.graphql.user_types import UserType
from app.graphql.user_inputs import UserInput
from app.database.sqlalchemy import get_db
from typing import AsyncGenerator
from app.pubsub import broker

# 1. Definimos cómo se verá la alerta en la pantalla de GraphQL
@strawberry.type
class UserEvent:
    evento: str   # Aquí dirá "CREACION", "MODIFICACION" o "ELIMINACION"
    datos: str    # Aquí mandaremos la info del usuario

# 2. Creamos la Suscripción (El oyente)
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_events(self) -> AsyncGenerator[UserEvent, None]:
        """
        Esta función se queda "viva" escuchando el broker infinitamente.
        """
        async for mensaje in broker.subscribe():
            # Cuando llega un mensaje, lo formateamos y lo enviamos a la pantalla
            yield UserEvent(
                evento=mensaje["evento"],
                datos=str(mensaje["datos"])
            )

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_user(self, data: UserInput) -> UserType:
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
        await broker.publish("CREACION", new_user)

        return UserType.from_pydantic(UserSchema.model_validate(new_user))

    @strawberry.mutation
    async def update_user(self, id: int, data: UserInput) -> UserType:
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

        await broker.publish("MODIFICACION", user)
        return UserType.from_pydantic(UserSchema.model_validate(user))

    @strawberry.mutation
    async def delete_user(self, id: int) -> bool:
        db = next(get_db())

        user = db.query(User).filter(User.id == id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        await broker.publish("ELIMINACION", {"id": id})
        return True
# Me imagino que ya tienes tu clase Query por ahí, si no, crea una básica:
@strawberry.type
class Query:
    @strawberry.field
    def status(self) -> str:
        return "OK"

