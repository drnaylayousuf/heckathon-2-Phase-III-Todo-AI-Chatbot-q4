# Data Model: Hackathon Todo Application

## Entity: User
**Description**: Represents a registered user with authentication credentials and profile information

### Fields:
- `id` (UUID, Primary Key): Unique user identifier
- `email` (String, Required, Unique): User's email address for authentication
- `password_hash` (String, Required): Bcrypt hash of user's password
- `name` (String, Optional): User's display name
- `created_at` (DateTime, Required): Account creation timestamp
- `updated_at` (DateTime, Required): Last update timestamp
- `is_active` (Boolean, Required): Account status flag

### Validation Rules:
- Email must be valid email format
- Email must be unique across all users
- Password must be hashed before storage
- Name, if provided, must be 1-100 characters

## Entity: Task
**Description**: Represents a todo item owned by a user with attributes like title, description, status, priority, due date

### Fields:
- `id` (UUID, Primary Key): Unique task identifier
- `user_id` (UUID, Foreign Key, Required): Reference to owning user
- `title` (String, Required): Task title (1-200 characters)
- `description` (String, Optional): Task description (max 1000 characters)
- `status` (Enum: pending, in-progress, completed, Required): Task status
- `priority` (Enum: low, medium, high, Required): Task priority level
- `due_date` (DateTime, Optional): Deadline for task completion
- `completed_at` (DateTime, Optional): Timestamp when task was completed
- `created_at` (DateTime, Required): Task creation timestamp
- `updated_at` (DateTime, Required): Last update timestamp

### Validation Rules:
- Title must be 1-200 characters
- Description, if provided, must be 1-1000 characters
- Status must be one of: pending, in-progress, completed
- Priority must be one of: low, medium, high
- User_id must reference an existing, active user
- Due date must be in the future if provided

### State Transitions:
- `pending` → `in-progress`: When user starts working on task
- `in-progress` → `completed`: When user marks task as done
- `completed` → `in-progress`: When user reopens completed task
- `in-progress` → `pending`: When user reverts to pending status

## Entity: Conversation
**Description**: Represents a chat session between user and AI assistant

### Fields:
- `id` (UUID, Primary Key): Unique conversation identifier
- `user_id` (UUID, Foreign Key, Required): Reference to owning user
- `title` (String, Optional): Conversation title or summary
- `created_at` (DateTime, Required): Conversation creation timestamp
- `updated_at` (DateTime, Required): Last update timestamp

### Validation Rules:
- User_id must reference an existing, active user
- Title, if provided, must be 1-200 characters

## Entity: Message
**Description**: Represents individual messages within a conversation, including user input and AI responses

### Fields:
- `id` (UUID, Primary Key): Unique message identifier
- `conversation_id` (UUID, Foreign Key, Required): Reference to parent conversation
- `role` (Enum: user, assistant, Required): Message sender role
- `content` (String, Required): Message content (1-5000 characters)
- `timestamp` (DateTime, Required): Message timestamp
- `tool_calls` (JSON, Optional): Optional tool calls made in this message
- `tool_responses` (JSON, Optional): Optional responses from tools

### Validation Rules:
- Conversation_id must reference an existing conversation
- Role must be either 'user' or 'assistant'
- Content must be 1-5000 characters
- Tool calls and responses must be valid JSON if provided

## Relationships:
- **User (1)** ←→ **Task (Many)**: One user can have many tasks
- **User (1)** ←→ **Conversation (Many)**: One user can have many conversations
- **Conversation (1)** ←→ **Message (Many)**: One conversation can have many messages

## Indexes:
- User.email: Unique index for fast email lookup
- Task.user_id: Index for user-based task queries
- Task.status: Index for status-based filtering
- Task.priority: Index for priority-based filtering
- Task.due_date: Index for due date queries
- Conversation.user_id: Index for user-based conversation queries
- Message.conversation_id: Index for conversation-based message queries
- Message.timestamp: Index for chronological ordering

## Constraints:
- Foreign key relationships enforced at database level
- Check constraints on status and priority enums
- Not null constraints on required fields
- Unique constraint on user emails
- User isolation enforced through application logic (user can only access their own data)