"""
Enhanced MCP Task Tools with better error handling and context awareness
"""
from typing import Dict, Any, Optional, List
from sqlmodel import Session
from app.models.task import Task as TaskModel, TaskStatus, TaskPriority
from app.models.conversation import ConversationMessage
from datetime import datetime
import json
import re
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class EnhancedMCPTaskTools:
    """
    Enhanced MCP tools implementation with better context awareness and error handling
    """

    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.user_id = user_id

    async def add_task(self, title: str, description: Optional[str] = None, priority: Optional[str] = "medium", due_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a new task with enhanced validation and error handling
        """
        try:
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

            logger.info(f"Task created: {new_task.id} for user {self.user_id}")

            return {
                "success": True,
                "result": {
                    "task_id": new_task.id,
                    "task": {
                        "id": new_task.id,
                        "title": new_task.title,
                        "description": new_task.description,
                        "status": new_task.status,
                        "priority": new_task.priority,
                        "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
                        "created_at": new_task.created_at.isoformat()
                    },
                    "message": f"Task '{title}' has been added successfully"
                }
            }
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error adding task for user {self.user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to add task"
            }

    async def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None, sort_by: Optional[str] = None, order: Optional[str] = "asc") -> Dict[str, Any]:
        """
        List tasks with enhanced filtering and sorting
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
            else:
                # Default sorting: by status (pending first), then by creation date (newest first)
                statement = statement.order_by(
                    TaskModel.status.asc(),  # pending comes first
                    TaskModel.created_at.desc()
                )

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
                    "count": len(task_list),
                    "message": f"Found {len(task_list)} tasks" if task_list else "No tasks found"
                }
            }
        except Exception as e:
            logger.error(f"Error listing tasks for user {self.user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to list tasks"
            }

    async def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None,
                         priority: Optional[str] = None, due_date: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing task with enhanced validation
        """
        try:
            from sqlmodel import select

            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == self.user_id
            )
            task = self.session.execute(statement).scalars().first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or access denied"
                }

            # Track what changed for the response
            changes = []

            # Validate and update fields if provided
            if title is not None and title != task.title:
                task.title = title
                changes.append(f"title to '{title}'")
            if description is not None and description != task.description:
                task.description = description
                changes.append("description")
            if priority is not None and priority != task.priority:
                if priority not in ["low", "medium", "high"]:
                    return {
                        "success": False,
                        "error": "Invalid priority. Must be 'low', 'medium', or 'high'",
                        "message": "Invalid priority provided"
                    }
                task.priority = priority
                changes.append(f"priority to '{priority}'")
            if due_date is not None:
                try:
                    parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    task.due_date = parsed_due_date
                    changes.append(f"due date to '{due_date}'")
                except ValueError:
                    return {
                        "success": False,
                        "error": "Invalid due date format. Must be ISO 8601 format",
                        "message": "Invalid due date format"
                    }
            if status is not None and status != task.status:
                if status not in ["pending", "in-progress", "completed"]:
                    return {
                        "success": False,
                        "error": "Invalid status. Must be 'pending', 'in-progress', or 'completed'",
                        "message": "Invalid status provided"
                    }
                task.status = status
                if status == "completed":
                    task.completed_at = datetime.utcnow()
                    changes.append("status to completed")
                else:
                    if task.status == "completed":
                        task.completed_at = None  # Reset completed_at if changing from completed
                        changes.append(f"status to '{status}'")
                changes[-1] += f" and marked {'completed' if status == 'completed' else 'not completed'}"

            if not changes:
                return {
                    "success": False,
                    "message": "No changes were made to the task"
                }

            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            changes_str = ", ".join(changes)
            return {
                "success": True,
                "result": {
                    "message": f"Task '{task.title}' has been updated ({changes_str})"
                }
            }
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating task {task_id} for user {self.user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update task"
            }

    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Delete a task with enhanced confirmation
        """
        try:
            from sqlmodel import select

            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == self.user_id
            )
            task = self.session.execute(statement).scalars().first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or access denied"
                }

            task_title = task.title
            self.session.delete(task)
            self.session.commit()

            logger.info(f"Task deleted: {task_id} for user {self.user_id}")

            return {
                "success": True,
                "result": {
                    "message": f"Task '{task_title}' has been deleted successfully"
                }
            }
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting task {task_id} for user {self.user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to delete task"
            }

    async def complete_task(self, task_id: str, completed: bool) -> Dict[str, Any]:
        """
        Mark a task as complete/incomplete with enhanced response
        """
        try:
            from sqlmodel import select

            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == self.user_id
            )
            task = self.session.execute(statement).scalars().first()

            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "message": "Task not found or access denied"
                }

            if completed:
                task.status = "completed"
                task.completed_at = datetime.utcnow()
                action = "completed"
            else:
                task.status = "pending"
                task.completed_at = None
                action = "marked as pending"

            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            return {
                "success": True,
                "result": {
                    "message": f"Task '{task.title}' has been {action}",
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "status": task.status,
                        "completed_at": task.completed_at.isoformat() if task.completed_at else None
                    }
                }
            }
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating completion status for task {task_id} for user {self.user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update task completion status"
            }

    async def get_task_by_title(self, title_query: str) -> Optional[TaskModel]:
        """
        Find a task by partial title match
        """
        from sqlmodel import select

        # First try exact match
        statement = select(TaskModel).where(
            TaskModel.user_id == self.user_id,
            TaskModel.title.ilike(f"%{title_query}%")
        ).order_by(TaskModel.created_at.desc())

        # Execute the statement and get scalar results
        results = self.session.execute(statement)
        tasks = results.scalars().all()

        if len(tasks) == 1:
            return tasks[0]

        # If multiple matches, return the most recent one
        if tasks:
            return tasks[0]

        return None