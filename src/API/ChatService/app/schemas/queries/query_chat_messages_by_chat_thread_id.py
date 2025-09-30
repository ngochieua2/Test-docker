import json
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel
import uuid

from app.models.user import User
from app.models.chat_thread import ChatThread
from app.models.chat_message import ChatMessage
from app.models.import_data import ImportData, ImportStatus


#------------------query Class---------------------

class get_chat_messages_by_chat_thread_id_query(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID

#--------------------------------------------------


#------------------response Class------------------
class import_data_dto(BaseModel):
    id: str
    file_name: str
    file_url: str
    status: str
    data_summary: str
    suggestions: List[str] = []
    data_preview: List[Dict[str, Any]]

class get_import_data_by_chat_thread_id_query_response(BaseModel):
    messages: list[import_data_dto]
                   
class chat_message_dto(BaseModel):
    id: uuid.UUID
    role: str
    message: str
    value: str | None

class get_chat_messages_by_chat_thread_id_query_response(BaseModel):
    messages: list[chat_message_dto]

#--------------------------------------------------


#------------------Exceute-------------------------

async def get_chat_messages_by_chat_thread_id_query_handler_async(
        db_session: AsyncSession, 
        query: get_chat_messages_by_chat_thread_id_query
) -> get_chat_messages_by_chat_thread_id_query_response:
    user_query=await db_session.scalars(select(User).where(User.id == query.user_id).limit(1))
    user=user_query.first()
    if user is None:
        return None
    thread_chat_query=await db_session.scalars(
        select(ChatThread)
        .where(
            and_(
                ChatThread.id==query.id,
                ChatThread.user_id==query.user_id
            )
        )
        .limit(1))
    thread_chat=thread_chat_query.first()
    if thread_chat is None:
        return None
    chat_messages_query = await db_session.scalars(
        select(ChatMessage)
        .where(
            and_(
                ChatMessage.user_id==query.user_id,
                ChatMessage.thread_id==query.id
            )
        )
    )
    chat_messages = chat_messages_query.all()
    if not chat_messages:
        return None
    return get_chat_messages_by_chat_thread_id_query_response(
        messages=[
            chat_message_dto(
                id=p.id,
                role=p.chat_role.value,
                message=p.chat_message,
                value=p.summerize_message
            )
            for p in chat_messages
        ])


async def get_import_data_by_chat_thread_id_query_handler_async(
    db_session: AsyncSession, 
    query: get_chat_messages_by_chat_thread_id_query
) -> get_import_data_by_chat_thread_id_query_response:
    # 🔹 Validate user
    user_query = await db_session.scalars(
        select(User).where(User.id == query.user_id).limit(1)
    )
    user = user_query.first()
    if user is None:
        return None

    # 🔹 Validate chat thread
    thread_chat_query = await db_session.scalars(
        select(ChatThread)
        .where(
            and_(
                ChatThread.id == query.id,
                ChatThread.user_id == query.user_id
            )
        )
        .limit(1)
    )
    thread_chat = thread_chat_query.first()
    if thread_chat is None:
        return None

    # 🔹 Get import data messages
    import_data_query = await db_session.scalars(
        select(ImportData)
        .where(
            and_(
                ImportData.UserId == query.user_id,
                ImportData.ThreadId == query.id,
                ImportData.Status == ImportStatus.COMPLETED.value
            )
        )
        .order_by(ImportData.CreatedOn.desc())
    )
    importDatas = import_data_query.all()
    if not importDatas:
        return None

    results = []
    for p in importDatas:
        # Parse Response (profiling result)
        try:
            response_obj = json.loads(p.Response) if p.Response else None
        except Exception:
            response_obj = p.Response

        data_preview = []
        if isinstance(response_obj, dict):
            data_preview = response_obj.get("preview_rows", [])

        # Parse DataSummary (contains both data_summary + suggestions)
        data_summary = ""
        suggestions = []
        try:
            if p.DataSummary:
                parsed_summary = json.loads(p.DataSummary)
                data_summary = parsed_summary.get("data_summary", "")
                suggestions = parsed_summary.get("suggestions", [])
        except Exception:
            data_summary = p.DataSummary or ""
            suggestions = []

        results.append(
            import_data_dto(
                id=str(p.Id),
                file_name=p.FileName,
                file_url=p.FileUrl,
                status=p.Status,
                data_summary=data_summary,
                data_preview=data_preview,
                suggestions=suggestions
            )
        )

    return get_import_data_by_chat_thread_id_query_response(messages=results)

#--------------------------------------------------