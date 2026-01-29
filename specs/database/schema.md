# Database Schema Specification

## Overview
The database schema defines the structure for storing users, tasks, and conversation data using SQLModel with Neon Serverless PostgreSQL.

## Tables

### users
- **id** (UUID, Primary Key): Unique user identifier
- **email** (VARCHAR, Unique, Not Null): User's email address
- **password_hash** (VARCHAR, Not Null): Hashed password
- **name** (VARCHAR): User's display name
- **created_at** (TIMESTAMP, Not Null): Account creation timestamp
- **updated_at** (TIMESTAMP, Not Null): Last update timestamp
- **is_active** (BOOLEAN, Not Null): Account status flag

### tasks
- **id** (UUID, Primary Key): Unique task identifier
- **user_id** (UUID, Foreign Key, Not Null): Reference to owning user
- **title** (VARCHAR, Not Null): Task title
- **description** (TEXT): Task description
- **status** (VARCHAR, Not Null): Task status ('pending', 'in-progress', 'completed')
- **priority** (VARCHAR, Not Null): Task priority ('low', 'medium', 'high')
- **due_date** (TIMESTAMP): Optional due date
- **completed_at** (TIMESTAMP): Timestamp when task was completed
- **created_at** (TIMESTAMP, Not Null): Task creation timestamp
- **updated_at** (TIMESTAMP, Not Null): Last update timestamp

### conversations
- **id** (UUID, Primary Key): Unique conversation identifier
- **user_id** (UUID, Foreign Key, Not Null): Reference to owning user
- **title** (VARCHAR): Conversation title or summary
- **created_at** (TIMESTAMP, Not Null): Conversation creation timestamp
- **updated_at** (TIMESTAMP, Not Null): Last update timestamp

### conversation_messages
- **id** (UUID, Primary Key): Unique message identifier
- **conversation_id** (UUID, Foreign Key, Not Null): Reference to parent conversation
- **role** (VARCHAR, Not Null): Message role ('user', 'assistant')
- **content** (TEXT, Not Null): Message content
- **timestamp** (TIMESTAMP, Not Null): Message timestamp
- **tool_calls** (JSONB): Optional tool calls made in this message
- **tool_responses** (JSONB): Optional responses from tools

## Relationships
- users (1) -> tasks (Many): One user can have many tasks
- users (1) -> conversations (Many): One user can have many conversations
- conversations (1) -> conversation_messages (Many): One conversation can have many messages

## Indexes
- users.email: Unique index for fast email lookup
- tasks.user_id: Index for user-based task queries
- tasks.status: Index for status-based filtering
- tasks.priority: Index for priority-based filtering
- tasks.due_date: Index for due date queries
- conversations.user_id: Index for user-based conversation queries
- conversation_messages.conversation_id: Index for conversation-based message queries
- conversation_messages.timestamp: Index for chronological ordering

## Constraints
- Foreign key relationships enforced
- Check constraints on status and priority fields
- Not null constraints on required fields
- Unique constraint on user emails

## Security Considerations
- All user data isolated by user_id foreign keys
- No cross-user data access without proper authorization
- Proper indexing for performance without exposing sensitive data