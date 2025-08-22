import asyncio
from datetime import datetime
from typing import Set
from models import Task
import os
import threading
import time

# Try to import winsound, with better fallback handling
try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False
    print("Warning: winsound not available. Using alternative sound methods.")

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


class RingingNotification:
    """A simple, reliable notification that works in production executables."""
    
    def __init__(self, task_title: str, task_description: str, due_date: datetime):
        self.task_title = task_title
        self.task_description = task_description
        self.due_date = due_date
        self.is_ringing = False
        self.ring_thread = None
    
    def start_ringing(self):
        """Start the ringing sound effect in a separate thread."""
        if self.is_ringing:
            return
        
        self.is_ringing = True
        self.ring_thread = threading.Thread(target=self._ring_loop, daemon=True)
        self.ring_thread.start()
    
    def stop_ringing(self):
        """Stop the ringing sound effect."""
        self.is_ringing = False
        if self.ring_thread:
            self.ring_thread.join(timeout=1.0)
    
    def _ring_loop(self):
        """Ring continuously until stopped."""
        ring_count = 0
        while self.is_ringing and ring_count < 30:  # Ring for max 30 seconds
            try:
                # Multiple sound methods for maximum compatibility
                self._play_ring_sound()
                ring_count += 1
                time.sleep(2)  # Ring every 2 seconds
            except Exception as e:
                print(f"Ring sound error: {e}")
                time.sleep(2)
    
    def _play_ring_sound(self):
        """Play a distinctive ring sound."""
        # Method 1: Try winsound with different frequencies for a ring effect
        if WINSOUND_AVAILABLE:
            try:
                # Create a ring pattern
                winsound.Beep(800, 200)   # Low tone
                time.sleep(0.1)
                winsound.Beep(1200, 200)  # High tone
                time.sleep(0.1)
                winsound.Beep(800, 200)   # Low tone
                return
            except Exception:
                pass
        
        # Method 2: Try PowerShell beep with ring pattern
        try:
            os.system('powershell -c "[console]::beep(800,200); Start-Sleep -m 100; [console]::beep(1200,200); Start-Sleep -m 100; [console]::beep(800,200)"')
            return
        except Exception:
            pass
        
        # Method 3: ASCII bell sequence
        try:
            print("\a\a\a")  # Multiple bell characters
            return
        except Exception:
            pass
        
        # Method 4: Visual ring indicator
        print("🔔 *RING* 🔔 *RING* 🔔 *RING* 🔔")


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
        
        # Store active ringing notifications
        self.active_ringing_notifications = {}
    
    def set_main_window(self, main_window):
        """Set reference to main window for popup positioning."""
        self.main_window = main_window
    
    def _play_notification_sound(self):
        """Play a notification sound to alert the user."""
        sound_played = False
        
        # Method 1: Try winsound if available
        if WINSOUND_AVAILABLE:
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
                sound_played = True
                print("🔊 Played notification sound (winsound)")
            except Exception as e:
                print(f"winsound.MessageBeep failed: {e}")
                try:
                    winsound.Beep(800, 500)  # 800Hz for 500ms
                    sound_played = True
                    print("🔊 Played notification sound (winsound beep)")
                except Exception as e2:
                    print(f"winsound.Beep failed: {e2}")
        
        # Method 2: Try system command for sound
        if not sound_played:
            try:
                os.system('powershell -c "[console]::beep(800,500)"')
                sound_played = True
                print("🔊 Played notification sound (PowerShell)")
            except Exception as e:
                print(f"PowerShell beep failed: {e}")
        
        # Method 3: Try ASCII bell character
        if not sound_played:
            try:
                print("\a")  # ASCII bell character
                sound_played = True
                print("🔊 Played notification sound (ASCII bell)")
            except Exception as e:
                print(f"ASCII bell failed: {e}")
        
        # Method 4: Visual indicator if all sound methods fail
        if not sound_played:
            print("🔔 *NOTIFICATION SOUND* 🔔")
            print("🔔 *NOTIFICATION SOUND* 🔔")
            print("🔔 *NOTIFICATION SOUND* 🔔")
    
    def _is_main_window_valid(self):
        """Check if the main window reference is still valid."""
        if self.main_window is None:
            return False
        
        try:
            # Try to access a property to check if the object is still valid
            _ = self.main_window.objectName()
            return True
        except (RuntimeError, AttributeError):
            # Object has been deleted or is invalid
            self.main_window = None
            return False
    
    def _show_emergency_popup(self, task: Task):
        """Show an emergency popup that will definitely work in production."""
        try:
            # Create a simple, reliable popup using tkinter (more reliable than PyQt in executables)
            import tkinter as tk
            from tkinter import messagebox
            
            # Create a simple popup
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            # Show the message box
            messagebox.showwarning(
                "🔔 TASKY ALERT - TASK DUE! 🔔",
                f"TASK: {task.title}\n\n"
                f"DESCRIPTION: {task.description or 'No description'}\n\n"
                f"DUE: {task.due_date.strftime('%Y-%m-%d %H:%M')}\n\n"
                "This task is now due! Please take action immediately!",
                parent=root
            )
            
            root.destroy()
            print(f"✅ Emergency popup shown for task: {task.title}")
            return True
            
        except ImportError:
            print("❌ tkinter not available for emergency popup")
            return False
        except Exception as e:
            print(f"❌ Emergency popup failed: {e}")
            return False
    
    def show_task_notification(self, task: Task) -> bool:
        """Show a notification for a due task."""
        try:
            print(f"\n🔔 Attempting to show notification for task: {task.title}")
            
            # Start ringing notification immediately
            ringing_notification = RingingNotification(task.title, task.description, task.due_date)
            ringing_notification.start_ringing()
            self.active_ringing_notifications[task.id] = ringing_notification
            
            # Play notification sound
            self._play_notification_sound()
            
            # Try custom popup first (most prominent) - with better error handling
            popup_shown = False
            if POPUP_AVAILABLE and self._is_main_window_valid():
                try:
                    popup = NotificationPopup(
                        task.title, 
                        task.description, 
                        task.due_date,
                        self.main_window
                    )
                    popup.show_popup()
                    print(f"✅ Custom popup shown for task: {task.title}")
                    popup_shown = True
                except Exception as e:
                    print(f"❌ Custom popup failed: {e}")
                    # Clear invalid main window reference
                    if "deleted" in str(e).lower():
                        self.main_window = None
                    # Continue to other notification methods
            
            # If custom popup failed, try emergency popup
            if not popup_shown:
                popup_shown = self._show_emergency_popup(task)
            
            # Try Windows toast notification with better error handling
            if self.toaster and WIN10TOAST_AVAILABLE:
                try:
                    title = f"🔔 TASK DUE: {task.title}"
                    
                    if task.description:
                        message = f"{task.description}\n\nDue: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
                    else:
                        message = f"Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
                    
                    # Show the notification with corrected parameters and better error handling
                    try:
                        self.toaster.show_toast(
                            title=title,
                            msg=message,
                            duration=15,  # Show for 15 seconds
                            threaded=True,  # Don't block the main thread
                            icon_path=None  # Use default icon
                        )
                        print(f"✅ Windows toast notification shown for task: {task.title}")
                    except (TypeError, Exception) as e:
                        # Fallback for older win10toast versions or other errors
                        try:
                            self.toaster.show_toast(
                                title=title,
                                msg=message,
                                duration=15,
                                threaded=True
                            )
                            print(f"✅ Windows toast notification shown for task: {task.title} (fallback)")
                        except Exception as e2:
                            print(f"❌ Windows toast notification fallback also failed: {e2}")
                            # Clear the toaster reference if it's causing issues
                            self.toaster = None
                except Exception as e:
                    print(f"❌ Windows toast notification failed: {e}")
                    # Clear the toaster reference if it's causing issues
                    self.toaster = None
            
            # Always show console notification as backup
            self._show_console_notification(task)
            
            # Mark this task as notified
            self.notified_tasks.add(task.id)
            print(f"✅ Task {task.title} marked as notified")
            
            # Stop ringing after a delay to allow user to see the notification
            def stop_ringing_delayed():
                time.sleep(10)  # Ring for 10 seconds
                if task.id in self.active_ringing_notifications:
                    self.active_ringing_notifications[task.id].stop_ringing()
                    del self.active_ringing_notifications[task.id]
            
            threading.Thread(target=stop_ringing_delayed, daemon=True).start()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to show notification for task {task.id}: {e}")
            # Try console notification as fallback
            try:
                self._play_notification_sound()
                self._show_console_notification(task)
                self.notified_tasks.add(task.id)
                print(f"✅ Fallback notification succeeded for task: {task.title}")
                return True
            except Exception as fallback_error:
                print(f"❌ Fallback notification also failed: {fallback_error}")
                return False
    
    def show_test_notification(self, title: str, message: str, notification_type: str = "info"):
        """Show a test notification for debugging purposes."""
        try:
            print(f"\n🧪 Showing test notification: {title}")
            
            # Play notification sound
            self._play_notification_sound()
            
            # Create a test task for the notification
            test_task = type('Task', (), {
                'id': 0,
                'title': title,
                'description': message,
                'due_date': datetime.now()
            })()
            
            # Try custom popup first
            popup_shown = False
            if POPUP_AVAILABLE and self._is_main_window_valid():
                try:
                    popup = NotificationPopup(
                        test_task.title, 
                        test_task.description, 
                        test_task.due_date,
                        self.main_window
                    )
                    popup.show_popup()
                    print(f"✅ Test custom popup shown")
                    popup_shown = True
                except Exception as e:
                    print(f"❌ Test custom popup failed: {e}")
            
            # If custom popup failed, try emergency popup
            if not popup_shown:
                popup_shown = self._show_emergency_popup(test_task)
            
            # Try Windows toast notification
            if self.toaster and WIN10TOAST_AVAILABLE:
                try:
                    self.toaster.show_toast(
                        title=f"🧪 TEST: {title}",
                        msg=message,
                        duration=10,
                        threaded=True,
                        icon_path=None
                    )
                    print(f"✅ Test Windows toast notification shown")
                except Exception as e:
                    print(f"❌ Test Windows toast notification failed: {e}")
            
            # Show console notification
            print("\n" + "="*60)
            print("🧪 TEST NOTIFICATION")
            print("="*60)
            print(f"Title: {title}")
            print(f"Message: {message}")
            print(f"Type: {notification_type}")
            print("="*60 + "\n")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to show test notification: {e}")
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
        
        # Stop any active ringing for this task
        if task_id in self.active_ringing_notifications:
            self.active_ringing_notifications[task_id].stop_ringing()
            del self.active_ringing_notifications[task_id]
    
    def stop_all_ringing(self):
        """Stop all active ringing notifications."""
        for ringing in self.active_ringing_notifications.values():
            ringing.stop_ringing()
        self.active_ringing_notifications.clear()
    
    async def check_and_notify_due_tasks(self, get_due_tasks_func):
        """Check for due tasks and show notifications."""
        print("🔄 Starting notification check loop...")
        check_count = 0
        
        while True:
            try:
                check_count += 1
                print(f"🔄 Check #{check_count}: Checking for due tasks...")
                
                # Get all due tasks
                due_tasks = get_due_tasks_func()
                print(f"📋 Found {len(due_tasks)} due tasks")
                
                # Show notifications for tasks that haven't been notified yet
                for task in due_tasks:
                    if not self.is_task_notified(task):
                        print(f"🔔 Task '{task.title}' is due and needs notification")
                        self.show_task_notification(task)
                    else:
                        print(f"✅ Task '{task.title}' already notified")
                
                # Wait for 1 minute before checking again
                print(f"⏰ Waiting 60 seconds before next check...")
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"❌ Error in notification check loop: {e}")
                print("⏰ Continuing in 60 seconds despite error...")
                await asyncio.sleep(60)  # Continue checking even if there's an error
