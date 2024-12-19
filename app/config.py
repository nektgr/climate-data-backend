import os

class Config:
    """
    Configuration class for the Climate Data API.
    """
    # General Settings
    APP_NAME = "Climate Data API"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # File Handling
    TEMP_DIR = os.getenv("TEMP_DIR", "temp")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 25))
    ALLOWED_EXTENSIONS = [".csv"]

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # CORS Settings
    CORS_ALLOWED_ORIGINS = os.getenv(
        "CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

    # Cleanup Settings
    FILE_MAX_AGE_SECONDS = int(os.getenv("FILE_MAX_AGE_SECONDS", 3600))

# Instantiate the configuration
config = Config()
