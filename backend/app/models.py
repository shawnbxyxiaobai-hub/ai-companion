from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    user_id: str
    name: str = "用户"
    preference: dict = {}
    emotion_state: str = "neutral"
    created_at: datetime = None
    updated_at: datetime = None

class Memory(BaseModel):
    memory_id: Optional[str] = None
    user_id: str
    content: str
    memory_type: str  # preference/habit/emotion/event
    importance: int = 3  # 1-5
    created_at: datetime = None
    updated_at: datetime = None

class Message(BaseModel):
    role: str  # user/assistant
    content: str
    timestamp: datetime = None

class Conversation(BaseModel):
    conv_id: Optional[str] = None
    user_id: str
    messages: List[Message] = []
    created_at: datetime = None

class Reminder(BaseModel):
    reminder_id: Optional[str] = None
    user_id: str
    title: str
    content: str
    reminder_type: str  # interval/fixed/event
    time: str  # HH:MM format or interval in minutes
    enabled: bool = True
    created_at: datetime = None

class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: dict = {}

class ChatResponse(BaseModel):
    reply: str
    emotion: str  # positive/negative/neutral
