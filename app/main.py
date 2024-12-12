from fastapi import FastAPI
from app.routes import upload
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Climate Data Backend :)"}

app.include_router(upload.router, prefix="/api")