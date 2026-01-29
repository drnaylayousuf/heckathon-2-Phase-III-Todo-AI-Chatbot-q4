from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database.session import get_session
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskComplete, TaskFilter
from uuid import UUID
from datetime import datetime

router = APIRouter()

def verify_user_owns_task(session: Session, user_id: str, task_id: str) -> Task:
    """Verify that the user owns the task."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.execute(statement).scalar()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )
    return task

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    filters: TaskFilter = Depends()
):
    """Get all tasks for the authenticated user."""
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's tasks"
        )

    # Build query with filters
    statement = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if filters.status:
        statement = statement.where(Task.status == filters.status)

    # Apply priority filter
    if filters.priority:
        statement = statement.where(Task.priority == filters.priority)

    # Apply search filter
    if filters.search:
        statement = statement.where(Task.title.contains(filters.search) | Task.description.contains(filters.search))

    # Apply sorting
    if filters.sort_by == "title":
        if filters.order == "desc":
            statement = statement.order_by(Task.title.desc())
        else:
            statement = statement.order_by(Task.title.asc())
    elif filters.sort_by == "due_date":
        if filters.order == "desc":
            statement = statement.order_by(Task.due_date.desc())
        else:
            statement = statement.order_by(Task.due_date.asc())
    elif filters.sort_by == "priority":
        if filters.order == "desc":
            statement = statement.order_by(Task.priority.desc())
        else:
            statement = statement.order_by(Task.priority.asc())
    else:  # Default to created_at
        if filters.order == "desc":
            statement = statement.order_by(Task.created_at.desc())
        else:
            statement = statement.order_by(Task.created_at.asc())

    tasks = session.execute(statement).scalars().all()
    return tasks

@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task(
    user_id: str,
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task for the authenticated user."""
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot create tasks for another user"
        )

    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        user_id=current_user.id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
def update_task(
    user_id: str,
    id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing task."""
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's tasks"
        )

    db_task = verify_user_owns_task(session, current_user.id, id)

    # Update task fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{user_id}/tasks/{id}")
def delete_task(
    user_id: str,
    id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a task."""
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot delete another user's tasks"
        )

    db_task = verify_user_owns_task(session, current_user.id, id)

    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}

@router.patch("/{user_id}/tasks/{id}/complete")
def complete_task(
    user_id: str,
    id: str,
    task_complete: TaskComplete,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Mark a task as complete or incomplete."""
    # Verify that the requested user_id matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's tasks"
        )

    db_task = verify_user_owns_task(session, current_user.id, id)

    # Update completion status
    if task_complete.completed:
        db_task.status = "completed"
        db_task.completed_at = datetime.utcnow()
    else:
        db_task.status = "pending"
        db_task.completed_at = None

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task