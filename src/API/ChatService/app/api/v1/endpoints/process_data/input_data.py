import os

from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse


from app.core.utils.constants import VALID_FILE_TYPES
from .helpers import generate_data_summary

router = APIRouter()

@router.post("", response_class=PlainTextResponse)
async def process_data(file: UploadFile = File(...)) -> Optional[str]:
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in VALID_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Only .csv, .xlsx, .xls files are allowed")

    data_summary = await generate_data_summary(file, file_extension)

    if data_summary is None:
        raise HTTPException(status_code=400, detail="Error occurred while generating data summary")

    return data_summary
