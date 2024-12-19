from fastapi import HTTPException

def file_not_found_error():
    return HTTPException(status_code=404, detail="File not found.")

def invalid_csv_error():
    return HTTPException(status_code=400, detail="Invalid CSV structure.")

def file_too_large_error(max_size_mb):
    return HTTPException(status_code=400, detail=f"File is too large. Maximum size is {max_size_mb}MB.")

def invalid_file_type_error():
    return HTTPException(status_code=400, detail="Invalid file type. Only .csv files are allowed.")

def file_save_error():
    return HTTPException(status_code=500, detail="Internal server error while saving the file.")

def cleanup_error():
    return HTTPException(status_code=500, detail="Internal server error during cleanup.")

def csv_validation_error():
    return HTTPException(status_code=500, detail="Internal server error during CSV validation.")
