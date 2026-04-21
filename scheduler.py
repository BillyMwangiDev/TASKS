import asyncio
import logging
import threading
import time
from typing import Callable
from notifications import NotificationManager

logger = logging.getLogger(__name__)


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
            return

        with self._lock:
            if self.is_running:
                return

            logger.info("Starting notification scheduler")
            self.is_running = True

            def run_scheduler():
                try:
                    self.loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self.loop)
                    self.scheduler_task = self.loop.create_task(
                        self.notification_manager.check_and_notify_due_tasks(get_due_tasks_func)
                    )
                    self.loop.run_forever()
                except Exception as e:
                    logger.exception("Scheduler thread error: %s", e)
                finally:
                    if self.loop and not self.loop.is_closed():
                        try:
                            self.loop.close()
                        except Exception as e:
                            logger.warning("Error closing event loop: %s", e)

            self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True, name="TaskScheduler")
            self.scheduler_thread.start()
            logger.info("Scheduler started in thread: %s", self.scheduler_thread.name)

    def stop(self):
        """Stop the background scheduler."""
        if not self.is_running:
            return

        with self._lock:
            if not self.is_running:
                return

            logger.info("Stopping notification scheduler")
            self.is_running = False

            if self.loop and not self.loop.is_closed():
                try:
                    if self.scheduler_task and not self.scheduler_task.done():
                        self.scheduler_task.cancel()
                    self.loop.call_soon_threadsafe(self.loop.stop)
                    time.sleep(0.5)
                except Exception as e:
                    logger.warning("Error stopping event loop: %s", e)

            if self.scheduler_thread and self.scheduler_thread.is_alive():
                self.scheduler_thread.join(timeout=2.0)
                if self.scheduler_thread.is_alive():
                    logger.warning("Scheduler thread did not finish within timeout")

    def is_active(self) -> bool:
        return self.is_running

    def get_status(self) -> dict:
        status = {
            "is_running": self.is_running,
            "thread_alive": self.scheduler_thread.is_alive() if self.scheduler_thread else False,
            "loop_active": self.loop and not self.loop.is_closed() if self.loop else False,
            "task_active": self.scheduler_task and not self.scheduler_task.done() if self.scheduler_task else False,
        }
        if self.scheduler_thread:
            status["thread_name"] = self.scheduler_thread.name
            status["thread_id"] = self.scheduler_thread.ident
        return status

    def restart(self, get_due_tasks_func: Callable):
        logger.info("Restarting notification scheduler")
        self.stop()
        time.sleep(0.5)
        if self.is_running:
            self.is_running = False
            time.sleep(0.5)
        self.start(get_due_tasks_func)

    def force_restart(self, get_due_tasks_func: Callable):
        logger.info("Force restarting notification scheduler")
        self.is_running = False
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            if self.loop and not self.loop.is_closed():
                try:
                    self.loop.call_soon_threadsafe(self.loop.stop)
                except Exception:
                    pass
        time.sleep(1.0)
        self.start(get_due_tasks_func)
