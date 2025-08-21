from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon
from datetime import datetime


class NotificationPopup(QDialog):
    """Custom notification popup for task due alerts."""
    
    def __init__(self, task_title: str, task_description: str, due_date: datetime, parent=None):
        """Initialize the notification popup."""
        super().__init__(parent)
        self.task_title = task_title
        self.task_description = task_description
        self.due_date = due_date
        
        self.setup_ui()
        self.setup_timer()
        
        # Make the popup appear on top of all windows
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        
        # Position the popup in the top-right corner
        self.position_popup()
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setFixedSize(360, 180)  # Smaller size for better compactness
        
        # Modern, cohesive styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e293b, stop:1 #0f172a);
                border: 2px solid #6366f1;
                border-radius: 12px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: white;
                background-color: transparent;
            }
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 600;
                font-size: 12px;
                min-height: 32px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
            QPushButton[class="secondary"] {
                background-color: #8b5cf6;
            }
            QPushButton[class="secondary"]:hover {
                background-color: #7c3aed;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setSpacing(14)  # Reduced spacing
        main_layout.setContentsMargins(18, 18, 18, 18)  # Reduced margins
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        
        # Bell icon (using emoji as text)
        icon_label = QLabel("🔔")
        icon_label.setFont(QFont("Segoe UI", 16))  # Smaller icon
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(icon_label)
        
        # Title section
        title_layout = QVBoxLayout()
        
        # Main title
        title_label = QLabel("TASKY ALERT!")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))  # Smaller font
        title_label.setStyleSheet("color: #fbbf24; font-weight: bold; font-family: 'Segoe UI', sans-serif;")  # Warning color
        title_layout.addWidget(title_label)
        
        # Task title
        task_title_label = QLabel(f"'{self.task_title}'")
        task_title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))  # Smaller font
        task_title_label.setStyleSheet("color: #ecf0f1; font-family: 'Segoe UI', sans-serif;")
        title_layout.addWidget(task_title_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #475569;")
        separator.setFixedHeight(1)
        main_layout.addWidget(separator)
        
        # Task details
        if self.task_description:
            desc_label = QLabel(f"Description: {self.task_description}")
            desc_label.setFont(QFont("Segoe UI", 10))  # Smaller font
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #cbd5e1; font-family: 'Segoe UI', sans-serif;")
            main_layout.addWidget(desc_label)
        
        # Due date
        due_label = QLabel(f"Due: {self.due_date.strftime('%m/%d %H:%M')}")
        due_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))  # Smaller font
        due_label.setStyleSheet("color: #fbbf24; font-family: 'Segoe UI', sans-serif;")
        main_layout.addWidget(due_label)
        
        main_layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)  # Reduced spacing
        
        # Dismiss button
        dismiss_button = QPushButton("✕ Dismiss")
        dismiss_button.setProperty("class", "small")
        dismiss_button.clicked.connect(self.close)
        dismiss_button.setFixedHeight(32)  # Smaller height
        button_layout.addWidget(dismiss_button)
        
        # Snooze button
        snooze_button = QPushButton("⏰ Snooze")
        snooze_button.setProperty("class", "small secondary")
        snooze_button.clicked.connect(self.snooze_notification)
        snooze_button.setFixedHeight(32)  # Smaller height
        button_layout.addWidget(snooze_button)
        
        main_layout.addLayout(button_layout)
    
    def setup_timer(self):
        """Set up auto-close timer."""
        # Auto-close after 25 seconds
        self.auto_close_timer = QTimer()
        self.auto_close_timer.timeout.connect(self.close)
        self.auto_close_timer.start(25000)  # 25 seconds
    
    def position_popup(self):
        """Position the popup in the top-right corner of the screen."""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        
        # Calculate position (top-right corner with some margin)
        x = screen.width() - self.width() - 20
        y = 20
        
        self.move(x, y)
    
    def snooze_notification(self):
        """Snooze the notification for 5 minutes."""
        # This could be implemented to re-trigger the notification later
        print(f"Notification snoozed for task: {self.task_title}")
        self.close()
    
    def show_popup(self):
        """Show the popup with animation."""
        # Fade in effect
        self.setWindowOpacity(0.0)
        self.show()
        
        # Animate opacity
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.fade_in)
        self.fade_timer.start(50)  # Update every 50ms
    
    def fade_in(self):
        """Fade in animation."""
        current_opacity = self.windowOpacity()
        if current_opacity < 1.0:
            self.setWindowOpacity(current_opacity + 0.1)
        else:
            self.fade_timer.stop()
    
    def closeEvent(self, event):
        """Handle close event."""
        if hasattr(self, 'auto_close_timer'):
            self.auto_close_timer.stop()
        if hasattr(self, 'fade_timer'):
            self.fade_timer.stop()
        event.accept()
