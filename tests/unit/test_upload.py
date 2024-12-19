import os
from fastapi import status
from app.config import config

def test_upload_valid_file(client):
    """
    Test uploading a valid CSV file.

    Args:
        client: Test client for making API requests.
    """
    # Prepare valid CSV content
    csv_content = "Product code,Station Number,Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,Annual\n"
    csv_content += "ABC123,12345,2024,1,2,3,4,5,6,7,8,9,10,11,12,78\n"
    files = {"file": ("test.csv", csv_content)}

    # Upload the file
    response = client.post("/api/upload/", files=files)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "File uploaded successfully"

def test_upload_invalid_file(client):
    """
    Test uploading an invalid file type.

    Args:
        client: Test client for making API requests.
    """
    # Prepare invalid file content
    files = {"file": ("test.txt", "This is not a CSV file.")}

    # Upload the file
    response = client.post("/api/upload/", files=files)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type. Only .csv files are allowed."

def test_upload_large_file(client):
    """
    Test uploading a file that exceeds the size limit.

    Args:
        client: Test client for making API requests.
    """
    # Prepare large file content
    large_file_content = "A" * (config.MAX_FILE_SIZE_MB * 1024 * 1024 + 1)
    files = {"file": ("large.csv", large_file_content)}

    # Upload the file
    response = client.post("/api/upload/", files=files)
    assert response.status_code == 400
    assert response.json()["detail"] == f"File is too large. Maximum size is {config.MAX_FILE_SIZE_MB}MB."