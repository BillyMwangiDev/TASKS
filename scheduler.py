import asyncio
import threading
from typing import Callable
from notifications import NotificationManager


class TaskScheduler:
    """Manages the background asyncio task for checking due tasks."""
    
    def __init__(self, notification_manager: NotificationManager):
        """Initialize the task scheduler."""
        self.notification_manager = notification_manager
        self.loop = None
        self.scheduler_task = None
        self.is_running = False
        self._lock = threading.Lock()
    
    def start(self, get_due_tasks_func: Callable):
        """Start the background scheduler in a separate thread."""
        if self.is_running:
            return
        
        with self._lock:
            if self.is_running:
                return
            
            self.is_running = True
            
            # Create a new thread for the asyncio event loop
            def run_scheduler():
                try:
                    # Create a new event loop for this thread
                    self.loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self.loop)
                    
                    # Start the notification check task
                    self.scheduler_task = self.loop.create_task(
                        self.notification_manager.check_and_notify_due_tasks(get_due_tasks_func)
                    )
                    
                    # Run the event loop
                    self.loop.run_forever()
                    
                except Exception as e:
                    print(f"Error in scheduler thread: {e}")
                finally:
                    if self.loop and not self.loop.is_closed():
                        self.loop.close()
            
            # Start the scheduler thread
            scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            scheduler_thread.start()
    
    def stop(self):
        """Stop the background scheduler."""
        if not self.is_running:
            return
        
        with self._lock:
            if not self.is_running:
                return
            
            self.is_running = False
            
            if self.loop and not self.loop.is_closed():
                # Cancel the scheduler task
                if self.scheduler_task and not self.scheduler_task.done():
                    self.scheduler_task.cancel()
                
                # Stop the event loop
                try:
                    self.loop.call_soon_threadsafe(self.loop.stop)
                except Exception as e:
                    print(f"Error stopping event loop: {e}")
    
    def is_active(self) -> bool:
        """Check if the scheduler is currently running."""
        return self.is_running
    
    def restart(self, get_due_tasks_func: Callable):
        """Restart the scheduler."""
        self.stop()
        # Give it a moment to fully stop
        import time
        time.sleep(0.1)
        self.start(get_due_tasks_func)
