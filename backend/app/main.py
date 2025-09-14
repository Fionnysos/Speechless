from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated, Any
from backend import auth, db
from datetime import datetime, timezone


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
    now_utc = datetime.now().replace(microsecond=0)
    db.startup_database()
    db.create_user_database(user.username, hashed_password, now_utc)
    return user
