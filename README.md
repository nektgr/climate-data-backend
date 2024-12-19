# Climate Data API

This project provides a FastAPI-based backend for uploading, processing, and analyzing climate data in CSV format. The API includes endpoints for uploading files, validating them, and generating statistics.

## Features

- **File Upload**: Upload CSV files containing climate data.
- **Data Validation**: Ensure the file structure is correct before processing.
- **Data Processing**: Generate monthly averages and yearly statistics.
- **Error Handling**: Comprehensive error responses for invalid file types, size limits, or processing errors.
- **CORS Support**: Enable communication with frontends hosted on different domains.

## Prerequisites

Ensure the following are installed on your system:

- Python 3.9+
- Virtual environment tool (e.g., `venv` or `virtualenv`)
- [Poetry](https://python-poetry.org/) or `pip` (for dependency management)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nektgr/climate-data-backend.git
   cd climate-data-backend
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   - Using `pip`:
     ```bash
     pip install -r requirements.txt
     ```

4. Configure application settings:
Edit the config.py file to adjust the following parameters as needed:  
   ```bash
   class Config:
    APP_NAME = "Climate Data API"
    DEBUG = False  # Set to True for development
    TEMP_DIR = "temp"  # Temporary file storage directory
    MAX_FILE_SIZE_MB = 25  # Maximum file upload size in MB
    LOG_LEVEL = "INFO"  # Logging level
    CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    FILE_MAX_AGE_SECONDS = 3600  # Maximum age for temporary files
   ```

## Running the Application

1. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Open your browser or API testing tool (e.g., Postman) and navigate to the FastAPI docs:
   ```
   http://127.0.0.1:8000/docs
   ```

## Testing

1. Install testing dependencies:
   ```bash
   pip install pytest
   ```

2. Run the tests:
   ```bash
   python -m pytest
   ```

## Project Structure

```plaintext
├── app
│   ├── main.py           # Entry point for the application
│   ├── config.py         # Configuration settings
│   ├── routes            # API route handlers
│   ├── utils             # Utility functions for processing and validation
├── tests
│   ├── test_upload_file.py   # Tests for the upload functionality
│   ├── test_process_file.py  # Tests for file processing
│   ├── test_client_setup.py  # Test client setup
├── requirements.txt      # Dependency list for pip
├── README.md             # Project documentation
├── .env                  # Environment variables
```

## Notes

- Ensure the TEMP_DIR specified in config.py exists and is writable.
- Modify the CORS_ALLOWED_ORIGINS in config.py to match the domains of your frontend applications.



