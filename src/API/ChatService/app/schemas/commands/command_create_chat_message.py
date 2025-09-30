from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, and_

import uuid
from pydantic import BaseModel

from app.core.utils.datetime_utils import now_utc

from app.models.user import User
from app.models.chat_thread import ChatThread
from app.models.chat_message import ChatMessage

from app.enums.chat_role import ChatRole

from app.services.chat_service import chat_async, ChatDto


#------------------Command Class-------------------

class create_chat_message_command(BaseModel):
    user_id: uuid.UUID
    chat_thread_id: uuid.UUID
    message: str

#--------------------------------------------------


#------------------Response Class------------------

class create_chat_message_command_response(BaseModel):
    response: str

#--------------------------------------------------


#------------------Execute-------------------------

async def create_chat_message_command_handler_async(
        db_session: AsyncSession, 
        model: create_chat_message_command
) -> create_chat_message_command_response:
    user_query = await db_session.scalars(select(User).where(User.id==model.user_id).limit(1))
    user = user_query.first()
    if user is None:
        return None
    thread_chat_query=await db_session.scalars(
        select(ChatThread)
        .where(
            and_(
                ChatThread.id==model.chat_thread_id,
                ChatThread.user_id==model.user_id
            )
        )
        .limit(1))
    chat_thread=thread_chat_query.first()
    if chat_thread is None:
        return None
    chat_messages = await chat_async(
        db_session,
        ChatDto(
            user_id=model.user_id,
            thread_id=model.chat_thread_id,
            message=model.message
        )
    )
    if not chat_messages:
        return None
    return create_chat_message_command_response(
        response=chat_messages.reponse
    )

#--------------------------------------------------