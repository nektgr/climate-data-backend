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

# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    debug=config.DEBUG
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOWED_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS,
)

@app.on_event("startup")
def on_startup():
    """Startup event to perform initial setup tasks."""
    logger.info("Application is starting up...")
    logger.info("Cleaning up temp files...")
    cleanup_temp_files(config.TEMP_DIR, max_age_seconds=config.FILE_MAX_AGE_SECONDS)

@app.on_event("shutdown")
def on_shutdown():
    """Shutdown event to perform cleanup tasks."""
    logger.info("Application is shutting down...")

@app.get("/")
async def read_root():
    """Root endpoint for health check."""
    return {
        "message": "Welcome to the Climate Data Backend :)",
        "app_name": config.APP_NAME,
        "version": config.VERSION,
        "status": "Running"
    }

# Include routes from the routes module
app.include_router(upload.router, prefix="/api")
app.include_router(process.router, prefix="/api")
