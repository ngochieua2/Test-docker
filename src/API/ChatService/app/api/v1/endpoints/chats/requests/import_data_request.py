import uuid
from pydantic import BaseModel

class ImportDataRequest(BaseModel):
    file_base64: str
    filename: str
    fileUrl: str = None  # Optional URL for the file
    thread_id : uuid.UUID
    user_id : uuid.UUID