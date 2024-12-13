import os
import csv
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.utils.file_operations import save_large_file
from app.utils.data_validation import validate_csv_headers
from app.utils.cleanup import cleanup_temp_files

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload a CSV file."""
    temp_dir = os.getenv("TEMP_DIR", "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # Cleanup old files
    cleanup_temp_files(temp_dir)

    # Restrict file size
    MAX_FILE_SIZE_MB = 25
    file_size = len(await file.read())
    await file.seek(0)
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File is too large. Maximum size is {MAX_FILE_SIZE_MB}MB.")

    # Ensure the file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .csv files are allowed.")

    # Save the file in chunks
    file_path = os.path.join(temp_dir, file.filename)
    await save_large_file(file, file_path)

    # Validate the CSV structure
    if not validate_csv_headers(file_path):
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Invalid CSV headers. Please upload the correct file.")

    return {"message": "File uploaded successfully", "file_path": file_path}
