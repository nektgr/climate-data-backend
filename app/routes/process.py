import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from app.utils.data_validation import validate_csv_columns
from app.utils.exceptions import file_not_found_error, invalid_csv_error
from app.utils.csv_processing import calculate_monthly_averages, calculate_yearly_statistics
from app.config import config
import logging

# Set up logger
logger = logging.getLogger("app.routes.process")

router = APIRouter()

@router.get("/process/")
def process_file(file_name: str):
    """Endpoint to process the uploaded CSV file."""
    file_path = os.path.join(config.TEMP_DIR, file_name)

    # Ensure the file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise file_not_found_error()

    try:
        # Load the CSV into a DataFrame
        df = pd.read_csv(file_path)
        logger.info(f"File loaded successfully: {file_path}")

        # Validate the columns
        if not validate_csv_columns(df):
            logger.error(f"Invalid CSV structure: {file_path}")
            raise invalid_csv_error()

        # Replace invalid values with NaN
        df.replace([float('inf'), -float('inf')], pd.NA, inplace=True)

        # Compute monthly averages
        monthly_columns = df.columns[3:15]
        monthly_averages = df[monthly_columns].mean()

        # Fill missing values with the respective monthly averages
        for col in monthly_columns:
            df.loc[:, col] = df[col].fillna(monthly_averages[col])
            logger.debug(f"Filled missing values in column {col} with average {monthly_averages[col]}")

        # Recalculate yearly data
        df = calculate_monthly_averages(df)
        df = calculate_yearly_statistics(df)

        logger.info(f"File processed successfully: {file_name}")

        # Prepare the response
        response = {
            "yearly_averages": df["Yearly Average"].tolist(),
            "yearly_stddev": df["Yearly StdDev"].tolist(),
            "years": df["Year"].tolist(),
            "monthly_data": df[monthly_columns].to_dict(orient="list"),
        }
        return response

    except Exception as e:
        logger.error(f"Unexpected error while processing file {file_name}: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
