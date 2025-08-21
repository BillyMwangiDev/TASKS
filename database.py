import sqlite3
import os
from datetime import datetime
from typing import List, Optional
from models import Task


class DatabaseManager:
    """Manages SQLite database operations for tasks."""
    
    def __init__(self, db_path: str = "tasks.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """Create the tasks table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            ''')
            conn.commit()
    
    def add_task(self, task: Task) -> int:
        """Add a new task to the database and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (title, description, due_date, completed, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                task.title,
                task.description,
                task.due_date.isoformat(),
                1 if task.completed else 0,
                task.created_at.isoformat()
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, description, due_date, completed, created_at
                FROM tasks
                ORDER BY due_date ASC
            ''')
            
            tasks = []
            for row in cursor.fetchall():
                task = Task(
                    id=row[0],
                    title=row[1],
                    description=row[2] or "",
                    due_date=datetime.fromisoformat(row[3]),
                    completed=bool(row[4]),
                    created_at=datetime.fromisoformat(row[5])
                )
                tasks.append(task)
            
            return tasks
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a specific task by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, description, due_date, completed, created_at
                FROM tasks
                WHERE id = ?
            ''', (task_id,))
            
            row = cursor.fetchone()
            if row:
                return Task(
                    id=row[0],
                    title=row[1],
                    description=row[2] or "",
                    due_date=datetime.fromisoformat(row[3]),
                    completed=bool(row[4]),
                    created_at=datetime.fromisoformat(row[5])
                )
            return None
    
    def update_task(self, task: Task) -> bool:
        """Update an existing task in the database."""
        if task.id is None:
            return False
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET title = ?, description = ?, due_date = ?, completed = ?
                WHERE id = ?
            ''', (
                task.title,
                task.description,
                task.due_date.isoformat(),
                1 if task.completed else 0,
                task.id
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_due_tasks(self) -> List[Task]:
        """Get all tasks that are due (not completed and due date has passed)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute('''
                SELECT id, title, description, due_date, completed, created_at
                FROM tasks
                WHERE completed = 0 AND due_date <= ?
                ORDER BY due_date ASC
            ''', (now,))
            
            tasks = []
            for row in cursor.fetchall():
                task = Task(
                    id=row[0],
                    title=row[1],
                    description=row[2] or "",
                    due_date=datetime.fromisoformat(row[3]),
                    completed=bool(row[4]),
                    created_at=datetime.fromisoformat(row[5])
                )
                tasks.append(task)
            
            return tasks
    
    def mark_task_completed(self, task_id: int, completed: bool = True) -> bool:
        """Mark a task as completed or uncompleted."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET completed = ?
                WHERE id = ?
            ''', (1 if completed else 0, task_id))
            conn.commit()
            return cursor.rowcount > 0
