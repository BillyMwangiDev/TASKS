import asyncio
import threading
import time
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
        self.scheduler_thread = None
    
    def start(self, get_due_tasks_func: Callable):
        """Start the background scheduler in a separate thread."""
        if self.is_running:
            print("🔄 Scheduler already running, skipping start request")
            return
        
        with self._lock:
            if self.is_running:
                print("🔄 Scheduler already running, skipping start request")
                return
            
            print("🚀 Starting notification scheduler...")
            self.is_running = True
            
            # Create a new thread for the asyncio event loop
            def run_scheduler():
                try:
                    print("🔄 Creating new asyncio event loop in scheduler thread")
                    
                    # Create a new event loop for this thread
                    self.loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self.loop)
                    
                    print("🔄 Starting notification check task")
                    
                    # Start the notification check task
                    self.scheduler_task = self.loop.create_task(
                        self.notification_manager.check_and_notify_due_tasks(get_due_tasks_func)
                    )
                    
                    print("🔄 Running asyncio event loop")
                    
                    # Run the event loop
                    self.loop.run_forever()
                    
                except Exception as e:
                    print(f"❌ Error in scheduler thread: {e}")
                    import traceback
                    traceback.print_exc()
                finally:
                    print("🔄 Cleaning up scheduler thread")
                    if self.loop and not self.loop.is_closed():
                        try:
                            self.loop.close()
                        except Exception as e:
                            print(f"❌ Error closing event loop: {e}")
            
            # Start the scheduler thread
            self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True, name="TaskScheduler")
            self.scheduler_thread.start()
            
            print(f"✅ Scheduler started successfully in thread: {self.scheduler_thread.name}")
    
    def stop(self):
        """Stop the background scheduler."""
        if not self.is_running:
            print("🔄 Scheduler not running, skipping stop request")
            return
        
        with self._lock:
            if not self.is_running:
                print("🔄 Scheduler not running, skipping stop request")
                return
            
            print("🛑 Stopping notification scheduler...")
            self.is_running = False
            
            if self.loop and not self.loop.is_closed():
                try:
                    # Cancel the scheduler task
                    if self.scheduler_task and not self.scheduler_task.done():
                        print("🔄 Cancelling scheduler task")
                        self.scheduler_task.cancel()
                    
                    # Stop the event loop
                    print("🔄 Stopping event loop")
                    self.loop.call_soon_threadsafe(self.loop.stop)
                    
                    # Wait a bit for the loop to stop
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"❌ Error stopping event loop: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Wait for thread to finish
            if self.scheduler_thread and self.scheduler_thread.is_alive():
                print("🔄 Waiting for scheduler thread to finish...")
                self.scheduler_thread.join(timeout=2.0)
                if self.scheduler_thread.is_alive():
                    print("⚠️ Scheduler thread did not finish within timeout")
                else:
                    print("✅ Scheduler thread finished successfully")
    
    def is_active(self) -> bool:
        """Check if the scheduler is currently running."""
        return self.is_running
    
    def get_status(self) -> dict:
        """Get detailed status of the scheduler."""
        status = {
            "is_running": self.is_running,
            "thread_alive": self.scheduler_thread.is_alive() if self.scheduler_thread else False,
            "loop_active": self.loop and not self.loop.is_closed() if self.loop else False,
            "task_active": self.scheduler_task and not self.scheduler_task.done() if self.scheduler_task else False
        }
        
        if self.scheduler_thread:
            status["thread_name"] = self.scheduler_thread.name
            status["thread_id"] = self.scheduler_thread.ident
        
        return status
    
    def restart(self, get_due_tasks_func: Callable):
        """Restart the scheduler."""
        print("🔄 Restarting notification scheduler...")
        self.stop()
        
        # Give it a moment to fully stop
        time.sleep(0.5)
        
        # Check if it actually stopped
        if self.is_running:
            print("⚠️ Scheduler did not stop properly, forcing restart...")
            self.is_running = False
            time.sleep(0.5)
        
        self.start(get_due_tasks_func)
    
    def force_restart(self, get_due_tasks_func: Callable):
        """Force restart the scheduler by killing the thread and starting fresh."""
        print("🔄 Force restarting notification scheduler...")
        
        # Force stop
        self.is_running = False
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            print("⚠️ Force stopping scheduler thread...")
            # Note: We can't actually kill a thread in Python, but we can stop the loop
            if self.loop and not self.loop.is_closed():
                try:
                    self.loop.call_soon_threadsafe(self.loop.stop)
                except:
                    pass
        
        # Wait longer for cleanup
        time.sleep(1.0)
        
        # Start fresh
        self.start(get_due_tasks_func)
