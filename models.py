from dataclasses import dataclass
from datetime import datetime, date
from enum import IntEnum
from typing import Optional, Tuple


class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    NONE = 4


# Keep legacy aliases so existing callers don't break.
PRIORITY_HIGH = Priority.HIGH
PRIORITY_MEDIUM = Priority.MEDIUM
PRIORITY_LOW = Priority.LOW
PRIORITY_NONE = Priority.NONE

PRIORITY_COLORS = {
    Priority.HIGH: "#ef4444",
    Priority.MEDIUM: "#f59e0b",
    Priority.LOW: "#3b82f6",
    Priority.NONE: "#6b7280",
}

PRIORITY_LABELS = {
    Priority.HIGH: "High",
    Priority.MEDIUM: "Medium",
    Priority.LOW: "Low",
    Priority.NONE: "None",
}


@dataclass
class Task:
    """Data class representing a task."""
    id: Optional[int]
    title: str
    description: str
    due_date: datetime
    completed: bool
    created_at: Optional[datetime] = None
    time_spent: int = 0
    started_at: Optional[datetime] = None
    # v2 fields
    priority: int = PRIORITY_MEDIUM
    category_id: Optional[int] = None
    tags: str = ""
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
    parent_task_id: Optional[int] = None
    estimated_minutes: int = 0
    notes: str = ""
    completed_at: Optional[datetime] = None
    sort_order: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def is_due(self) -> bool:
        return not self.completed and datetime.now() >= self.due_date

    def is_overdue(self) -> bool:
        return not self.completed and datetime.now() > self.due_date

    def is_due_today(self) -> bool:
        return not self.completed and self.due_date.date() == date.today()

    def time_until_due(self) -> str:
        """Return human-readable time string."""
        text, _ = self.time_until_due_with_urgency()
        return text

    def time_until_due_with_urgency(self) -> Tuple[str, str]:
        """Return (human-readable text, urgency_level).
        urgency_level: 'completed' | 'overdue' | 'today' | 'soon' | 'future'
        """
        if self.completed:
            return "Completed", "completed"

        now = datetime.now()
        if self.due_date > now:
            delta = self.due_date - now
            if delta.days > 7:
                return f"Due in {delta.days} days", "future"
            elif delta.days > 0:
                return f"Due in {delta.days} day(s)", "soon"
            elif delta.seconds > 3600:
                hours = delta.seconds // 3600
                return f"Due in {hours}h", "today"
            else:
                minutes = delta.seconds // 60
                return f"Due in {minutes}m", "today"
        else:
            delta = now - self.due_date
            if delta.days > 0:
                return f"Overdue {delta.days}d", "overdue"
            elif delta.seconds > 3600:
                hours = delta.seconds // 3600
                return f"Overdue {hours}h", "overdue"
            else:
                minutes = delta.seconds // 60
                return f"Overdue {minutes}m", "overdue"

    def priority_label(self) -> Tuple[str, str]:
        """Return (label, color_hex) for this task's priority."""
        return PRIORITY_LABELS.get(self.priority, "None"), PRIORITY_COLORS.get(self.priority, "#6b7280")

    def start_tracking(self):
        if not self.completed and self.started_at is None:
            self.started_at = datetime.now()

    def stop_tracking(self):
        if self.started_at is not None:
            delta = datetime.now() - self.started_at
            self.time_spent += int(delta.total_seconds() // 60)
            self.started_at = None

    def get_time_spent_formatted(self) -> str:
        if self.time_spent == 0:
            return "0m"
        hours = self.time_spent // 60
        minutes = self.time_spent % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    def is_tracking(self) -> bool:
        return self.started_at is not None


@dataclass
class Category:
    """A user-defined project/category for grouping tasks."""
    id: Optional[int]
    name: str
    color: str = "#8b5cf6"
    icon: str = "📁"
    is_archived: bool = False
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PomodoroSession:
    """A single Pomodoro work or break session linked to a task."""
    id: Optional[int]
    task_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_minutes: int = 25
    session_type: str = "work"
    completed: bool = False
