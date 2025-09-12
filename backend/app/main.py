from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def root():
    return {"message": "ok"}

@app.get("/docs")
async def root():
    return {"message": "ok"}