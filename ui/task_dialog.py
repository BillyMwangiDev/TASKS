from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QDateTimeEdit, QPushButton,
    QLabel, QCheckBox, QFrame
)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from datetime import datetime
from models import Task


class TaskDialog(QDialog):
    """Dialog for adding or editing tasks."""
    
    task_saved = pyqtSignal(Task)  # Signal emitted when task is saved
    
    def __init__(self, parent=None, task: Task = None):
        """Initialize the task dialog."""
        super().__init__(parent)
        self.task = task
        self.setup_ui()
        self.setup_connections()
        
        if task:
            self.setWindowTitle("Edit Task")
            self.load_task_data()
        else:
            self.setWindowTitle("Add Task")
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setModal(True)
        self.setMinimumWidth(360)  # Even smaller width
        self.setMinimumHeight(300)  # Even smaller height
        self.setMaximumHeight(360)
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setSpacing(14)  # Even more compact spacing
        
        # Header with icon
        header_layout = QHBoxLayout()
        
        # Task icon
        icon_label = QLabel("📝")
        icon_label.setFont(QFont("Segoe UI", 18))  # Even smaller icon
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(icon_label)
        
        # Title
        title_layout = QVBoxLayout()
        title_label = QLabel("Task Details")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))  # Even smaller title
        title_label.setStyleSheet("color: #0f172a; font-family: 'Segoe UI', sans-serif;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Manage your task information")
        subtitle_label.setFont(QFont("Segoe UI", 9))  # Even smaller subtitle
        subtitle_label.setStyleSheet("color: #64748b; font-family: 'Segoe UI', sans-serif;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #e2e8f0;")
        separator.setFixedHeight(1)
        main_layout.addWidget(separator)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)  # Even more compact spacing
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(form_layout)
        
        # Title field
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter task title...")
        self.title_edit.setMinimumHeight(28)  # Even smaller height
        self.title_edit.setStyleSheet("""
            QLineEdit {
                background-color: #374151;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                color: #f9fafb;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit:focus {
                border-color: #8b5cf6;
                background-color: #4b5563;
            }
        """)
        form_layout.addRow("Title:", self.title_edit)
        
        # Description field
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter task description (optional)...")
        self.description_edit.setMaximumHeight(55)  # Even smaller height
        self.description_edit.setStyleSheet("""
            QTextEdit {
                background-color: #374151;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                color: #f9fafb;
                font-family: 'Segoe UI', sans-serif;
            }
            QTextEdit:focus {
                border-color: #8b5cf6;
                background-color: #4b5563;
            }
        """)
        form_layout.addRow("Description:", self.description_edit)
        
        # Due date and time
        self.due_datetime = QDateTimeEdit()
        self.due_datetime.setDateTime(QDateTime.currentDateTime().addSecs(3600))  # Default: 1 hour from now
        self.due_datetime.setCalendarPopup(True)
        self.due_datetime.setMinimumHeight(28)  # Even smaller height
        self.due_datetime.setStyleSheet("""
            QDateTimeEdit {
                background-color: #374151;
                border: 2px solid #4b5563;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                color: #f9fafb;
                font-family: 'Segoe UI', sans-serif;
            }
            QDateTimeEdit:focus {
                border-color: #8b5cf6;
                background-color: #4b5563;
            }
        """)
        form_layout.addRow("Due Date & Time:", self.due_datetime)
        
        # Completed checkbox (only for editing)
        if self.task:
            self.completed_checkbox = QCheckBox("Mark as completed")
            self.completed_checkbox.setMinimumHeight(36)  # Smaller height
            self.completed_checkbox.setStyleSheet("""
                QCheckBox {
                    color: #f9fafb;
                    spacing: 10px;
                    font-size: 13px;
                    font-family: 'Segoe UI', sans-serif;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border: 2px solid #4b5563;
                    border-radius: 4px;
                    background-color: #374151;
                }
                QCheckBox::indicator:checked {
                    background-color: #8b5cf6;
                    border-color: #8b5cf6;
                }
            """)
            form_layout.addRow("", self.completed_checkbox)
        
        main_layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        
        # Cancel button
        self.cancel_button = QPushButton("✕ Cancel")
        self.cancel_button.setProperty("class", "secondary")
        self.cancel_button.setMinimumHeight(28)  # Even smaller height
        self.cancel_button.setMinimumWidth(75)  # Even smaller width
        button_layout.addWidget(self.cancel_button)
        
        button_layout.addStretch()
        
        # Save button
        self.save_button = QPushButton("💾 Save")
        self.save_button.setProperty("class", "success")
        self.save_button.setMinimumHeight(28)  # Even smaller height
        self.save_button.setMinimumWidth(85)  # Even smaller width
        button_layout.addWidget(self.save_button)
        
        # Set focus to title field
        self.title_edit.setFocus()
    
    def setup_connections(self):
        """Set up signal connections."""
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.save_task)
        self.title_edit.textChanged.connect(self.validate_form)
    
    def validate_form(self):
        """Validate the form and enable/disable save button."""
        title = self.title_edit.text().strip()
        self.save_button.setEnabled(len(title) > 0)
    
    def load_task_data(self):
        """Load existing task data into the form."""
        if not self.task:
            return
        
        self.title_edit.setText(self.task.title)
        self.description_edit.setPlainText(self.task.description)
        self.due_datetime.setDateTime(QDateTime.fromString(
            self.task.due_date.strftime("%yyyy-MM-dd hh:mm:ss"), 
            "yyyy-MM-dd hh:mm:ss"
        ))
        
        if hasattr(self, 'completed_checkbox'):
            self.completed_checkbox.setChecked(self.task.completed)
    
    def save_task(self):
        """Save the task and emit the task_saved signal."""
        title = self.title_edit.text().strip()
        if not title:
            return
        
        description = self.description_edit.toPlainText().strip()
        due_date = self.due_datetime.dateTime().toPyDateTime()
        
        if self.task:
            # Update existing task
            self.task.title = title
            self.task.description = description
            self.task.due_date = due_date
            if hasattr(self, 'completed_checkbox'):
                self.task.completed = self.completed_checkbox.isChecked()
        else:
            # Create new task
            self.task = Task(
                id=None,
                title=title,
                description=description,
                due_date=due_date,
                completed=False,
                created_at=datetime.now()
            )
        
        self.task_saved.emit(self.task)
        self.accept()
