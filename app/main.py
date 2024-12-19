from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, process
from app.utils.cleanup import cleanup_temp_files
from app.config import config

# Configure logging based on config
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(config.APP_NAME)

# Define lifespan with cleanup logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context for FastAPI with startup and shutdown logic.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Indicates startup logic is complete.
    """
    try:
        logger.info("Application is starting up...")
        logger.info("Cleaning up temp files...")
        cleanup_temp_files(config.TEMP_DIR, max_age_seconds=config.FILE_MAX_AGE_SECONDS)
        yield
    finally:
        logger.info("Application is shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    debug=config.DEBUG,
    lifespan=lifespan,
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOWED_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS,
)

@app.get("/")
async def read_root():
    """
    Root endpoint for health check.

    Returns:
        dict: A message indicating the API is running.
    """
    return {
        "message": "Welcome to the Climate Data Backend :)",
        "app_name": config.APP_NAME,
        "version": config.VERSION,
        "status": "Running",
    }

# Include routes from the routes module
app.include_router(upload.router, prefix="/api")
app.include_router(process.router, prefix="/api")
