from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class ImportProfileResponse(BaseModel):
    filename: str
    import_record_id: Optional[str]
    data_summary: Optional[str] = None
    suggestions : List[str] = []
    data_preview: List[Dict[str, Any]]

