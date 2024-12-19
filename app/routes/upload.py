import os
from fastapi import APIRouter, UploadFile, File
from app.utils.file_operations import save_large_file
from app.utils.data_validation import validate_csv_headers
from app.utils.cleanup import cleanup_temp_files
from app.utils.exceptions import (
    file_not_found_error,
    invalid_csv_error,
    file_too_large_error,
    invalid_file_type_error,
    file_save_error,
    cleanup_error,
    csv_validation_error,
)
import logging
from app.config import config
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload a CSV file."""
    try:   
        os.makedirs(config.TEMP_DIR, exist_ok=True)

        # Cleanup old files
        try:
            cleanup_temp_files(config.TEMP_DIR)
        except Exception as e:  
            logger.error(f"Error cleaning up temporary files: {e}")
            raise cleanup_error()


        try:
            file_size = len(await file.read())
            await file.seek(0)
        except Exception as e:
            logger.error(f"Error reading file size: {e}")
            raise invalid_csv_error()

        if file_size > config.MAX_FILE_SIZE_MB * 1024 * 1024:
            logger.warning(f"File size exceeds limit: {file_size / (1024 * 1024):.2f} MB")
            raise file_too_large_error(config.MAX_FILE_SIZE_MB)

        # Ensure the file is a CSV
        if not any(file.filename.endswith(ext) for ext in config.ALLOWED_EXTENSIONS):
            logger.warning(f"Invalid file type uploaded: {file.filename} Allowed extensions: {', '.join(config.ALLOWED_EXTENSIONS)}")
            raise invalid_file_type_error()

        # Save the file in chunks
        file_path = os.path.join(config.TEMP_DIR, file.filename)
        try:
            await save_large_file(file, file_path)
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise file_save_error()

        # Validate the CSV structure
        try:
            if not validate_csv_headers(file_path):
                os.remove(file_path)
                logger.warning("CSV validation failed. File removed.")
                raise invalid_csv_error()
        except Exception as e:
            logger.error(f"Error validating CSV headers: {e}")
            raise csv_validation_error()

        logger.info(f"File uploaded successfully: {file.filename}")
        return {"message": "File uploaded successfully", "file_path": file_path}

    except HTTPException as http_exc:
        # Reraise HTTP exceptions as-is for structured client errors
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error in upload_file: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
