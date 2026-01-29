from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.session import get_session
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.conversation import Conversation, ConversationMessage
from app.models.task import Task, TaskStatus
from app.schemas.chat import ChatRequest, ChatResponse, MessageCreate
from app.schemas.task import TaskCreate, TaskUpdate, TaskComplete
from app.tools.enhanced_mcp_task_tools import EnhancedMCPTaskTools
from app.core.ai_service import gemini_service
from uuid import uuid4
from datetime import datetime
from typing import Dict, Any, Optional
import json
import re
import asyncio

router = APIRouter()


def extract_priority(text: str) -> Optional[str]:
    """Extract priority from text"""
    priority_patterns = {
        'high': [r'\b(highest|high|critical|urgent|asap|top priority)\b'],
        'medium': [r'\b(medium|meh|normal|regular|standard)\b'],
        'low': [r'\b(low|lowest|optional|whenever|later)\b']
    }

    text_lower = text.lower()
    for priority, patterns in priority_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return priority
    return None


def extract_date(text: str) -> Optional[str]:
    """Extract date from text using various patterns"""
    # Pattern for formats like "tomorrow", "next week", "in 2 days", etc.
    date_patterns = [
        r'by\s+(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'on\s+(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'by\s+(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY
        r'on\s+(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY
        r'by\s+(\d{1,2}-\d{1,2}-\d{4})',  # MM-DD-YYYY
        r'in\s+(\d+)\s+(day|days|week|weeks)',  # in N days/weeks
        r'tomorrow',
        r'next\s+(week|month|year)',
    ]

    text_lower = text.lower()
    for pattern in date_patterns:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(1) if match.lastindex else match.group(0)
    return None


async def parse_natural_language_command(message: str, user_id: str, session: Session) -> Optional[Dict[str, Any]]:
    """Parse natural language command and map to appropriate MCP tool."""
    message_lower = message.lower().strip()

    # Initialize enhanced MCP tools
    tools = EnhancedMCPTaskTools(session, user_id)

    # Handle adding tasks with better parsing
    if any(word in message_lower for word in ["add", "create", "make", "new", "schedule", "put", "plan"]):
        # Extract task title and additional information
        # Patterns to capture title and additional info like priority, due date
        patterns = [
            # "add task to buy groceries with high priority by tomorrow"
            r"(?:add|create|make|new|schedule|put|plan)\s+(?:a\s+)?(?:task|todo|item)\s+(?:to|for|about|that|which)\s+(.+?)(?:\s+with\s+(.+?)(?:\s+by|date|on|\s*$))?",
            # "add buy groceries task"
            r"(?:add|create|make|new|schedule|put|plan)\s+(.+?)\s+(?:task|todo|item)",
            # General fallback
            r"(?:add|create|make|new|schedule|put|plan)\s+(.+)"
        ]

        task_title = None
        additional_info = None

        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                task_title = match.group(1).strip()
                if len(match.groups()) > 1 and match.group(2):
                    additional_info = match.group(2)
                break

        if task_title:
            # Extract priority and due date from the message
            priority = extract_priority(message)
            due_date = extract_date(message)

            result = await tools.add_task(
                title=task_title,
                priority=priority,
                due_date=due_date
            )
            return result

    # Handle listing tasks with better filters
    if any(word in message_lower for word in ["what", "show", "list", "display", "see", "my", "view", "get"]):
        status_filter = None
        priority_filter = None

        if any(word in message_lower for word in ["pending", "incomplete", "not done", "todo", "to do"]):
            status_filter = "pending"
        elif any(word in message_lower for word in ["completed", "done", "finished", "completed tasks"]):
            status_filter = "completed"
        elif any(word in message_lower for word in ["in-progress", "working", "started", "in progress"]):
            status_filter = "in-progress"

        # Check for priority filters
        if any(word in message_lower for word in ["high priority", "high-priority", "urgent", "critical"]):
            priority_filter = "high"
        elif any(word in message_lower for word in ["medium priority", "medium-priority"]):
            priority_filter = "medium"
        elif any(word in message_lower for word in ["low priority", "low-priority"]):
            priority_filter = "low"

        result = await tools.list_tasks(status=status_filter, priority=priority_filter)
        return result

    # Handle updating tasks
    if any(word in message_lower for word in ["update", "change", "modify", "edit", "adjust", "alter"]):
        # More flexible pattern matching for updates
        patterns = [
            # "update the groceries task to buy apples instead"
            r"(?:update|change|modify|edit|adjust|alter)\s+(?:the\s+)?(.+?)\s+(?:to|as|with)\s+(.+)",
            # "change groceries task title to shopping"
            r"(?:update|change|modify|edit|adjust|alter)\s+(.+?)\s+(?:title|name)\s+(?:to|as)\s+(.+)",
            # "update groceries task priority to high"
            r"(?:update|change|modify|edit|adjust|alter)\s+(.+?)\s+(?:priority|due date|status)\s+(?:to|as)\s+(.+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                task_identifier = match.group(1).strip()
                new_value = match.group(2).strip()

                # Find the task by title using enhanced tool (async call)
                task = await tools.get_task_by_title(task_identifier)

                if task:
                    # Determine what is being updated based on the original command
                    if "priority" in message_lower:
                        result = await tools.update_task(
                            task_id=task.id,
                            priority=new_value.split()[0] if new_value.split() else "medium"
                        )
                        return result
                    elif "title" in message_lower or "name" in message_lower:
                        result = await tools.update_task(task_id=task.id, title=new_value)
                        return result
                    else:
                        # Default to updating title
                        result = await tools.update_task(task_id=task.id, title=new_value)
                        return result
                else:
                    return {
                        "success": False,
                        "message": f"No task found containing '{task_identifier}'. Could you be more specific?"
                    }

    # Handle completing tasks
    if any(word in message_lower for word in ["complete", "finish", "done", "mark", "accomplish", "achieve"]):
        # More flexible patterns for completing tasks
        patterns = [
            r"(?:complete|finish|done|mark|accomplish|achieve)\s+(?:the\s+)?(.+?)(?:\s+(?:as\s+)?(?:complete|done|finished))?",
            r"(?:mark|set)\s+(?:the\s+)?(.+?)\s+(?:as\s+)?(?:complete|done|finished)",
            r"(?:complete|finish|done|mark|accomplish|achieve)\s+(?:task\s+|#)?(\d+)"
        ]

        task_identifier = None
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                task_identifier = match.group(1).strip()
                break

        if task_identifier:
            # Find the task by title using enhanced tool (async call)
            task = await tools.get_task_by_title(task_identifier)

            if task:
                result = await tools.complete_task(task_id=task.id, completed=True)
                return result
            else:
                return {
                    "success": False,
                    "message": f"No task found containing '{task_identifier}'. Could you be more specific?"
                }

    # Handle deleting tasks
    if any(word in message_lower for word in ["delete", "remove", "cancel", "erase", "eliminate"]):
        # More flexible patterns for deleting tasks
        patterns = [
            r"(?:delete|remove|cancel|erase|eliminate)\s+(?:the\s+)?(.+?)\s+(?:task|item)?",
            r"(?:delete|remove|cancel|erase|eliminate)\s+(?:task\s+|#)?(\d+)",
            r"(?:remove|delete)\s+(?:the\s+)?task\s+(?:about|for|to)\s+(.+)"
        ]

        task_identifier = None
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                task_identifier = match.group(1).strip()
                break

        if task_identifier:
            # Find the task by title using enhanced tool (async call)
            task = await tools.get_task_by_title(task_identifier)

            if task:
                result = await tools.delete_task(task_id=task.id)
                return result
            else:
                return {
                    "success": False,
                    "message": f"No task found containing '{task_identifier}'. Could you be more specific?"
                }

    # Handle general inquiries about tasks
    if "how many" in message_lower and "task" in message_lower:
        result = await tools.list_tasks()
        if result["success"]:
            count = result["result"]["count"]
            status_msg = result["result"]["message"]
            return {
                "success": True,
                "result": {
                    "message": f"You have {count} tasks. {status_msg}."
                }
            }
        return result

    # Default response if command not recognized
    return {
        "success": False,
        "message": f"I'm not sure how to handle '{message}'. You can ask me to add tasks, list your tasks, update tasks, complete tasks, or delete tasks. For example: 'Add a task to buy groceries', 'Show my pending tasks', or 'Mark the meeting task as complete'."
    }


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    chat_request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Process natural language chat request and return response."""
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's chat"
        )

    # Create or get existing conversation
    statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
    conversation = session.execute(statement).scalar()

    if not conversation:
        conversation = Conversation(user_id=user_id, title="New Conversation")
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Save user message
    user_message = ConversationMessage(
        conversation_id=conversation.id,
        role="user",
        content=chat_request.message
    )
    session.add(user_message)

    # Check if the message is a task management command or general chat
    message_lower = chat_request.message.lower()

    # If it's a task-related command, use the existing MCP tools
    is_task_command = any(keyword in message_lower for keyword in [
        "add", "create", "make", "new", "schedule", "put", "plan",
        "what", "show", "list", "display", "see", "view", "get",
        "update", "change", "modify", "edit", "adjust", "alter",
        "complete", "finish", "done", "mark", "accomplish", "achieve",
        "delete", "remove", "cancel", "erase", "eliminate", "how many"
    ])

    if is_task_command:
        # Process the natural language command with enhanced MCP tools
        result = await parse_natural_language_command(chat_request.message, user_id, session)

        # Generate response based on tool execution result
        response_text = result.get("result", {}).get("message", result.get("message", "I processed your request."))
    else:
        # Use AI for general conversation
        response_text = gemini_service.generate_response(chat_request.message, session, user_id)

    # Save assistant response
    assistant_message = ConversationMessage(
        conversation_id=conversation.id,
        role="assistant",
        content=response_text
    )
    session.add(assistant_message)

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)

    session.commit()

    return ChatResponse(
        response=response_text,
        conversation_id=conversation.id
    )