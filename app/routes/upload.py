import csv
import os
from fastapi import APIRouter, HTTPException, UploadFile, File
import numpy as np
import pandas as pd

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

@router.get("/api/process/")
def process_file(file_name: str):
    file_path = os.path.join("temp", file_name)
    
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    # Load the CSV into a DataFrame
    df = pd.read_csv(file_path)

    # Validate the columns match the expected structure
    required_columns = [
        "Product code", "Station Number", "Year",
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Annual"
    ]
    if list(df.columns) != required_columns:
        raise HTTPException(status_code=400, detail="Invalid CSV structure.")

    # Handle missing or invalid data
    df.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace infinite values with NaN
    df.fillna(0, inplace=True)  # Replace NaN with 0 or another appropriate default

    # Extract and compute yearly data
    df["Yearly Average"] = df.iloc[:, 3:15].mean(axis=1)
    df["Yearly StdDev"] = df.iloc[:, 3:15].std(axis=1)

    # Prepare the response, ensuring JSON-safe values
    response = {
        "yearly_averages": df["Yearly Average"].fillna(0).replace({np.nan: 0}).tolist(),
        "yearly_stddev": df["Yearly StdDev"].fillna(0).replace({np.nan: 0}).tolist(),
        "years": df["Year"].tolist(),
        "monthly_data": df.iloc[:, 3:15].fillna(0).replace({np.nan: 0}).to_dict(orient="list")
    }
    return response
