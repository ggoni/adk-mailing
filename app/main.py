from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Smart Marketing Agent API", version="1.0.0")

app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Marketing Agent API"}
