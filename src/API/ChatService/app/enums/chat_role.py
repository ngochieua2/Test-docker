from enum import Enum


class ChatRole(Enum):
        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"
        TOOL = "tool"