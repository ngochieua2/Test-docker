from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from typing import Optional
import os
from shared.constants.constants import VALID_FILE_TYPES

from app.services.handle_file_service import HandleFileService

router = APIRouter()

@router.post("/", response_class=PlainTextResponse)
async def process_data(
    file: UploadFile = File(...), 
    handleFileService: HandleFileService = Depends(HandleFileService)
) -> Optional[str]:
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in VALID_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Only .csv, .xlsx, .xls files are allowed")

    data_summary = await handleFileService.generate_data_summary(file, file_extension)

    if data_summary is None:
        raise HTTPException(status_code=400, detail="Error occurred while generating data summary")

    return data_summary
