"""
Image Utilities Module
Contains helper functions for handling image uploads.
"""

import shutil
from fastapi import UploadFile

def save_upload_image(uploaded_file: UploadFile, destination: str) -> None:
    """
    Save an uploaded file to a destination path.

    Args:
        uploaded_file (UploadFile): The file uploaded via FastAPI.
        destination (str): The path to save the file to.
    """
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
        print(f"File '{uploaded_file.filename}' saved to '{destination}'")
    except IOError as e:
        print(f"Error saving file: {e}")
        raise e
    finally:
        uploaded_file.file.close() # Ensure the file is closed

