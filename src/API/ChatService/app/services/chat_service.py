from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from uuid import UUID, uuid4

from app.config import settings

from sqlalchemy import select, insert, desc

from app.core.utils.datetime_utils import now_utc

from app.models.chat_message import ChatMessage
from app.enums.chat_role import ChatRole

from app.services.openai_service import ask_openai, OpenAIChatMessage, OpenAIChatModel


#------------------Objects Class-------------------

class ChatDto(BaseModel):
    user_id: UUID
    thread_id: UUID
    message: str

class ChatResponseDto(BaseModel):
    response: str

#--------------------------------------------------

#------------------Services Class------------------

async def chat_async(
        db_session: AsyncSession,
        model: ChatDto
) -> ChatResponseDto:
    chats_query = await db_session.scalars(select(ChatMessage).where(ChatMessage.thread_id==model.thread_id).order_by(desc(ChatMessage.created_on)).limit(8))
    chats = chats_query.all()
    content_list: List[OpenAIChatMessage] = []
    if not chats:
        content_list.append(
                OpenAIChatMessage(
                    role=ChatRole.USER.value,
                    content=model.message
                )
            )
    else:
        chats = sorted(chats, key=lambda p: p.created_on)
        content_list = list(
            [
                OpenAIChatMessage(
                    role=p.chat_role,
                    content=p.chat_message
                )
                for p in chats
            ]
        )
        content_list.append(
                OpenAIChatMessage(
                    role=ChatRole.USER.value,
                    content=model.message
                )
            )
    openai_model = settings.CHAT_GPTs_MODEL
    ask_model = OpenAIChatModel(messages=content_list)
    ask_openai_response = ask_openai(ask_model, openai_model)
    if ask_openai_response is None:
        return None
    creat_chat_entities: List[ChatMessage] = []
    creat_chat_entities.append(
        ChatMessage(
            id=uuid4(),
            thread_id=model.thread_id,
            user_id=model.user_id,
            chat_role=ChatRole.USER,
            chat_message=model.message,
            created_by=model.user_id,
            created_on=now_utc()
        )
    )
    creat_chat_entities.append(ChatMessage(
            id=uuid4(),
            thread_id=model.thread_id,
            user_id=model.user_id,
            chat_role=ChatRole.ASSISTANT,
            chat_message=ask_openai_response,
            created_by=model.user_id,
            created_on=now_utc()
        )
    )
    insert_entities = [
        {
            "id": e.id,
            "thread_id": e.thread_id,
            "user_id": e.user_id,
            "chat_role": e.chat_role,
            "chat_message": e.chat_message,
            "created_by": e.created_by,
            "created_on": e.created_on,
        }
        for e in creat_chat_entities
    ]
    stmt = insert(ChatMessage).values(insert_entities).returning(ChatMessage.id)
    result = await db_session.execute(stmt)
    await db_session.commit()
    ids = result.scalars().all()
    if not ids:
        return None
    else:
        return ChatResponseDto(response=ask_openai_response)
    
async def excute_gpt_chat_async(
    prompt: str,
    content: str
) -> ChatResponseDto:
    content_list: List[OpenAIChatMessage] = [
        OpenAIChatMessage(role=ChatRole.SYSTEM.value, content=prompt),
        OpenAIChatMessage(role=ChatRole.USER.value, content=content),
    ]

    ask_model = OpenAIChatModel(messages=content_list)
    ask_openai_response = ask_openai(model=ask_model, openai_model=settings.CHAT_GPTs_MODEL)
    if not ask_openai_response:
        return ChatResponseDto(response="No response")

    summary_text = ask_openai_response

    return ChatResponseDto(response=summary_text)

#--------------------------------------------------