from typing import Annotated

from app.db.session import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

DbContext = Annotated[AsyncSession, Depends(get_db_session)]
