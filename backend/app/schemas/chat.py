from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None

class ConversationCreate(BaseModel):
    title: Optional[str] = None

class ConversationRead(BaseModel):
    id: str
    user_id: str
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    tool_calls: Optional[Dict[str, Any]] = None
    tool_responses: Optional[Dict[str, Any]] = None

class MessageRead(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    timestamp: datetime
    tool_calls: Optional[Dict[str, Any]] = None
    tool_responses: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True