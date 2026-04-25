from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.sqlalchemy import SessionLocal
from app.models.user import User
from app.schemas.user import UserSchema

router = APIRouter()


# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET ALL USERS
@router.get("/users", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# CREATE USER
@router.post("/users", response_model=UserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_user = User(
        id=user.id,
        name=user.name,
        email=user.email,
        puesto=user.puesto,
        antiguedad=user.antiguedad,
        area=user.area
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET USER BY ID
@router.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# DELETE USER
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}
