from PyQt6.QtCore import QObject, pyqtSignal

class NotificationSignals(QObject):
    """Global signals for cross-thread notification events."""
    
    # Signal emitted when a task notification should be shown
    # Arguments: task_id (int), title (str), description (str), due_date (datetime)
    show_notification_popup = pyqtSignal(int, str, str, object)

# Global instance to be shared across threads
notification_signals = NotificationSignals()
