from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import uuid4
from typing import Optional

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = None

class User(UserBase, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

class UserUpdate(SQLModel):
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None