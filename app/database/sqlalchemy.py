from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cambia users_db por el nombre de tu base si es diferente
DATABASE_URL = "postgresql+psycopg2://postgres:12345678@localhost:5432/Usuarios"

# Crea el motor de conexión
engine = create_engine(
    DATABASE_URL,
    echo=True,      # Muestra el SQL en consola (útil para enseñar)
    future=True
)

# Crea la sesión para interactuar con la BD
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos ORM
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
