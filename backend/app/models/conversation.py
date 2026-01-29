from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import uuid4
from typing import Optional, Dict, Any
from sqlalchemy import JSON

class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None)

class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(nullable=False, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ConversationMessageBase(SQLModel):
    role: str = Field(nullable=False)  # "user" or "assistant"
    content: str = Field(nullable=False)

class ConversationMessage(ConversationMessageBase, table=True):
    __tablename__ = "conversation_messages"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    conversation_id: str = Field(nullable=False, foreign_key="conversations.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)
    tool_responses: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON)

class ConversationCreate(ConversationBase):
    pass

class ConversationRead(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class MessageCreate(ConversationMessageBase):
    pass

class MessageRead(ConversationMessageBase):
    id: str
    conversation_id: str
    timestamp: datetime
    tool_calls: Optional[Dict[str, Any]] = None
    tool_responses: Optional[Dict[str, Any]] = None