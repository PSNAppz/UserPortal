from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional
from . import crud, models, schemas, database
import os
import shutil

app = FastAPI()

# Uncomment the below code to create the tables in the database for
# the first time the application is run

# from .database import engine
# from . import models

# models.Base.metadata.create_all(bind=engine)


# Dependency to get the DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ensure the directory for profile pictures exists
profile_pictures_directory = "static/profile_pictures"
os.makedirs(profile_pictures_directory, exist_ok=True)


@app.post("/register/")
async def register_user(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    profile_picture: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    # Check if email or phone already exists
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_phone(db, phone=phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone already registered")

    # Create new user with the provided data
    user_data = {
        "full_name": full_name,
        "email": email,
        "password": password,
        "phone": phone,
    }
    new_user = crud.create_user(db=db, user=schemas.UserCreate(**user_data))

    # Handle profile picture after creating the user
    if profile_picture:
        # Define the full path where the profile picture will be saved
        profile_pic_filename = f"{new_user.id}_{profile_picture.filename}"
        profile_pic_path = os.path.join(
            profile_pictures_directory, profile_pic_filename
        )

        # Save profile picture to disk (Can be replaced with cloud storage)
        with open(profile_pic_path, "wb") as buffer:
            shutil.copyfileobj(profile_picture.file, buffer)
        profile_picture.file.close()

        # Update MongoDB with the path of the saved profile picture
        profile_collection = database.mongodb["profiles"]
        profile_collection.insert_one(
            {
                "user_id": str(new_user.id),  # Storing the user ID as a string
                "profile_picture_path": profile_pic_path,
            }
        )

    return {"user_id": new_user.id, "message": "User registered successfully"}


@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch the profile picture path from MongoDB if it exists
    profile_collection = database.mongodb["profiles"]
    profile_info = profile_collection.find_one({"user_id": str(user_id)})
    profile_picture_path = (
        profile_info.get("profile_picture_path") if profile_info else None
    )

    # Make sure the response includes all the fields defined in the response model
    return {
        "id": db_user.id,
        "full_name": db_user.full_name,
        "email": db_user.email,
        "phone": db_user.phone,
        "profile_picture_path": profile_picture_path,
    }
