async def save_large_file(upload_file, destination, chunk_size=1024 * 1024):
    """Save an uploaded file in chunks."""
    with open(destination, "wb") as buffer:
        while chunk := await upload_file.read(chunk_size):
            buffer.write(chunk)
