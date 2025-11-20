
from pydantic import BaseModel

import uuid
from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    id: uuid.UUID
    filename: str
    content_type: str
    size: int
