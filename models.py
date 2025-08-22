from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Data class representing a task in the productivity app."""
    id: Optional[int]
    title: str
    description: str
    due_date: datetime
    completed: bool
    created_at: Optional[datetime] = None
    time_spent: int = 0  # Time spent in minutes
    started_at: Optional[datetime] = None  # When task was started
    
    def __post_init__(self):
        """Initialize created_at if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def is_due(self) -> bool:
        """Check if the task is due (past due date and not completed)."""
        return not self.completed and datetime.now() >= self.due_date
    
    def is_overdue(self) -> bool:
        """Check if the task is overdue (past due date and not completed)."""
        return not self.completed and datetime.now() > self.due_date
    
    def time_until_due(self) -> str:
        """Get human-readable time until due or overdue status."""
        if self.completed:
            return "Completed"
        
        now = datetime.now()
        if self.due_date > now:
            delta = self.due_date - now
            if delta.days > 0:
                return f"Due in {delta.days} day(s)"
            elif delta.seconds > 3600:
                hours = delta.seconds // 3600
                return f"Due in {hours} hour(s)"
            else:
                minutes = delta.seconds // 60
                return f"Due in {minutes} minute(s)"
        else:
            delta = now - self.due_date
            if delta.days > 0:
                return f"Overdue by {delta.days} day(s)"
            elif delta.seconds > 3600:
                hours = delta.seconds // 3600
                return f"Overdue by {hours} hour(s)"
            else:
                minutes = delta.seconds // 60
                return f"Overdue by {minutes} minute(s)"
    
    def start_tracking(self):
        """Start time tracking for this task."""
        if not self.completed and self.started_at is None:
            self.started_at = datetime.now()
    
    def stop_tracking(self):
        """Stop time tracking and add to total time spent."""
        if self.started_at is not None:
            delta = datetime.now() - self.started_at
            self.time_spent += int(delta.total_seconds() // 60)
            self.started_at = None
    
    def get_time_spent_formatted(self) -> str:
        """Get formatted time spent string."""
        if self.time_spent == 0:
            return "0m"
        
        hours = self.time_spent // 60
        minutes = self.time_spent % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def is_tracking(self) -> bool:
        """Check if task is currently being tracked."""
        return self.started_at is not None
