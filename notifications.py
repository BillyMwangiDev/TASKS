import asyncio
import base64
import logging
import os
import sys
import threading
import time
from datetime import datetime
from typing import Dict, Set

from models import Task
from config import (
    NOTIFICATION_CHECK_INTERVAL_S,
    NOTIFICATION_RING_BEEP_HZ_HI,
    NOTIFICATION_RING_BEEP_HZ_LO,
    NOTIFICATION_RING_BEEP_MS,
    NOTIFICATION_RING_COUNT,
    NOTIFICATION_RING_FALLBACK_PAUSE_S,
    NOTIFICATION_RING_PAUSE_S,
    NOTIFICATION_STOP_AFTER_S,
    NOTIFICATION_TOAST_MAX_CHARS,
)

logger = logging.getLogger(__name__)

# Platform Detection
IS_WINDOWS = sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"

try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False

try:
    if IS_WINDOWS:
        from winotify import Notification, audio
        WINOTIFY_AVAILABLE = True
    else:
        WINOTIFY_AVAILABLE = False
except ImportError:
    WINOTIFY_AVAILABLE = False

try:
    from ui.signals import notification_signals
    SIGNALS_AVAILABLE = True
except ImportError:
    SIGNALS_AVAILABLE = False


class NotificationManager:
    """Manages task due notifications — cross-platform (Windows & macOS)."""

    def __init__(self):
        self.notified_tasks: Set[int] = set()
        self.main_window = None
        self.active_ringing_notifications: Dict[int, threading.Thread] = {}
        # Each task gets a threading.Event; set() means "stop ringing".
        self._stop_events: Dict[int, threading.Event] = {}

    def set_main_window(self, main_window):
        self.main_window = main_window

    # ── Sound ─────────────────────────────────────────────────────────────────

    def _play_sound(self):
        """Play a short system beep/notification sound."""
        if IS_WINDOWS and WINSOUND_AVAILABLE:
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
                return
            except Exception:
                pass
        
        if IS_MAC:
            try:
                os.system('osascript -e "beep"')
                return
            except Exception:
                pass

        # Generic fallback
        print("\a")

    def _ring_loop(self, stop_event: threading.Event):
        """Looping sound for persistent notifications."""
        count = 0
        while not stop_event.is_set() and count < NOTIFICATION_RING_COUNT:
            if IS_WINDOWS and WINSOUND_AVAILABLE:
                try:
                    winsound.Beep(NOTIFICATION_RING_BEEP_HZ_LO, NOTIFICATION_RING_BEEP_MS)
                    time.sleep(0.1)
                    winsound.Beep(NOTIFICATION_RING_BEEP_HZ_HI, NOTIFICATION_RING_BEEP_MS)
                    time.sleep(NOTIFICATION_RING_PAUSE_S)
                except Exception:
                    time.sleep(NOTIFICATION_RING_FALLBACK_PAUSE_S)
            elif IS_MAC:
                try:
                    os.system('osascript -e "beep 2"')
                    time.sleep(NOTIFICATION_RING_PAUSE_S)
                except Exception:
                    time.sleep(NOTIFICATION_RING_FALLBACK_PAUSE_S)
            else:
                print("\a")
                time.sleep(NOTIFICATION_RING_FALLBACK_PAUSE_S)
            count += 1

    def _start_ringing(self, task_id: int):
        stop_event = threading.Event()
        self._stop_events[task_id] = stop_event
        t = threading.Thread(
            target=self._ring_loop, args=(stop_event,), daemon=True
        )
        t.start()
        self.active_ringing_notifications[task_id] = t

    def _stop_ringing(self, task_id: int):
        event = self._stop_events.get(task_id)
        if event:
            event.set()

    # ── Toast notification ────────────────────────────────────────────────────

    def _show_toast(self, title: str, message: str):
        """Show a native OS toast notification."""
        
        # 1. macOS Native Notification
        if IS_MAC:
            try:
                script = f'display notification "{message}" with title "{title}" sound name "Glass"'
                os.system(f"osascript -e '{script}'")
                return True
            except Exception as e:
                logger.warning("macOS notification failed: %s", e)

        # 2. Windows winotify (Premium)
        if IS_WINDOWS and WINOTIFY_AVAILABLE:
            try:
                toast = Notification(
                    app_id="TASKY",
                    title=title,
                    msg=message,
                    duration="short",
                )
                toast.set_audio(audio.Default, loop=False)
                toast.show()
                return True
            except Exception as e:
                logger.warning("winotify failed: %s", e)

        # 3. Windows PowerShell Fallback
        if IS_WINDOWS:
            try:
                truncated = message[:NOTIFICATION_TOAST_MAX_CHARS]
                ps_lines = [
                    "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType=WindowsRuntime] | Out-Null",
                    "$t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)",
                    f"$t.GetElementsByTagName('text')[0].AppendChild($t.CreateTextNode({_ps_escape(title)})) | Out-Null",
                    f"$t.GetElementsByTagName('text')[1].AppendChild($t.CreateTextNode({_ps_escape(truncated)})) | Out-Null",
                    "$n = [Windows.UI.Notifications.ToastNotification]::new($t)",
                    "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('TASKY').Show($n)",
                ]
                ps_script = "; ".join(ps_lines)
                encoded = base64.b64encode(ps_script.encode("utf-16-le")).decode("ascii")
                os.system(f'powershell -WindowStyle Hidden -EncodedCommand {encoded}')
                return True
            except Exception as e:
                logger.warning("PowerShell toast failed: %s", e)
        
        return False

    # ── Main notification entry point ─────────────────────────────────────────

    def show_task_notification(self, task: Task) -> bool:
        if task.id is None:
            logger.warning("Cannot notify task with no id: %s", task.title)
            return False
        try:
            self._start_ringing(task.id)
            self._play_sound()

            # Emit signal for internal UI popups (In-App)
            if SIGNALS_AVAILABLE:
                try:
                    notification_signals.show_notification_popup.emit(
                        task.id, task.title, task.description, task.due_date
                    )
                except Exception as e:
                    logger.warning("Popup signal error: %s", e)

            # Show OS-level toast
            self._show_toast(
                f"TASK DUE: {task.title}",
                task.description or task.due_date.strftime("%Y-%m-%d %H:%M"),
            )

            self._show_console_notification(task)
            self.notified_tasks.add(task.id)

            def _stop_later():
                time.sleep(NOTIFICATION_STOP_AFTER_S)
                self._stop_ringing(task.id)

            threading.Thread(target=_stop_later, daemon=True).start()
            return True

        except Exception as e:
            logger.exception("Notification error for task %s: %s", task.id, e)
            try:
                self._play_sound()
                self._show_console_notification(task)
                self.notified_tasks.add(task.id)
                return True
            except Exception:
                return False

    def show_test_notification(self, title: str, message: str, notification_type: str = "info"):  # noqa: ARG002
        self._play_sound()
        if SIGNALS_AVAILABLE:
            try:
                notification_signals.show_notification_popup.emit(-1, title, message, datetime.now())
            except Exception as e:
                logger.warning("Test popup signal error: %s", e)
        self._show_toast(f"TEST: {title}", message)

    def _show_console_notification(self, task: Task):
        logger.info("TASK DUE: %s — %s", task.title, task.due_date.strftime("%Y-%m-%d %H:%M"))

    def is_task_notified(self, task: Task) -> bool:
        return task.id in self.notified_tasks

    def reset_notification_for_task(self, task_id: int):
        self.notified_tasks.discard(task_id)
        self._stop_ringing(task_id)

    def stop_all_ringing(self):
        for task_id in list(self.active_ringing_notifications.keys()):
            self._stop_ringing(task_id)
        self.active_ringing_notifications.clear()

    async def check_and_notify_due_tasks(self, get_due_tasks_func):
        logger.info("Notification check loop started")
        while True:
            try:
                due_tasks = get_due_tasks_func()
                for task in due_tasks:
                    if not self.is_task_notified(task):
                        self.show_task_notification(task)
                await asyncio.sleep(NOTIFICATION_CHECK_INTERVAL_S)
            except Exception as e:
                logger.exception("Notification loop error: %s", e)
                await asyncio.sleep(NOTIFICATION_CHECK_INTERVAL_S)


def _ps_escape(value: str) -> str:
    """Wrap a string value safely for PowerShell single-quoted string literals."""
    return "'" + value.replace("'", "''") + "'"
