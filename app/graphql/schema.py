import strawberry
from typing import Sequence

from app.graphql.user_types import UserType
from app.graphql.resolvers import resolve_users, resolve_user
from app.graphql.mutations import Mutation

#  IMPORTAR LA SUSCRIPCIÓN
from app.graphql.mutations import Subscription 

@strawberry.type
class Query:
    users: Sequence[UserType] = strawberry.field(resolver=resolve_users)
    user: UserType | None = strawberry.field(resolver=resolve_user)

#  2. AGREGAR AL ESQUEMA
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription  # <--- ¡La pieza faltante!
)