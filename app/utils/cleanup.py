import os
import time
import logging
from app.config import config
logger = logging.getLogger(__name__)

def cleanup_temp_files(directory: str, max_age_seconds: int = config.FILE_MAX_AGE_SECONDS):
    """Remove files older than `max_age_seconds` in the specified directory."""
    current_time = time.time()
    if not os.path.exists(directory):
        logger.info(f"Directory {directory} does not exist. Skipping cleanup.")
        return
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)
                logger.info(f"Deleted old file: {file_path}")
