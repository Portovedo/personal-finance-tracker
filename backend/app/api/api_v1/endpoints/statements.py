
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.file import FileUpload
from app.services.statement_processor import StatementProcessor

router = APIRouter()

@router.post("/process/{file_id}")
async def process_statement(file_id: str, db: Session = Depends(get_db)):
    """
    Process an uploaded statement.
    """
    file_upload = db.query(FileUpload).filter(FileUpload.id == file_id).first()
    if not file_upload:
        raise HTTPException(status_code=404, detail="File not found")

    processor = StatementProcessor(file_path=file_upload.file_path, file_type=file_upload.mime_type)
    transactions = processor.process()

    # Here we would save the transactions to the database, but for now, we'll just return them.
    return transactions
