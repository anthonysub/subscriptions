from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.sqlalchemy import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    puesto: Mapped[str] = mapped_column(String(100), nullable=False)
    antiguedad: Mapped[str] = mapped_column(String(50), nullable=False)
    area: Mapped[str] = mapped_column(String(100), nullable=False)







"""from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    puesto: str
    antiguedad: str
    area: str"""