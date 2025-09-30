from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

import uuid
from pydantic import BaseModel

from app.core.utils.datetime_utils import now_utc

from app.models.chat_thread import ChatThread


#------------------Command Class-------------------

class create_chat_thread_command(BaseModel):
    user_id: uuid.UUID

#--------------------------------------------------


#------------------Response Class------------------

class create_chat_thread_command_response(BaseModel):
    id: uuid.UUID

#--------------------------------------------------


#------------------Execute-------------------------

async def create_chat_thread_command_handler_async(db_session: AsyncSession, model: create_chat_thread_command) -> create_chat_thread_command_response:
    stmt = (
        insert(ChatThread)
        .values(
            id=uuid.uuid4(),
            user_id=model.user_id,
            thread_name="",
            created_by=model.user_id,
            created_on=now_utc()
        )
        .returning(ChatThread)
    )
    result = await db_session.execute(stmt)
    await db_session.commit()
    chat_thread=result.scalar_one_or_none()
    if chat_thread is None:
        return None
    return create_chat_thread_command_response(
        id=chat_thread.id
    )

#--------------------------------------------------