#!/usr/bin/env python3
"""TASKY v2 — offline-first task manager with Pomodoro, analytics, and system tray."""

import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from ui.main_window import MainWindow

def _load_api_key_from_keychain():
    """Load the Anthropic API key from secure storage into the environment at startup."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return  # Already set via environment — respect it
    try:
        from key_storage import load_key
        key = load_key()
        if key:
            os.environ["ANTHROPIC_API_KEY"] = key
            logger.info("Anthropic API key loaded from secure storage")
    except Exception as e:
        logger.warning("Could not load API key from secure storage: %s", e)


def main():
    _load_api_key_from_keychain()

    app = QApplication(sys.argv)
    app.setApplicationName("TASKY")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("TASKY")

    # Don't quit when main window is closed (stays in tray)
    app.setQuitOnLastWindowClosed(False)

    # Create main window (restores its own geometry via QSettings)
    main_window = MainWindow()
    main_window.show()

    # Notification scheduler (background due-date checks)
    try:
        from notifications import NotificationManager
        from scheduler import TaskScheduler
        from ui.notification_popup import NotificationPopup
        from ui.signals import notification_signals
        from ui.theme_manager import ThemeManager

        notification_manager = NotificationManager()
        notification_manager.set_main_window(main_window)
        scheduler = TaskScheduler(notification_manager)
        scheduler.start(main_window.db_manager.get_due_tasks)
        app.aboutToQuit.connect(scheduler.stop)

        _active_popups: list = []

        def _show_notification_popup(task_id: int, title: str, description: str, due_date):
            tm = ThemeManager.instance()

            def _snooze_task(tid: int, new_due):
                try:
                    task = main_window.db_manager.get_task_by_id(tid)
                    if task:
                        task.due_date = new_due
                        main_window.db_manager.update_task(task)
                        notification_manager.reset_notification_for_task(tid)
                        main_window.load_tasks()
                        logger.info("Task %d snoozed until %s", tid, new_due.strftime("%H:%M"))
                except Exception as exc:
                    logger.warning("Snooze failed for task %d: %s", tid, exc)

            popup = NotificationPopup(
                task_id, title, description, due_date, tm,
                snooze_callback=_snooze_task if task_id > 0 else None,
            )
            _active_popups.append(popup)
            popup.finished.connect(lambda: _active_popups.remove(popup) if popup in _active_popups else None)
            popup.show_popup()

        notification_signals.show_notification_popup.connect(_show_notification_popup)
        logger.info("Notification scheduler started")
    except Exception as e:
        logger.warning("Notification scheduler unavailable: %s", e)

    # System tray
    try:
        from ui.tray_manager import TrayManager
        tray = TrayManager(main_window, main_window.db_manager, app)
        tray.open_pomodoro.connect(main_window._open_pomodoro)

        # Wire close-to-tray behavior based on settings
        settings = QSettings("TASKY", "TASKY")
        minimize_to_tray = settings.value("minimize_to_tray", True, type=bool)

        if minimize_to_tray:
            def _close_to_tray(event):
                event.ignore()
                main_window.hide()
                tray.show_message("TASKY", "Running in the background. Double-click tray icon to restore.")
            main_window.closeEvent = _close_to_tray

        # Update tray tooltip periodically
        from PyQt6.QtCore import QTimer
        def _update_tray():
            try:
                tasks = main_window.db_manager.get_all_tasks()
                pending = sum(1 for t in tasks if not t.completed)
                overdue = sum(1 for t in tasks if t.is_overdue())
                tray.update_tooltip(pending, overdue)
            except Exception as e:
                logger.warning("Tray tooltip update failed: %s", e)
        tray_timer = QTimer()
        tray_timer.timeout.connect(_update_tray)
        tray_timer.start(60_000)
        _update_tray()

    except Exception as e:
        logger.warning("System tray unavailable: %s", e)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
