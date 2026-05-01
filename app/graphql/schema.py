import strawberry
from typing import Sequence

from app.graphql.user_types import UserType
from app.graphql.resolvers import resolve_users, resolve_user
from app.graphql.mutations import Mutation

# 👇 1. IMPORTAR LA SUSCRIPCIÓN
# (Asegúrate de poner la ruta correcta de donde guardaste tu clase Subscription. 
# Si la pusiste en el mismo archivo que las mutaciones, impórtala desde ahí).
from app.graphql.mutations import Subscription 

@strawberry.type
class Query:
    users: Sequence[UserType] = strawberry.field(resolver=resolve_users)
    user: UserType | None = strawberry.field(resolver=resolve_user)

# 👇 2. AGREGARLA AL ESQUEMA
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription  # <--- ¡La pieza faltante!
)