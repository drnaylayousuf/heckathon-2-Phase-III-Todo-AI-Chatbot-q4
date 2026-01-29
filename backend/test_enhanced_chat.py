#!/usr/bin/env python3
"""
Simple test script to verify enhanced chat functionality
"""

import asyncio
from app.tools.enhanced_mcp_task_tools import EnhancedMCPTaskTools
from sqlmodel import create_engine, Session, SQLModel
from app.database.session import DATABASE_URL
from app.models.user import User
from app.models.task import Task
from app.core.auth import get_password_hash


def setup_test_user(session: Session) -> str:
    """Create a test user for testing"""
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        name="Test User"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user.id


def test_enhanced_features():
    """Test the enhanced features of the MCP tools"""
    print("Testing Enhanced MCP Task Tools...")

    # Create a test database session
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create a test user
        user_id = setup_test_user(session)

        # Initialize the enhanced tools
        tools = EnhancedMCPTaskTools(session, user_id)

        print("\n1. Testing enhanced add_task with priority and due date:")
        result = asyncio.run(tools.add_task(
            title="Buy groceries",
            description="Buy milk, bread, and eggs",
            priority="high",
            due_date=None
        ))
        print(f"   Result: {result['result']['message']}")
        task_id = result['result']['task']['id']

        print("\n2. Testing enhanced list_tasks with filtering:")
        result = asyncio.run(tools.list_tasks(status="pending", priority="high"))
        print(f"   Found {result['result']['count']} high-priority pending tasks")

        print("\n3. Testing enhanced update_task:")
        result = asyncio.run(tools.update_task(
            task_id=task_id,
            title="Buy groceries and vegetables",
            priority="medium"
        ))
        print(f"   Result: {result['result']['message']}")

        print("\n4. Testing enhanced complete_task:")
        result = asyncio.run(tools.complete_task(task_id=task_id, completed=True))
        print(f"   Result: {result['result']['message']}")

        print("\n5. Testing get_task_by_title:")
        task = asyncio.run(tools.get_task_by_title("groceries"))
        if task:
            print(f"   Found task: {task.title}")
        else:
            print("   Task not found")

        print("\n6. Testing error handling with invalid data:")
        result = asyncio.run(tools.add_task(
            title="Test invalid priority",
            priority="super_high"  # Invalid priority
        ))
        print(f"   Error handled: {result['message']}")

    print("\nEnhanced features test completed!")


if __name__ == "__main__":
    test_enhanced_features()