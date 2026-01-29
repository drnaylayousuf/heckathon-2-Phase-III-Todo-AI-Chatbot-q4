"""
MCP Task Tools Implementation
Real MCP tools for task management operations
"""
from typing import Dict, Any, Optional
from sqlmodel import Session
from app.models.task import Task as TaskModel, TaskStatus
from app.models.conversation import ConversationMessage
from datetime import datetime
import json


class MCPTaskTools:
    """
    Real MCP tools implementation for task management operations
    """

    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.user_id = user_id

    async def add_task(self, title: str, description: Optional[str] = None, priority: Optional[str] = "medium", due_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a new task - MCP tool implementation
        """
        try:
            # Import here to avoid circular imports
            from app.models.task import Task as TaskModel, TaskPriority

            # Validate priority
            if priority and priority not in ["low", "medium", "high"]:
                return {
                    "success": False,
                    "error": "Invalid priority. Must be 'low', 'medium', or 'high'",
                    "message": "Invalid priority provided"
                }

            # Parse due date if provided
            parsed_due_date = None
            if due_date:
                try:
                    parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    return {
                        "success": False,
                        "error": "Invalid due date format. Must be ISO 8601 format",
                        "message": "Invalid due date format"
                    }

            new_task = TaskModel(
                title=title,
                description=description,
                user_id=self.user_id,
                status="pending",
                priority=priority or "medium",
                due_date=parsed_due_date
            )
            self.session.add(new_task)
            self.session.commit()
            self.session.refresh(new_task)

            return {
                "success": True,
                "result": {
                    "task_id": new_task.id,
                    "message": f"Task '{title}' has been added successfully"
                }
            }
        except Exception as e:
            self.session.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to add task"
            }

    async def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None, sort_by: Optional[str] = None, order: Optional[str] = "asc") -> Dict[str, Any]:
        """
        List tasks for the user - MCP tool implementation
        """
        try:
            from sqlmodel import select

            statement = select(TaskModel).where(TaskModel.user_id == self.user_id)

            if status:
                if status not in ["pending", "in-progress", "completed"]:
                    return {
                        "success": False,
                        "error": "Invalid status. Must be 'pending', 'in-progress', or 'completed'",
                        "message": "Invalid status provided"
                    }
                statement = statement.where(TaskModel.status == status)

            if priority:
                if priority not in ["low", "medium", "high"]:
                    return {
                        "success": False,
                        "error": "Invalid priority. Must be 'low', 'medium', or 'high'",
                        "message": "Invalid priority provided"
                    }
                statement = statement.where(TaskModel.priority == priority)

            # Apply sorting
            if sort_by == "title":
                if order == "desc":
                    statement = statement.order_by(TaskModel.title.desc())
                else:
                    statement = statement.order_by(TaskModel.title.asc())
            elif sort_by == "due_date":
                if order == "desc":
                    statement = statement.order_by(TaskModel.due_date.desc())
                else:
                    statement = statement.order_by(TaskModel.due_date.asc())
            elif sort_by == "priority":
                if order == "desc":
                    statement = statement.order_by(TaskModel.priority.desc())
                else:
                    statement = statement.order_by(TaskModel.priority.asc())
            elif sort_by == "created_at":
                if order == "desc":
                    statement = statement.order_by(TaskModel.created_at.desc())
                else:
                    statement = statement.order_by(TaskModel.created_at.asc())

            tasks = self.session.execute(statement).scalars().all()

            task_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                    "due_date": task.due_date.isoformat() if task.due_date else None
                }
                task_list.append(task_dict)

            return {
                "success": True,
                "result": {
                    "tasks": task_list,
                    "count": len(task_list)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to list tasks"
            }

    async def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None,
                         priority: Optional[str] = None, due_date: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing task - MCP tool implementation
        """
        try:
            from sqlmodel import select

            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == self.user_id
            )
            task = self.session.execute(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or access denied"
                }

            # Validate and update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                if priority not in ["low", "medium", "high"]:
                    return {
                        "success": False,
                        "error": "Invalid priority. Must be 'low', 'medium', or 'high'",
                        "message": "Invalid priority provided"
                    }
                task.priority = priority
            if due_date is not None:
                try:
                    parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    task.due_date = parsed_due_date
                except ValueError:
                    return {
                        "success": False,
                        "error": "Invalid due date format. Must be ISO 8601 format",
                        "message": "Invalid due date format"
                    }
            if status is not None:
                if status not in ["pending", "in-progress", "completed"]:
                    return {
                        "success": False,
                        "error": "Invalid status. Must be 'pending', 'in-progress', or 'completed'",
                        "message": "Invalid status provided"
                    }
                task.status = status
                if status == "completed":
                    task.completed_at = datetime.utcnow()
                else:
                    if task.status == "completed":
                        task.completed_at = None  # Reset completed_at if changing from completed

            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            return {
                "success": True,
                "result": {
                    "message": f"Task '{task.title}' has been updated successfully"
                }
            }
        except Exception as e:
            self.session.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update task"
            }

    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Delete a task - MCP tool implementation
        """
        try:
            from sqlmodel import select

            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == self.user_id
            )
            task = self.session.execute(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or access denied"
                }

            task_title = task.title
            self.session.delete(task)
            self.session.commit()

            return {
                "success": True,
                "result": {
                    "message": f"Task '{task_title}' has been deleted successfully"
                }
            }
        except Exception as e:
            self.session.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to delete task"
            }

    async def complete_task(self, task_id: str, completed: bool) -> Dict[str, Any]:
        """
        Mark a task as complete/incomplete - MCP tool implementation
        """
        try:
            from sqlmodel import select

            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == self.user_id
            )
            task = self.session.execute(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or access denied"
                }

            if completed:
                task.status = "completed"
                task.completed_at = datetime.utcnow()
            else:
                task.status = "pending"
                task.completed_at = None

            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            status_text = "completed" if completed else "marked as pending"
            return {
                "success": True,
                "result": {
                    "message": f"Task '{task.title}' has been {status_text}"
                }
            }
        except Exception as e:
            self.session.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update task completion status"
            }