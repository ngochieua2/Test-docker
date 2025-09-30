from pydantic import BaseModel, Field


class ChatMessageCreateRequest(BaseModel):
    message: str = Field(alias="message")