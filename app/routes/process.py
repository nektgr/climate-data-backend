import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from app.utils.data_validation import validate_csv_columns

router = APIRouter()

@router.get("/process/")
def process_file(file_name: str):
    """Endpoint to process the uploaded CSV file."""
    temp_dir = os.getenv("TEMP_DIR", "temp")
    file_path = os.path.join(temp_dir, file_name)

    # Ensure the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    # Load the CSV into a DataFrame
    df = pd.read_csv(file_path)

    # Validate the columns
    if not validate_csv_columns(df):
        raise HTTPException(status_code=400, detail="Invalid CSV structure.")

    # Replace invalid values with NaN
    df.replace([float('inf'), -float('inf')], pd.NA, inplace=True)

    # Compute monthly averages
    monthly_columns = df.columns[3:15]
    monthly_averages = df[monthly_columns].mean()

    # Fill missing values with the respective monthly averages
    for col in monthly_columns:
        df[col].fillna(monthly_averages[col], inplace=True)

    # Recalculate yearly data
    df["Yearly Average"] = df[monthly_columns].mean(axis=1)
    df["Yearly StdDev"] = df[monthly_columns].std(axis=1)

    # Prepare the response
    response = {
        "yearly_averages": df["Yearly Average"].tolist(),
        "yearly_stddev": df["Yearly StdDev"].tolist(),
        "years": df["Year"].tolist(),
        "monthly_data": df[monthly_columns].to_dict(orient="list"),
    }
    return response
