import os
import time

def cleanup_temp_files(directory: str, max_age_seconds: int = 3600):
    """Remove files older than `max_age_seconds` in the specified directory."""
    current_time = time.time()
    if not os.path.exists(directory):
        return
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")
