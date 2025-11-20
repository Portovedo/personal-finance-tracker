
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.file import FileUpload

def test_upload_file(client: TestClient, db: Session):
    # Create a fake file
    file_content = b"col1,col2\nval1,val2"
    files = {"file": ("test.csv", file_content, "text/csv")}

    # Upload the file
    response = client.post("/api/v1/files/upload", files=files)

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.csv"
    assert data["content_type"] == "text/csv"

    # Check that a FileUpload record was created
    file_upload = db.query(FileUpload).filter(FileUpload.original_filename == "test.csv").first()
    assert file_upload is not None
