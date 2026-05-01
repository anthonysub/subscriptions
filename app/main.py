from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.routers import users
from app.database.sqlalchemy import engine, Base
from app.pubsub import broker

app = FastAPI()

#creacion de tablas 
Base.metadata.create_all(bind=engine)

# REST
app.include_router(users.router)

# GraphQL
graphql_app = GraphQLRouter(schema,
    subscription_protocols=["graphql-transport-ws", "graphql-ws"])

app.include_router(graphql_app, prefix="/graphql")


