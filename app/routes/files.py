import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.uploaded_file import UploadedFile

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = "uploads"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a file, save it to local storage, and create a record in the database.
    """
    try:
        # Read the file content
        file_content = await file.read()
        size_bytes = len(file_content)
        
        # Determine MIME type safely
        mime_type = file.content_type if file.content_type else "application/octet-stream"
        
        # Generate a unique filename and path
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        storage_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the file to disk
        with open(storage_path, "wb") as f:
            f.write(file_content)
            
        # Create database record
        uploaded_file = UploadedFile(
            user_id=current_user.id,
            filename=file.filename,
            storage_path=storage_path,
            mime_type=mime_type,
            size_bytes=size_bytes,
            is_processed=False
        )
        
        db.add(uploaded_file)
        db.commit()
        db.refresh(uploaded_file)
        
        return {
            "file_id": uploaded_file.id,
            "filename": uploaded_file.filename,
            "size_bytes": uploaded_file.size_bytes,
            "mime_type": uploaded_file.mime_type
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )
