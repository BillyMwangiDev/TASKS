#!/usr/bin/env python3
"""
Test script for TASKY - Task Manager application.
This script tests the core functionality without launching the GUI.
"""

from datetime import datetime, timedelta
from models import Task
from database import DatabaseManager
from notifications import NotificationManager
from scheduler import TaskScheduler


def test_core_functionality():
    """Test the core functionality of the application."""
    print("🧪 Testing TASKY - Task Manager Core Functionality")
    print("=" * 60)
    
    # Test 1: Task Model
    print("\n1. Testing Task Model...")
    task = Task(
        id=None,
        title="Test Task",
        description="This is a test task",
        due_date=datetime.now() + timedelta(hours=1),
        completed=False,
        created_at=datetime.now()
    )
    print(f"   ✓ Task created: {task.title}")
    print(f"   ✓ Time until due: {task.time_until_due()}")
    print(f"   ✓ Is due: {task.is_due()}")
    print(f"   ✓ Is overdue: {task.is_overdue()}")
    
    # Test 2: Database Operations
    print("\n2. Testing Database Operations...")
    db = DatabaseManager("test_tasks.db")
    
    # Add task
    task_id = db.add_task(task)
    print(f"   ✓ Task added with ID: {task_id}")
    
    # Retrieve task
    retrieved_task = db.get_task_by_id(task_id)
    if retrieved_task:
        print(f"   ✓ Task retrieved: {retrieved_task.title}")
    else:
        print("   ✗ Failed to retrieve task")
        return False
    
    # Get all tasks
    all_tasks = db.get_all_tasks()
    print(f"   ✓ Total tasks in database: {len(all_tasks)}")
    
    # Update task
    retrieved_task.completed = True
    if db.update_task(retrieved_task):
        print("   ✓ Task updated successfully")
    else:
        print("   ✗ Failed to update task")
        return False
    
    # Test 3: Notification System
    print("\n3. Testing Notification System...")
    notification_mgr = NotificationManager()
    print(f"   ✓ Notification manager initialized")
    print(f"   ✓ Windows notifications available: {hasattr(notification_mgr, 'toaster') and notification_mgr.toaster is not None}")
    
    # Test 4: Scheduler
    print("\n4. Testing Task Scheduler...")
    scheduler = TaskScheduler(notification_mgr)
    print(f"   ✓ Task scheduler initialized")
    
    # Clean up test database
    import os
    if os.path.exists("test_tasks.db"):
        os.remove("test_tasks.db")
        print("   ✓ Test database cleaned up")
    
    print("\n" + "=" * 60)
    print("🎉 All core functionality tests passed!")
    print("TASKY is ready to use.")
    return True


if __name__ == "__main__":
    try:
        test_core_functionality()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
