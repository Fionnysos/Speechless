from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated, Any

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
    return user
