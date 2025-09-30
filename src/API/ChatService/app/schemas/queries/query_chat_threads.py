from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel, Field
from uuid import UUID

from app.models.user import User
from app.models.chat_thread import ChatThread


#------------------query Class---------------------

class get_chat_threads_by_user_id_query(BaseModel):
    user_id: UUID

#--------------------------------------------------


#------------------response Class------------------

class chat_threads_by_usear_id_dto(BaseModel):
    id: UUID = Field(alias="id")

class get_chat_threads_by_usear_id_query_response(BaseModel):
    thread_ids: list[chat_threads_by_usear_id_dto] = Field(alias="threadIds")

    class Config:
        populate_by_name = True

#--------------------------------------------------


#------------------Exceute-------------------------

async def get_chat_threads_by_user_id_query_handler_async(
        db_session: AsyncSession, 
        query: get_chat_threads_by_user_id_query
) -> get_chat_threads_by_usear_id_query_response:
    user_query=await db_session.scalars(select(User).where(User.id == query.user_id).limit(1))
    user=user_query.first()
    if user is None:
        return None
    chat_thread_query=await db_session.scalars(select(ChatThread).where(ChatThread.user_id==query.user_id))
    chat_threads=chat_thread_query.all()
    if not chat_threads:
        return None
    return get_chat_threads_by_usear_id_query_response(
        thread_ids=[
            chat_threads_by_usear_id_dto(
                id=p.id 
            )
            for p in chat_threads]
    )

#--------------------------------------------------