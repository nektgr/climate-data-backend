import csv
import os
from fastapi import APIRouter, HTTPException, UploadFile, File

router = APIRouter()

@router.post("/api/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Ensure the file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .csv files are allowed.")
    
    # Save the file to a temporary directory
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Validate the CSV structure
    required_headers = [
        "Product code", "Station Number", "Year",
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Annual"
    ]

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        if headers != required_headers:
            raise HTTPException(status_code=400, detail="Invalid CSV headers. Please upload the correct file.")

    return {"message": "File uploaded successfully", "file_path": file_path}
