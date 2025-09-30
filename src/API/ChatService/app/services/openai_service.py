from pydantic import BaseModel
from openai import OpenAI
from typing import List, Optional

from app.config import settings


class OpenAIChatMessage(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None

class OpenAIChatModel(BaseModel):
    messages: Optional[List[OpenAIChatMessage]] = None

client = OpenAI(
    # This is the default and can be omitted
    api_key=settings.CHAT_GPTs_API_KEY
)

def ask_openai(model: OpenAIChatModel, openai_model: str = "gpt-4o") -> str:
    try:
        completion = client.chat.completions.create(
            model=openai_model,
            messages=format_messages(model.messages)
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def format_messages(user_messages: list[OpenAIChatMessage]) -> list[dict]:
    messages = [{"role": "system", "content": "You are an profeshional data analytics"}]
    for msg in user_messages:
        messages.append({"role": msg.role, "content": msg.content})
    return messages