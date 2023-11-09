from sqlalchemy.orm import Session
from . import models, schemas, database


# CRUD for PostgreSQL
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=fake_hashed_password,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# CRUD for MongoDB
def store_profile_picture(user_id: int, profile_picture_content: bytes):
    profile_collection = database.mongodb["profiles"]
    profile_collection.insert_one(
        {
            "user_id": user_id,
            "profile_picture": profile_picture_content,  # Storing binary data
        }
    )
