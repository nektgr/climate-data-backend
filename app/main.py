import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, process
from app.utils.cleanup import cleanup_temp_files
import logging
logger = logging.getLogger(__name__)
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def on_startup():
    temp_dir = os.getenv("TEMP_DIR", "temp")
    logger.info("Cleaning up temp files...")
    cleanup_temp_files(temp_dir)


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Climate Data Backend :)",
        "version": "1.0.0",
        "status": "Running"
    }


# Include routes
app.include_router(upload.router, prefix="/api")
app.include_router(process.router, prefix="/api")
