from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QMessageBox, QFrame, QSplitter, QSizePolicy, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QAction
from datetime import datetime
from models import Task
from ui.task_dialog import TaskDialog
from ui.theme_manager import ThemeManager
from database import DatabaseManager
from notifications import NotificationManager
from scheduler import TaskScheduler
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication


class MainWindow(QMainWindow):
    """Main window of TASKY - Task Manager."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.db_manager = DatabaseManager()
        self.notification_manager = NotificationManager()
        self.task_scheduler = TaskScheduler(self.notification_manager)
        self.theme_manager = ThemeManager()
        
        self.setup_ui()
        self.setup_connections()
        self.load_tasks()
        
        # Start notification scheduler after UI is loaded
        QTimer.singleShot(1000, self.start_notification_scheduler)
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("TASKY")
        self.setMinimumSize(380, 350)  # Slightly smaller minimum width
        self.resize(420, 400)  # Slightly smaller default width, same height
        self.setMaximumSize(800, 700)  # Allow resizing up to reasonable limits
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout - ultra compact spacing
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(8)  # Even more compact spacing
        main_layout.setContentsMargins(10, 10, 10, 10)  # Even more compact margins
        
        # Header with logo and theme toggle - cleaner design
        header_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)
        
        # App logo and title - more prominent
        logo_layout = QHBoxLayout()
        
        # Logo (using emoji as icon)
        logo_label = QLabel("📋")
        logo_label.setFont(QFont("Segoe UI", 16))  # Even smaller logo
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        # App title - ultra compact typography
        title_layout = QVBoxLayout()
        title_label = QLabel("TASKY")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))  # Even smaller title
        title_label.setStyleSheet("color: #8b5cf6; font-family: 'Segoe UI', sans-serif;")  # Purple color with better font
        title_layout.addWidget(title_label)
        
        # Removed subtitle to avoid confusion with Windows Task Manager
        
        logo_layout.addLayout(title_layout)
        header_layout.addLayout(logo_layout)
        
        header_layout.addStretch()
        
        # Theme toggle switch - sun/moon design
        self.theme_toggle_button = QPushButton()
        self.theme_toggle_button.setProperty("class", "secondary")
        self.theme_toggle_button.setFixedSize(50, 26)  # Smaller toggle switch size
        self.theme_toggle_button.setToolTip("Toggle between Dark and Light themes")
        self.update_theme_button_text()
        header_layout.addWidget(self.theme_toggle_button)
        
        # Status indicator - cleaner design
        self.status_label = QLabel("🔔 Starting...")
        self.status_label.setFont(QFont("Segoe UI", 8))  # Even smaller font
        self.status_label.setStyleSheet("""
            padding: 3px 8px; 
            border-radius: 5px; 
            background-color: #fef3c7; 
            color: #92400e;
            border: 1px solid #fbbf24;
            font-family: 'Segoe UI', sans-serif;
        """)
        header_layout.addWidget(self.status_label)
        
        # Search bar - like sticky notes
        search_layout = QHBoxLayout()
        main_layout.addLayout(search_layout)
        
        # Search icon
        search_icon = QLabel("🔍")
        search_icon.setFont(QFont("Segoe UI", 10))  # Even smaller icon
        search_icon.setStyleSheet("color: #64748b;")
        search_layout.addWidget(search_icon)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tasks...")
        self.search_input.setMinimumHeight(26)  # Even smaller height
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #374151, stop:1 #4b5563);
                border: 2px solid #6b7280;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 13px;
                color: #f9fafb;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit:focus {
                border-color: #8b5cf6;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4b5563, stop:1 #6b7280);
                box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
            }
        """)
        search_layout.addWidget(self.search_input)
        
        # Button toolbar - ultra compact
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)  # Even more reduced spacing between buttons
        main_layout.addLayout(button_layout)
        
        # Add Task button - ultra compact
        self.add_button = QPushButton("➕ Add")
        self.add_button.setProperty("class", "success")
        self.add_button.setMinimumHeight(24)  # Even smaller height
        self.add_button.setMinimumWidth(60)  # Even smaller width
        button_layout.addWidget(self.add_button)
        
        # Edit Task button
        self.edit_button = QPushButton("✏️ Edit")
        self.edit_button.setProperty("class", "warning")
        self.edit_button.setEnabled(False)
        self.edit_button.setMinimumHeight(24)  # Even smaller height
        self.edit_button.setMinimumWidth(50)  # Even smaller width
        button_layout.addWidget(self.edit_button)
        
        # Mark as Done button
        self.complete_button = QPushButton("✓ Done")
        self.complete_button.setProperty("class", "info")
        self.complete_button.setEnabled(False)
        self.complete_button.setMinimumHeight(24)  # Even smaller height
        self.complete_button.setMinimumWidth(50)  # Even smaller width
        button_layout.addWidget(self.complete_button)
        
        # Delete Task button
        self.delete_button = QPushButton("🗑️ Del")
        self.delete_button.setProperty("class", "danger")
        self.delete_button.setEnabled(False)
        self.delete_button.setMinimumHeight(24)  # Even smaller height
        self.delete_button.setMinimumWidth(45)  # Even smaller width
        button_layout.addWidget(self.delete_button)
        
        button_layout.addStretch()
        
        # Time tracking button
        self.track_button = QPushButton("⏱️ Track")
        self.track_button.setProperty("class", "info")
        self.track_button.setEnabled(False)
        self.track_button.setMinimumHeight(24)  # Even smaller height
        self.track_button.setMinimumWidth(55)  # Even smaller width
        button_layout.addWidget(self.track_button)
        
        # Refresh button
        self.refresh_button = QPushButton("🔄")
        self.refresh_button.setProperty("class", "secondary")
        self.refresh_button.setMinimumHeight(24)  # Even smaller height
        self.refresh_button.setMinimumWidth(28)  # Even smaller width - icon only
        button_layout.addWidget(self.refresh_button)
        
        # Task table - cleaner design like sticky notes
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(6)
        self.task_table.setHorizontalHeaderLabels([
            "Title", "Description", "Due Date", "Status", "Time Until Due", "Time Spent"
        ])
        
        # Set table properties - cleaner appearance
        header = self.task_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Title
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Description
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Due Date
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Time Until Due
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Time Spent
        
        self.task_table.setAlternatingRowColors(True)
        self.task_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.task_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.task_table.setShowGrid(False)  # No grid lines for cleaner look
        self.task_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                outline: none;
                font-family: 'Segoe UI', sans-serif;
            }
            QTableWidget::item {
                padding: 8px 6px;
                border: none;
                border-bottom: 1px solid #4b5563;
                font-size: 12px;
            }
            QTableWidget::item:selected {
                background-color: #8b5cf6;
                color: white;
            }
            QHeaderView::section {
                background-color: transparent;
                color: #9ca3af;
                padding: 12px 6px;
                border: none;
                font-weight: 600;
                font-size: 12px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        
        # Set table size policy to expand
        self.task_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        main_layout.addWidget(self.task_table)
        
        # Statistics bar - show task counts and productivity
        self.stats_label = QLabel("📊 Tasks: 0 | Completed: 0 | Pending: 0 | Overdue: 0")
        self.stats_label.setFont(QFont("Segoe UI", 8))
        self.stats_label.setStyleSheet("""
            padding: 4px 8px;
            border-radius: 4px;
            background-color: #1e40af;
            color: white;
            border: 1px solid #3b82f6;
            font-family: 'Segoe UI', sans-serif;
        """)
        self.statusBar().addPermanentWidget(self.stats_label)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Timer for updating time until due
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_time_until_due)
        self.update_timer.start(30000)  # Update every 30 seconds
        
        # Apply initial theme
        self.apply_theme()
    
    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        from PyQt6.QtGui import QShortcut, QKeySequence
        
        # Add new task
        add_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        add_shortcut.activated.connect(self.add_task)
        
        # Edit selected task
        edit_shortcut = QShortcut(QKeySequence("Enter"), self)
        edit_shortcut.activated.connect(self.edit_task)
        
        # Delete selected task
        delete_shortcut = QShortcut(QKeySequence("Delete"), self)
        delete_shortcut.activated.connect(self.delete_task)
        
        # Refresh tasks
        refresh_shortcut = QShortcut(QKeySequence("F5"), self)
        refresh_shortcut.activated.connect(self.load_tasks)
        
        # Focus search box
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(lambda: self.search_input.setFocus())
        
        # Toggle theme
        theme_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        theme_shortcut.activated.connect(self.toggle_theme)
    
    def setup_connections(self):
        """Set up signal connections."""
        self.add_button.clicked.connect(self.add_task)
        self.edit_button.clicked.connect(self.edit_task)
        self.complete_button.clicked.connect(self.toggle_task_completion)
        self.delete_button.clicked.connect(self.delete_task)
        self.track_button.clicked.connect(self.toggle_time_tracking)
        self.refresh_button.clicked.connect(self.load_tasks)
        self.theme_toggle_button.clicked.connect(self.toggle_theme)
        self.task_table.itemSelectionChanged.connect(self.update_button_states)
        
        # Connect theme manager
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # Connect search functionality
        self.search_input.textChanged.connect(self.filter_tasks)
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
    
    def apply_theme(self):
        """Apply the current theme to the application."""
        app = QApplication.instance()
        if app:
            self.theme_manager.apply_theme_to_app(app)
            app.setStyleSheet(self.theme_manager.get_stylesheet())
    
    def on_theme_changed(self, theme_name: str):
        """Handle theme change."""
        self.apply_theme()
        self.update_theme_button_text()
    
    def update_theme_button_text(self):
        """Update the theme toggle button text."""
        icon = self.theme_manager.get_theme_icon()
        self.theme_toggle_button.setText(icon)
    
    def toggle_theme(self):
        """Toggle between dark and light themes."""
        self.theme_manager.toggle_theme()
    
    def start_notification_scheduler(self):
        """Start the background notification scheduler."""
        try:
            # Connect notification manager to main window for popup positioning
            self.notification_manager.set_main_window(self)
            
            self.task_scheduler.start(self.db_manager.get_due_tasks)
            self.status_label.setText("🔔 Active")
            self.status_label.setStyleSheet("""
                padding: 4px 8px; 
                border-radius: 4px; 
                background-color: #d1fae5; 
                color: #065f46;
                border: 1px solid #10b981;
            """)
            self.statusBar().showMessage("Notification system started")
        except Exception as e:
            print(f"Failed to start notification scheduler: {e}")
            self.status_label.setText("🔔 Error")
            self.status_label.setStyleSheet("""
                padding: 4px 8px; 
                border-radius: 4px; 
                background-color: #fee2e2; 
                color: #991b1b;
                border: 1px solid #ef4444;
            """)
    
    def filter_tasks(self):
        """Filter tasks based on search input."""
        search_text = self.search_input.text().lower().strip()
        
        if not search_text:
            # If no search text, show all tasks
            self.load_tasks()
            return
        
        # Get all tasks and filter them
        all_tasks = self.db_manager.get_all_tasks()
        filtered_tasks = []
        
        for task in all_tasks:
            # Search in title, description, and due date
            if (search_text in task.title.lower() or 
                search_text in task.description.lower() or
                search_text in task.due_date.strftime("%m/%d %H:%M").lower()):
                filtered_tasks.append(task)
        
        # Display filtered tasks
        self.display_tasks(filtered_tasks)
        self.statusBar().showMessage(f"Found {len(filtered_tasks)} matching tasks")
    
    def display_tasks(self, tasks):
        """Display a list of tasks in the table."""
        self.task_table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            # Title
            title_item = QTableWidgetItem(task.title)
            title_item.setData(Qt.ItemDataRole.UserRole, task.id)
            self.task_table.setItem(row, 0, title_item)
            
            # Description (truncated)
            description = task.description[:40] + "..." if len(task.description) > 40 else task.description
            desc_item = QTableWidgetItem(description)
            self.task_table.setItem(row, 1, desc_item)
            
            # Due date
            due_date_item = QTableWidgetItem(task.due_date.strftime("%m/%d %H:%M"))
            self.task_table.setItem(row, 2, due_date_item)
            
            # Status
            status_text = "✓ Done" if task.completed else "⏰ Pending"
            status_item = QTableWidgetItem(status_text)
            if task.completed:
                status_item.setBackground(QColor("#10b981"))  # Success color
                status_item.setForeground(QColor("white"))
            self.task_table.setItem(row, 3, status_item)
            
            # Time until due
            time_item = QTableWidgetItem(task.time_until_due())
            self.task_table.setItem(row, 4, time_item)
            
            # Time spent
            time_spent_item = QTableWidgetItem(task.get_time_spent_formatted())
            self.task_table.setItem(row, 5, time_spent_item)
            
            # Status indicators
            if task.is_overdue() and not task.completed:
                for col in range(6):
                    item = self.task_table.item(row, col)
                    if item:
                        item.setBackground(QColor("#ef4444"))  # Danger color
                        item.setForeground(QColor("white"))
            elif task.completed:
                # Use a subtle green for completed tasks
                for col in range(6):
                    item = self.task_table.item(row, col)
                    if item:
                        item.setBackground(QColor("#10b981"))  # Success color
                        item.setForeground(QColor("white"))
    
    def load_tasks(self):
        """Load tasks from database and display them in the table."""
        tasks = self.db_manager.get_all_tasks()
        self.display_tasks(tasks)
        self.statusBar().showMessage(f"Loaded {len(tasks)} tasks")
    
    def update_button_states(self):
        """Update button states based on selection."""
        has_selection = len(self.task_table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.complete_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        self.track_button.setEnabled(has_selection)
        
        # Update track button text based on tracking status
        if has_selection:
            task_id = self.get_selected_task_id()
            if task_id:
                task = self.db_manager.get_task_by_id(task_id)
                if task and not task.completed:
                    if task.is_tracking():
                        self.track_button.setText("⏹️ Stop")
                        self.track_button.setProperty("class", "danger")
                    else:
                        self.track_button.setText("⏱️ Track")
                        self.track_button.setProperty("class", "info")
                    self.track_button.setStyleSheet("")  # Reset to use theme stylesheet
    
    def get_selected_task_id(self):
        """Get the ID of the currently selected task."""
        current_row = self.task_table.currentRow()
        if current_row >= 0:
            title_item = self.task_table.item(current_row, 0)
            if title_item:
                return title_item.data(Qt.ItemDataRole.UserRole)
        return None
    
    def add_task(self):
        """Open dialog to add a new task."""
        dialog = TaskDialog(self)
        dialog.task_saved.connect(self.on_task_saved)
        dialog.exec()
    
    def edit_task(self):
        """Open dialog to edit the selected task."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        
        task = self.db_manager.get_task_by_id(task_id)
        if task is None:
            return
        
        dialog = TaskDialog(self, task)
        dialog.task_saved.connect(self.on_task_saved)
        dialog.exec()
    
    def toggle_task_completion(self):
        """Toggle the completion status of the selected task."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        
        task = self.db_manager.get_task_by_id(task_id)
        if task is None:
            return
        
        new_status = not task.completed
        if self.db_manager.mark_task_completed(task_id, new_status):
            self.load_tasks()
            self.statusBar().showMessage(f"Task marked as {'completed' if new_status else 'pending'}")
        else:
            QMessageBox.warning(self, "Error", "Failed to update task status")
    
    def toggle_time_tracking(self):
        """Toggle time tracking for the selected task."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        
        task = self.db_manager.get_task_by_id(task_id)
        if task is None or task.completed:
            return
        
        if task.is_tracking():
            # Stop tracking
            task.stop_tracking()
            self.db_manager.update_task(task)
            self.statusBar().showMessage("Time tracking stopped")
        else:
            # Start tracking
            task.start_tracking()
            self.db_manager.update_task(task)
            self.statusBar().showMessage("Time tracking started")
        
        self.load_tasks()
    
    def delete_task(self):
        """Delete the selected task."""
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.db_manager.delete_task(task_id):
                self.load_tasks()
                self.statusBar().showMessage("Task deleted successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete task")
    
    def on_task_saved(self, task: Task):
        """Handle task saved signal from dialog."""
        if task.id is None:
            # New task
            task_id = self.db_manager.add_task(task)
            task.id = task_id
            self.statusBar().showMessage("Task added successfully")
        else:
            # Updated task
            if self.db_manager.update_task(task):
                self.statusBar().showMessage("Task updated successfully")
                # Reset notification for this task
                self.notification_manager.reset_notification_for_task(task.id)
            else:
                QMessageBox.warning(self, "Error", "Failed to update task")
                return
        
        self.load_tasks()
    
    def update_time_until_due(self):
        """Update the time until due column for all tasks."""
        for row in range(self.task_table.rowCount()):
            title_item = self.task_table.item(row, 0)
            if title_item:
                task_id = title_item.data(Qt.ItemDataRole.UserRole)
                if task_id:
                    task = self.db_manager.get_task_by_id(task_id)
                    if task:
                        time_item = self.task_table.item(row, 4)
                        if time_item:
                            time_item.setText(task.time_until_due())
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        """Update the statistics display."""
        all_tasks = self.db_manager.get_all_tasks()
        total = len(all_tasks)
        completed = sum(1 for task in all_tasks if task.completed)
        pending = total - completed
        overdue = sum(1 for task in all_tasks if task.is_overdue() and not task.completed)
        
        self.stats_label.setText(f"📊 Tasks: {total} | Completed: {completed} | Pending: {pending} | Overdue: {overdue}")
        
        # Update stats label color based on overdue count
        if overdue > 0:
            self.stats_label.setStyleSheet("""
                padding: 4px 8px;
                border-radius: 4px;
                background-color: #dc2626;
                color: white;
                border: 1px solid #ef4444;
                font-family: 'Segoe UI', sans-serif;
            """)
        else:
            self.stats_label.setStyleSheet("""
                padding: 4px 8px;
                border-radius: 4px;
                background-color: #1e40af;
                color: white;
                border: 1px solid #3b82f6;
                font-family: 'Segoe UI', sans-serif;
            """)
    
    def closeEvent(self, event):
        """Handle window close event."""
        try:
            self.task_scheduler.stop()
        except Exception as e:
            print(f"Error stopping scheduler: {e}")
        event.accept()
