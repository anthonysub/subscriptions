import strawberry

@strawberry.input
class UserInput:
    id: int
    name: str
    email: str
    puesto: str
    antiguedad: str
    area: str
