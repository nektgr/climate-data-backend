from fastapi import FastAPI
from app.routes import upload
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Climate Data Backend"}

app.include_router(upload.router, prefix="/api")