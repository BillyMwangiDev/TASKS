import sqlite3
import logging
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from models import Task, Category, PomodoroSession

logger = logging.getLogger(__name__)


def _row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        description=row["description"] or "",
        due_date=datetime.fromisoformat(row["due_date"]),
        completed=bool(row["completed"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        time_spent=row["time_spent"] or 0,
        started_at=datetime.fromisoformat(row["started_at"]) if row["started_at"] else None,
        priority=row["priority"] if row["priority"] is not None else 2,
        category_id=row["category_id"],
        tags=row["tags"] or "",
        is_recurring=bool(row["is_recurring"]),
        recurrence_rule=row["recurrence_rule"],
        parent_task_id=row["parent_task_id"],
        estimated_minutes=row["estimated_minutes"] or 0,
        notes=row["notes"] or "",
        completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
        sort_order=row["sort_order"] or 0,
    )


def _row_to_category(row: sqlite3.Row) -> Category:
    return Category(
        id=row["id"],
        name=row["name"],
        color=row["color"] or "#8b5cf6",
        icon=row["icon"] or "📁",
        is_archived=bool(row["is_archived"]),
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _row_to_session(row: sqlite3.Row) -> PomodoroSession:
    return PomodoroSession(
        id=row["id"],
        task_id=row["task_id"],
        started_at=datetime.fromisoformat(row["started_at"]),
        ended_at=datetime.fromisoformat(row["ended_at"]) if row["ended_at"] else None,
        duration_minutes=row["duration_minutes"] or 25,
        session_type=row["session_type"] or "work",
        completed=bool(row["completed"]),
    )


class DatabaseManager:
    """Manages SQLite database operations."""

    def __init__(self, db_path: str = "tasks.db"):
        resolved = Path(db_path).resolve()
        allowed_root = Path.home()
        if not str(resolved).startswith(str(allowed_root)):
            raise ValueError(f"db_path must be within the user home directory: {resolved}")
        self.db_path = str(resolved)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        with self._connect() as conn:
            self._create_tasks_table(conn)
            self._create_categories_table(conn)
            self._create_pomodoro_table(conn)
            self._create_daily_logs_table(conn)
            self._migrate_v2(conn)
            self._create_indexes(conn)
            conn.commit()

    def _create_indexes(self, conn: sqlite3.Connection):
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_category_id ON tasks(category_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_completed_at ON tasks(completed_at)")

    def _create_tasks_table(self, conn: sqlite3.Connection):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                time_spent INTEGER DEFAULT 0,
                started_at TEXT,
                priority INTEGER DEFAULT 2,
                category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
                tags TEXT DEFAULT '',
                is_recurring BOOLEAN DEFAULT 0,
                recurrence_rule TEXT,
                parent_task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
                estimated_minutes INTEGER DEFAULT 0,
                notes TEXT DEFAULT '',
                completed_at TEXT,
                sort_order INTEGER DEFAULT 0
            )
        """)

    def _create_categories_table(self, conn: sqlite3.Connection):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                color TEXT NOT NULL DEFAULT '#8b5cf6',
                icon TEXT DEFAULT '📁',
                is_archived BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

    def _create_pomodoro_table(self, conn: sqlite3.Connection):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pomodoro_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                duration_minutes INTEGER DEFAULT 25,
                session_type TEXT DEFAULT 'work',
                completed INTEGER DEFAULT 0
            )
        """)

    def _create_daily_logs_table(self, conn: sqlite3.Connection):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                total_tasks_completed INTEGER DEFAULT 0,
                total_focus_minutes INTEGER DEFAULT 0,
                notes TEXT
            )
        """)

    def _migrate_v2(self, conn: sqlite3.Connection):
        """Safely add v2 columns to existing tasks table."""
        cursor = conn.execute("PRAGMA table_info(tasks)")
        existing = {row["name"] for row in cursor.fetchall()}

        new_columns = [
            ("time_spent", "INTEGER DEFAULT 0"),
            ("started_at", "TEXT"),
            ("priority", "INTEGER DEFAULT 2"),
            ("category_id", "INTEGER"),
            ("tags", "TEXT DEFAULT ''"),
            ("is_recurring", "BOOLEAN DEFAULT 0"),
            ("recurrence_rule", "TEXT"),
            ("parent_task_id", "INTEGER"),
            ("estimated_minutes", "INTEGER DEFAULT 0"),
            ("notes", "TEXT DEFAULT ''"),
            ("completed_at", "TEXT"),
            ("sort_order", "INTEGER DEFAULT 0"),
        ]
        for col_name, col_def in new_columns:
            if col_name not in existing:
                conn.execute(f"ALTER TABLE tasks ADD COLUMN {col_name} {col_def}")

        # Category migration
        cursor = conn.execute("PRAGMA table_info(categories)")
        cat_existing = {row["name"] for row in cursor.fetchall()}
        if "is_archived" not in cat_existing:
            conn.execute("ALTER TABLE categories ADD COLUMN is_archived BOOLEAN DEFAULT 0")

    # ── Tasks ─────────────────────────────────────────────────────────────────

    def add_task(self, task: Task) -> int:
        with self._connect() as conn:
            cur = conn.execute("""
                INSERT INTO tasks (title, description, due_date, completed, created_at,
                    time_spent, started_at, priority, category_id, tags, is_recurring,
                    recurrence_rule, parent_task_id, estimated_minutes, notes, completed_at, sort_order)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                task.title, task.description, task.due_date.isoformat(),
                1 if task.completed else 0, (task.created_at or datetime.now()).isoformat(),
                task.time_spent,
                task.started_at.isoformat() if task.started_at else None,
                task.priority, task.category_id, task.tags,
                1 if task.is_recurring else 0, task.recurrence_rule,
                task.parent_task_id, task.estimated_minutes, task.notes,
                task.completed_at.isoformat() if task.completed_at else None,
                task.sort_order,
            ))
            conn.commit()
            return cur.lastrowid

    def get_all_tasks(self) -> List[Task]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE parent_task_id IS NULL ORDER BY sort_order ASC, due_date ASC"
            ).fetchall()
            return [_row_to_task(r) for r in rows]

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return _row_to_task(row) if row else None

    def update_task(self, task: Task) -> bool:
        if task.id is None:
            return False
        with self._connect() as conn:
            cur = conn.execute("""
                UPDATE tasks SET title=?, description=?, due_date=?, completed=?,
                    time_spent=?, started_at=?, priority=?, category_id=?, tags=?,
                    is_recurring=?, recurrence_rule=?, parent_task_id=?,
                    estimated_minutes=?, notes=?, completed_at=?, sort_order=?
                WHERE id=?
            """, (
                task.title, task.description, task.due_date.isoformat(),
                1 if task.completed else 0, task.time_spent,
                task.started_at.isoformat() if task.started_at else None,
                task.priority, task.category_id, task.tags,
                1 if task.is_recurring else 0, task.recurrence_rule,
                task.parent_task_id, task.estimated_minutes, task.notes,
                task.completed_at.isoformat() if task.completed_at else None,
                task.sort_order, task.id,
            ))
            conn.commit()
            return cur.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cur.rowcount > 0

    def duplicate_task(self, task_id: int) -> Optional[int]:
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        task.id = None
        task.title = f"{task.title} (copy)"
        task.completed = False
        task.completed_at = None
        task.started_at = None
        task.time_spent = 0
        task.created_at = datetime.now()
        return self.add_task(task)

    def mark_task_completed(self, task_id: int, completed: bool = True) -> bool:
        completed_at = datetime.now().isoformat() if completed else None
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE tasks SET completed=?, completed_at=? WHERE id=?",
                (1 if completed else 0, completed_at, task_id)
            )
            conn.commit()
            return cur.rowcount > 0

    def get_due_tasks(self) -> List[Task]:
        with self._connect() as conn:
            now = datetime.now().isoformat()
            rows = conn.execute(
                "SELECT * FROM tasks WHERE completed=0 AND due_date<=? ORDER BY due_date ASC",
                (now,)
            ).fetchall()
            return [_row_to_task(r) for r in rows]

    def get_tasks_due_today(self) -> List[Task]:
        with self._connect() as conn:
            today = date.today().isoformat()
            tomorrow = (date.today() + timedelta(days=1)).isoformat()
            rows = conn.execute(
                "SELECT * FROM tasks WHERE completed=0 AND due_date>=? AND due_date<? ORDER BY due_date ASC",
                (today, tomorrow)
            ).fetchall()
            return [_row_to_task(r) for r in rows]

    def get_tasks_due_this_week(self) -> List[Task]:
        with self._connect() as conn:
            today = date.today().isoformat()
            week_end = (date.today() + timedelta(days=7)).isoformat()
            rows = conn.execute(
                "SELECT * FROM tasks WHERE completed=0 AND due_date>=? AND due_date<? ORDER BY due_date ASC",
                (today, week_end)
            ).fetchall()
            return [_row_to_task(r) for r in rows]

    def get_overdue_tasks(self) -> List[Task]:
        with self._connect() as conn:
            now = datetime.now().isoformat()
            rows = conn.execute(
                "SELECT * FROM tasks WHERE completed=0 AND due_date<? ORDER BY due_date ASC",
                (now,)
            ).fetchall()
            return [_row_to_task(r) for r in rows]

    def get_tasks_by_category(self, category_id: Optional[int]) -> List[Task]:
        with self._connect() as conn:
            if category_id is None:
                rows = conn.execute(
                    "SELECT * FROM tasks WHERE category_id IS NULL ORDER BY due_date ASC"
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM tasks WHERE category_id=? ORDER BY due_date ASC",
                    (category_id,)
                ).fetchall()
            return [_row_to_task(r) for r in rows]

    def get_subtasks(self, parent_task_id: int) -> List[Task]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE parent_task_id=? ORDER BY sort_order ASC, created_at ASC",
                (parent_task_id,)
            ).fetchall()
            return [_row_to_task(r) for r in rows]

    def get_tasks_by_filter(
        self,
        priority: Optional[int] = None,
        category_id: Optional[int] = None,
        completed: Optional[bool] = None,
        search: Optional[str] = None,
        date_filter: Optional[str] = None,
        sort_by: str = "due_date",
    ) -> List[Task]:
        """Unified filter query for the main task list."""
        clauses = ["parent_task_id IS NULL"]
        params: List[Any] = []

        if priority is not None:
            clauses.append("priority=?")
            params.append(priority)
        if category_id is not None:
            clauses.append("category_id=?")
            params.append(category_id)
        if completed is not None:
            clauses.append("completed=?")
            params.append(1 if completed else 0)
        if search:
            clauses.append("(title LIKE ? OR description LIKE ? OR notes LIKE ? OR tags LIKE ?)")
            like = f"%{search}%"
            params.extend([like, like, like, like])

        now = datetime.now()
        today = date.today()
        if date_filter == "today":
            clauses.append("date(due_date)=?")
            params.append(today.isoformat())
            if completed is None:
                clauses.append("completed=0")
        elif date_filter == "tomorrow":
            clauses.append("date(due_date)=?")
            params.append((today + timedelta(days=1)).isoformat())
            if completed is None:
                clauses.append("completed=0")
        elif date_filter == "week":
            clauses.append("due_date>=? AND due_date<?")
            params.append(today.isoformat())
            params.append((today + timedelta(days=7)).isoformat())
            if completed is None:
                clauses.append("completed=0")
        elif date_filter == "overdue":
            clauses.append("due_date<?")
            params.append(now.isoformat())
            if completed is None:
                clauses.append("completed=0")

        _VALID_SORT = {
            "due_date": "due_date ASC",
            "priority": "priority ASC, due_date ASC",
            "created": "created_at DESC",
            "alpha": "title ASC",
            "sort_order": "sort_order ASC, due_date ASC",
        }
        if sort_by not in _VALID_SORT:
            raise ValueError(f"Invalid sort_by value: {sort_by!r}")
        order = _VALID_SORT[sort_by]

        where = " AND ".join(clauses)
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM tasks WHERE {where} ORDER BY {order}", params
            ).fetchall()
            return [_row_to_task(r) for r in rows]

    def get_tags_autocomplete(self) -> List[str]:
        with self._connect() as conn:
            rows = conn.execute("SELECT DISTINCT tags FROM tasks WHERE tags != ''").fetchall()
        tags: set = set()
        for row in rows:
            for tag in row["tags"].split(","):
                t = tag.strip()
                if t:
                    tags.add(t)
        return sorted(tags)

    # ── Categories ────────────────────────────────────────────────────────────

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
            return _row_to_category(row) if row else None

    def get_categories(self) -> List[Category]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM categories ORDER BY name ASC").fetchall()
            return [_row_to_category(r) for r in rows]

    def add_category(self, category: Category) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO categories (name, color, icon, is_archived, created_at) VALUES (?,?,?,?,?)",
                (category.name, category.color, category.icon, 1 if category.is_archived else 0,
                 (category.created_at or datetime.now()).isoformat())
            )
            conn.commit()
            return cur.lastrowid

    def update_category(self, category: Category) -> bool:
        if category.id is None:
            return False
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE categories SET name=?, color=?, icon=?, is_archived=? WHERE id=?",
                (category.name, category.color, category.icon, 1 if category.is_archived else 0, category.id)
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_category(self, category_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM categories WHERE id=?", (category_id,))
            conn.commit()
            return cur.rowcount > 0

    def get_task_count_by_category(self) -> Dict[Optional[int], int]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT category_id, COUNT(*) as cnt FROM tasks WHERE completed=0 GROUP BY category_id"
            ).fetchall()
            return {r["category_id"]: r["cnt"] for r in rows}

    # ── Pomodoro ──────────────────────────────────────────────────────────────

    def add_pomodoro_session(self, session: PomodoroSession) -> int:
        with self._connect() as conn:
            cur = conn.execute("""
                INSERT INTO pomodoro_sessions
                    (task_id, started_at, ended_at, duration_minutes, session_type, completed)
                VALUES (?,?,?,?,?,?)
            """, (
                session.task_id, session.started_at.isoformat(),
                session.ended_at.isoformat() if session.ended_at else None,
                session.duration_minutes, session.session_type,
                1 if session.completed else 0,
            ))
            conn.commit()
            return cur.lastrowid

    def get_sessions_for_task(self, task_id: int) -> List[PomodoroSession]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM pomodoro_sessions WHERE task_id=? ORDER BY started_at DESC",
                (task_id,)
            ).fetchall()
            return [_row_to_session(r) for r in rows]

    def get_recent_focus_sessions(self, days: int = 30) -> List[PomodoroSession]:
        cutoff = (datetime.now() - timedelta(days=days)).date().isoformat()
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM pomodoro_sessions WHERE date(started_at)>=? ORDER BY started_at DESC",
                (cutoff,),
            ).fetchall()
            return [_row_to_session(r) for r in rows]

    def get_total_pomodoro_minutes_today(self) -> int:
        with self._connect() as conn:
            today = date.today().isoformat()
            row = conn.execute("""
                SELECT COALESCE(SUM(duration_minutes), 0) as total
                FROM pomodoro_sessions
                WHERE completed=1 AND date(started_at)=?
            """, (today,)).fetchone()
            return row["total"] if row else 0

    # ── Analytics ─────────────────────────────────────────────────────────────

    def get_analytics_data(self, days: int = 7) -> Dict[str, Any]:
        """Return data for the analytics dashboard."""
        with self._connect() as conn:
            today = date.today()
            window_start = (today - timedelta(days=days - 1)).isoformat()

            # Seed every day in range with 0 so gaps show up correctly
            daily_completions: Dict[str, int] = {
                (today - timedelta(days=i)).isoformat(): 0 for i in range(days)
            }
            daily_focus: Dict[str, int] = dict(daily_completions)

            # Single batch query for completions
            for row in conn.execute(
                "SELECT date(completed_at) as d, COUNT(*) as cnt "
                "FROM tasks WHERE completed=1 AND date(completed_at)>=? "
                "GROUP BY d",
                (window_start,),
            ).fetchall():
                if row["d"] in daily_completions:
                    daily_completions[row["d"]] = row["cnt"]

            # Single batch query for focus minutes
            for row in conn.execute(
                "SELECT date(started_at) as d, COALESCE(SUM(duration_minutes),0) as total "
                "FROM pomodoro_sessions WHERE completed=1 AND date(started_at)>=? "
                "GROUP BY d",
                (window_start,),
            ).fetchall():
                if row["d"] in daily_focus:
                    daily_focus[row["d"]] = row["total"]

            # Time per category
            cat_rows = conn.execute("""
                SELECT c.name, c.color, COALESCE(SUM(t.time_spent),0) as total_minutes
                FROM categories c
                LEFT JOIN tasks t ON t.category_id=c.id
                GROUP BY c.id
            """).fetchall()
            time_by_category = [
                {"name": r["name"], "color": r["color"], "minutes": r["total_minutes"]}
                for r in cat_rows
            ]

            # Streak: fetch all completed-at dates once, then count in Python
            completed_dates = {
                row["d"]
                for row in conn.execute(
                    "SELECT DISTINCT date(completed_at) as d FROM tasks WHERE completed=1 AND completed_at IS NOT NULL"
                ).fetchall()
            }
            streak = 0
            check_date = today
            while check_date.isoformat() in completed_dates:
                streak += 1
                check_date -= timedelta(days=1)

            # Overall totals
            total_row = conn.execute(
                "SELECT COUNT(*) as total, SUM(completed) as done FROM tasks"
            ).fetchone()
            total = total_row["total"] or 0
            done = total_row["done"] or 0

            return {
                "daily_completions": daily_completions,
                "daily_focus": daily_focus,
                "time_by_category": time_by_category,
                "streak": streak,
                "total_tasks": total,
                "completed_tasks": done,
                "completion_rate": round(done / total * 100) if total > 0 else 0,
            }

    def get_most_productive_hours(self) -> Dict[int, int]:
        """Returns dict of hour -> number of tasks completed in that hour."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT strftime('%H', completed_at) as hr, COUNT(*) as cnt FROM tasks WHERE completed=1 AND completed_at IS NOT NULL GROUP BY hr"
            ).fetchall()
            return {int(r["hr"]): r["cnt"] for r in rows}

    # ── Misc ──────────────────────────────────────────────────────────────────

    def close(self):
        pass  # Connections are closed via context manager; nothing persistent to close.
