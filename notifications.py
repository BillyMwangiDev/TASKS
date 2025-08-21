import asyncio
from datetime import datetime
from typing import Set
from models import Task
import winsound
import os

# Try to import win10toast, fallback to console notifications if not available
try:
    from win10toast import ToastNotifier
    WIN10TOAST_AVAILABLE = True
except ImportError:
    WIN10TOAST_AVAILABLE = False
    print("Warning: win10toast not available. Using console notifications instead.")

# Try to import the custom popup
try:
    from ui.notification_popup import NotificationPopup
    POPUP_AVAILABLE = True
except ImportError:
    POPUP_AVAILABLE = False
    print("Warning: Custom popup not available. Using standard notifications.")


class NotificationManager:
    """Manages Windows notifications for due tasks."""
    
    def __init__(self):
        """Initialize the notification manager."""
        self.notified_tasks: Set[int] = set()  # Track which tasks have been notified
        
        if WIN10TOAST_AVAILABLE:
            try:
                self.toaster = ToastNotifier()
            except Exception as e:
                print(f"Warning: Failed to initialize win10toast: {e}")
                self.toaster = None
        else:
            self.toaster = None
        
        # Store reference to main window for popup positioning
        self.main_window = None
    
    def set_main_window(self, main_window):
        """Set reference to main window for popup positioning."""
        self.main_window = main_window
    
    def _play_notification_sound(self):
        """Play a notification sound to alert the user."""
        try:
            # Play Windows notification sound (SystemAsterisk)
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception as e:
            try:
                # Fallback to simple beep
                winsound.Beep(800, 500)  # 800Hz for 500ms
            except Exception:
                # If all else fails, just print a sound indicator
                print("\a")  # ASCII bell character
                print("🔔 *NOTIFICATION SOUND* 🔔")
    
    def show_task_notification(self, task: Task) -> bool:
        """Show a notification for a due task."""
        try:
            # Play notification sound first
            self._play_notification_sound()
            
            # Try custom popup first (most prominent)
            if POPUP_AVAILABLE and self.main_window:
                try:
                    popup = NotificationPopup(
                        task.title, 
                        task.description, 
                        task.due_date,
                        self.main_window
                    )
                    popup.show_popup()
                    print(f"Custom popup shown for task: {task.title}")
                except Exception as e:
                    print(f"Custom popup failed: {e}")
                    # Fall back to other notification methods
            
            # Try Windows toast notification
            if self.toaster and WIN10TOAST_AVAILABLE:
                try:
                    title = f"🔔 TASK DUE: {task.title}"
                    
                    if task.description:
                        message = f"{task.description}\n\nDue: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
                    else:
                        message = f"Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
                    
                    # Show the notification with corrected parameters
                    try:
                        self.toaster.show_toast(
                            title=title,
                            msg=message,
                            duration=15,  # Show for 15 seconds
                            threaded=True,  # Don't block the main thread
                            icon_path=None  # Use default icon
                        )
                    except TypeError:
                        # Fallback for older win10toast versions
                        self.toaster.show_toast(
                            title=title,
                            msg=message,
                            duration=15,
                            threaded=True
                        )
                except Exception as e:
                    print(f"Windows toast notification failed: {e}")
            
            # Always show console notification as backup
            self._show_console_notification(task)
            
            # Mark this task as notified
            self.notified_tasks.add(task.id)
            return True
            
        except Exception as e:
            print(f"Failed to show notification for task {task.id}: {e}")
            # Try console notification as fallback
            try:
                self._play_notification_sound()
                self._show_console_notification(task)
                self.notified_tasks.add(task.id)
                return True
            except Exception as fallback_error:
                print(f"Fallback notification also failed: {fallback_error}")
                return False
    
    def _show_console_notification(self, task: Task):
        """Show a console notification as fallback."""
        print("\n" + "="*60)
        print("🔔 TASK DUE NOTIFICATION")
        print("="*60)
        print(f"Title: {task.title}")
        if task.description:
            print(f"Description: {task.description}")
        print(f"Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
        print("="*60 + "\n")
    
    def is_task_notified(self, task: Task) -> bool:
        """Check if a task has already been notified."""
        return task.id in self.notified_tasks
    
    def clear_notified_tasks(self):
        """Clear the list of notified tasks (useful for daily reset)."""
        self.notified_tasks.clear()
    
    def reset_notification_for_task(self, task_id: int):
        """Reset notification status for a specific task (e.g., when it's edited)."""
        if task_id in self.notified_tasks:
            self.notified_tasks.remove(task_id)
    
    async def check_and_notify_due_tasks(self, get_due_tasks_func):
        """Check for due tasks and show notifications."""
        while True:
            try:
                # Get all due tasks
                due_tasks = get_due_tasks_func()
                
                # Show notifications for tasks that haven't been notified yet
                for task in due_tasks:
                    if not self.is_task_notified(task):
                        self.show_task_notification(task)
                
                # Wait for 1 minute before checking again
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"Error in notification check loop: {e}")
                await asyncio.sleep(60)  # Continue checking even if there's an error
