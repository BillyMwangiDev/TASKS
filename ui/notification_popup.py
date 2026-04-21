from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QApplication, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import (
    QFont, QPainter, QColor, QPen, QBrush, QPainterPath
)
from datetime import datetime, timedelta

_AUTO_CLOSE_MS = 25_000
_SNOOZE_MINUTES = 10
_PROGRESS_INTERVAL_MS = 100


class NotificationPopup(QDialog):
    """Polished floating notification — translucent bg, slide-in, countdown bar."""

    def __init__(self, task_id: int, task_title: str, task_description: str,
                 due_date: datetime, theme_manager, snooze_callback=None, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.task_title = task_title
        self.task_description = task_description
        self.due_date = due_date
        self.theme_manager = theme_manager
        self._snooze_callback = snooze_callback

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(360)
        self.setMinimumHeight(160 + (50 if task_description else 0))

        self._setup_ui()
        self._setup_timers()
        self._position()

    # ── Custom paint — rounded card + glow border ─────────────────────────────

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = 14
        
        c = self.theme_manager.get_theme_colors()

        # Outer glow
        glow_color = c.get('border_glow', 'rgba(156,163,175,0.35)')
        glow = QColor(glow_color)
        glow_pen = QPen(glow, 8)
        p.setPen(glow_pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        glow_path = QPainterPath()
        glow_path.addRoundedRect(4, 4, w - 8, h - 8, r, r)
        p.drawPath(glow_path)

        # Card background
        card_bg = QColor(c.get('card_bg', c['surface_1']))
        p.setBrush(QBrush(card_bg))
        card_path = QPainterPath()
        card_path.addRoundedRect(6, 6, w - 12, h - 12, r, r)
        
        # Solid fill instead of gradient to match premium cards
        p.fillPath(card_path, QBrush(card_bg))

        # Accent border
        p.setPen(QPen(QColor(c['primary']), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(card_path)

        p.end()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        c = self.theme_manager.get_theme_colors()

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 12)
        root.setSpacing(10)

        # ── Header row ────────────────────────────────────────────────────────
        header_row = QHBoxLayout()
        header_row.setSpacing(10)



        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        alert_lbl = QLabel("Task Due")
        alert_lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        alert_lbl.setStyleSheet(f"color: {c['warning']}; background: transparent;")
        title_col.addWidget(alert_lbl)

        task_lbl = QLabel(self.task_title)
        task_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        task_lbl.setStyleSheet(f"color: {c['text_primary']}; background: transparent;")
        task_lbl.setWordWrap(True)
        title_col.addWidget(task_lbl)

        header_row.addLayout(title_col, 1)



        root.addLayout(header_row)

        # ── Separator ─────────────────────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"background: {c['border']}; border: none;")
        sep.setFixedHeight(1)
        root.addWidget(sep)

        # ── Description + due ─────────────────────────────────────────────────
        if self.task_description:
            desc_lbl = QLabel(self.task_description)
            desc_lbl.setFont(QFont("Segoe UI", 11))
            desc_lbl.setStyleSheet(f"color: {c['text_secondary']}; background: transparent;")
            desc_lbl.setWordWrap(True)
            root.addWidget(desc_lbl)

        due_lbl = QLabel(f"Due: {self.due_date.strftime('%b %d · %H:%M')}")
        due_lbl.setFont(QFont("Segoe UI", 11))
        due_lbl.setStyleSheet(f"color: {c['text_muted']}; background: transparent;")
        root.addWidget(due_lbl)

        # ── Buttons ───────────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addStretch()

        snooze_btn = QPushButton("Snooze 10m")
        snooze_btn.setFixedHeight(30)
        snooze_btn.setProperty("class", "secondary")
        snooze_btn.clicked.connect(self._snooze)
        btn_row.addWidget(snooze_btn)

        dismiss_btn = QPushButton("Dismiss")
        dismiss_btn.setFixedHeight(30)
        dismiss_btn.clicked.connect(self.close)
        btn_row.addWidget(dismiss_btn)

        root.addLayout(btn_row)

        # ── Countdown progress bar ────────────────────────────────────────────
        self._progress = QProgressBar()
        self._progress.setFixedHeight(3)
        self._progress.setRange(0, _AUTO_CLOSE_MS)
        self._progress.setValue(_AUTO_CLOSE_MS)
        self._progress.setTextVisible(False)
        self._progress.setStyleSheet(
            f"QProgressBar {{ background: transparent; border: none; border-radius: 1px; }}"
            f"QProgressBar::chunk {{ background: {c['primary']}; border-radius: 1px; }}"
        )
        root.addWidget(self._progress)

    # ── Timers ────────────────────────────────────────────────────────────────

    def _setup_timers(self):
        self._elapsed = 0

        self._close_timer = QTimer(self)
        self._close_timer.setSingleShot(True)
        self._close_timer.timeout.connect(self.close)
        self._close_timer.start(_AUTO_CLOSE_MS)

        self._tick_timer = QTimer(self)
        self._tick_timer.timeout.connect(self._tick)
        self._tick_timer.start(_PROGRESS_INTERVAL_MS)

    def _tick(self):
        self._elapsed += _PROGRESS_INTERVAL_MS
        self._progress.setValue(max(0, _AUTO_CLOSE_MS - self._elapsed))

    # ── Position + slide-in ───────────────────────────────────────────────────

    def _position(self):
        screen = QApplication.primaryScreen()
        if screen:
            sg = screen.availableGeometry()
            target_x = sg.right() - self.width() - 16
            target_y = sg.bottom() - self.height() - 16
        else:
            target_x, target_y = 100, 100

        # Start off-screen to the right
        self.move(target_x + self.width() + 40, target_y)
        self._slide_anim = QPropertyAnimation(self, b"pos", self)
        self._slide_anim.setDuration(320)
        self._slide_anim.setStartValue(QPoint(target_x + self.width() + 40, target_y))
        self._slide_anim.setEndValue(QPoint(target_x, target_y))
        self._slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    # ── Public API ────────────────────────────────────────────────────────────

    def show_popup(self):
        self.setWindowOpacity(0.0)
        self.show()
        self._slide_anim.start()

        # Fade in alongside slide
        self._fade_timer = QTimer(self)
        self._fade_timer.timeout.connect(self._fade_step)
        self._fade_timer.start(20)

        self.raise_()
        self.activateWindow()

    def _fade_step(self):
        op = self.windowOpacity()
        if op < 1.0:
            self.setWindowOpacity(min(1.0, op + 0.08))
        else:
            self._fade_timer.stop()

    def _snooze(self):
        if self._snooze_callback and self.task_id > 0:
            self._snooze_callback(self.task_id, datetime.now() + timedelta(minutes=_SNOOZE_MINUTES))
        self.close()

    def closeEvent(self, event):
        for attr in ("_close_timer", "_tick_timer", "_fade_timer"):
            t = getattr(self, attr, None)
            if t:
                t.stop()
        event.accept()
