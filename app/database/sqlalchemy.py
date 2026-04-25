from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cambia users_db por el nombre de tu base si es diferente
DATABASE_URL = "mysql+pymysql://root:@localhost/users_db"

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
