from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated, Any
from backend import auth, db, exceptions
from datetime import datetime

class UserIn(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=32)]
    password: Annotated[str, Field(min_length=8)]

class UserOut(BaseModel):
    username: str


app = FastAPI()

@app.get("/health")
async def root():
    return {"message": "ok"}

@app.post("/register", response_model= UserOut)
async def create_user(user: UserIn) -> Any:
    hashed_password = auth.hash_password(user.password)
    created_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    db.startup_database()
    db.create_user_database(user.username, hashed_password, created_at)
    return user

@app.post("/login", response_model=UserOut)
async def login(user: UserIn) -> Any:
    db.startup_database()
    if user.username == db.get_user_by_username(user.username):
        if auth.verify_password(user.password, db.get_password_by_username(user.username)):
            db.create_session(user.username)
            print("You are logged in!")
        else:
            exceptions.InvalidPasswordError("Wrong password")
    else:
        exceptions.UserNotFoundError("Username do not exist")
    return user

