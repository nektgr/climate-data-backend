import csv
import pandas as pd

REQUIRED_HEADERS = [
    "Product code", "Station Number", "Year",
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Annual"
]

def validate_csv_headers(file_path: str) -> bool:
    """Validate the headers of the uploaded CSV file."""
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        return headers == REQUIRED_HEADERS

def validate_csv_columns(df: pd.DataFrame) -> bool:
    """Validate the columns of the DataFrame."""
    return list(df.columns) == REQUIRED_HEADERS
