import os
from fastapi import status
from app.config import config

def test_process_valid_file(client):
    """
    Test processing a valid uploaded CSV file.

    Args:
        client: Test client for making API requests.
    """
    # Prepare CSV content
    csv_content = "Product code,Station Number,Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,Annual\n"
    csv_content += "ABC123,12345,2024,1,2,3,4,5,6,7,8,9,10,11,12,78\n"
    files = {"file": ("test.csv", csv_content)}

    # Upload the file
    upload_response = client.post("/api/upload/", files=files)
    assert upload_response.status_code == status.HTTP_200_OK

    # Extract file name
    file_path = upload_response.json()["file_path"]
    file_name = os.path.basename(file_path)

    # Process the file
    process_response = client.get(f"/api/process/?file_name={file_name}")
    assert process_response.status_code == status.HTTP_200_OK

    # Validate response content
    response_data = process_response.json()
    assert "yearly_averages" in response_data
    assert "yearly_stddev" in response_data
    assert "years" in response_data
    assert "monthly_data" in response_data


def test_process_nonexistent_file(client):
    """
    Test processing a non-existent file.

    Args:
        client: Test client for making API requests.
    """
    response = client.get("/api/process/?file_name=nonexistent.csv")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "File not found."
