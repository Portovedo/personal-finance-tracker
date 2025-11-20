
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.file import FileUpload
from app.schemas.file import FileUploadResponse
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a file (PDF or CSV) for statement processing.
    """
    # Validate file type
    if file.content_type not in ["application/pdf", "text/csv"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and CSV are supported.")

    # Validate file size (max 50MB)
    if file.size > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the 50MB limit.")

    # Save the file
    stored_filename = f"{uuid.uuid4()}-{file.filename}"
    file_path = f"uploads/{stored_filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create a record in the database
    file_upload = FileUpload(
        user_id=current_user.id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=file_path,
        file_type=file.content_type.split("/")[1],
        mime_type=file.content_type,
        file_size=file.size,
    )
    db.add(file_upload)
    db.commit()
    db.refresh(file_upload)

    return file_upload
