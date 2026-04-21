import logging
from PyQt6.QtWidgets import (
    QSystemTrayIcon, QMenu, QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QDateTimeEdit
)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal, QObject
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from datetime import datetime
from models import Task

logger = logging.getLogger(__name__)


def _make_tray_icon() -> QIcon:
    """Generate a simple monochrome circle icon for the tray."""
    px = QPixmap(32, 32)
    px.fill(Qt.GlobalColor.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor("#0A84FF"))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(2, 2, 28, 28)
    p.setPen(QColor("#ffffff"))
    p.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    p.drawText(0, 0, 32, 32, Qt.AlignmentFlag.AlignCenter, "T")
    p.end()
    return QIcon(px)


class QuickAddDialog(QDialog):
    """Minimal quick-add dialog accessible from the tray."""

    task_saved = pyqtSignal(Task)

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.setWindowTitle("Quick Add Task")
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setMinimumWidth(360)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setSpacing(12)
        lay.setContentsMargins(20, 16, 20, 16)

        title_lbl = QLabel("+  Quick Add Task")
        title_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        lay.addWidget(title_lbl)

        title_field_lbl = QLabel("Task title:")
        title_field_lbl.setFont(QFont("Segoe UI", 11))
        lay.addWidget(title_field_lbl)

        self._title = QLineEdit()
        self._title.setPlaceholderText("What needs to be done?")
        self._title.setFixedHeight(36)
        lay.addWidget(self._title)

        due_field_lbl = QLabel("Due date & time:")
        due_field_lbl.setFont(QFont("Segoe UI", 11))
        lay.addWidget(due_field_lbl)

        self._due = QDateTimeEdit()
        self._due.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self._due.setCalendarPopup(True)
        self._due.setDisplayFormat("yyyy-MM-dd hh:mm")
        self._due.setFixedHeight(34)
        lay.addWidget(self._due)

        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        btn_row.addStretch()
        add_btn = QPushButton("Add Task")
        add_btn.clicked.connect(self._save)
        btn_row.addWidget(add_btn)
        lay.addLayout(btn_row)

        self._title.setFocus()
        self._title.returnPressed.connect(self._save)

    def _save(self):
        title = self._title.text().strip()
        if not title:
            return
        task = Task(
            id=None,
            title=title,
            description="",
            due_date=self._due.dateTime().toPyDateTime(),
            completed=False,
            created_at=datetime.now(),
        )
        try:
            new_id = self.db.add_task(task)
            task.id = new_id
        except Exception as exc:
            logger.warning("Quick-add failed to save task: %s", exc)
        self.task_saved.emit(task)
        self.accept()


class TrayManager(QObject):
    """System tray icon with context menu and quick-add support."""

    show_main_window = pyqtSignal()
    open_pomodoro = pyqtSignal()

    def __init__(self, main_window, db_manager, app):
        super().__init__(app)
        self._win = main_window
        self.db = db_manager
        self._app = app
        self._tray = QSystemTrayIcon(app)
        self._tray.setIcon(_make_tray_icon())
        self._tray.setToolTip("TASKY")
        self._build_menu()
        self._tray.activated.connect(self._on_activated)
        self._tray.show()

    def _build_menu(self):
        menu = QMenu()

        show_act = menu.addAction("Show TASKY")
        show_act.triggered.connect(self._show_window)

        quick_act = menu.addAction("+  Quick Add Task")
        quick_act.triggered.connect(self._quick_add)

        pomo_act = menu.addAction("Start Pomodoro")
        pomo_act.triggered.connect(self.open_pomodoro.emit)

        menu.addSeparator()

        quit_act = menu.addAction("Quit")
        quit_act.triggered.connect(self._quit)

        self._tray.setContextMenu(menu)

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._show_window()

    def _show_window(self):
        self._win.show()
        self._win.raise_()
        self._win.activateWindow()

    def _quick_add(self):
        dlg = QuickAddDialog(self.db, self._win)
        dlg.task_saved.connect(lambda _: self._win.load_tasks())
        dlg.exec()

    def _quit(self):
        self._app.quit()

    def update_tooltip(self, pending: int, overdue: int):
        tip = f"TASKY — {pending} pending"
        if overdue:
            tip += f", {overdue} overdue"
        self._tray.setToolTip(tip)

    def show_message(self, title: str, msg: str):
        self._tray.showMessage(title, msg, QSystemTrayIcon.MessageIcon.Information, 3000)
