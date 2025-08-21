#!/usr/bin/env python3
"""
TASKY - Task Manager - Main Entry Point

A modern desktop application for managing tasks with notifications and reminders.
Built with PyQt6, SQLite, and asyncio for background task scheduling.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def main():
    """Main application entry point."""
    # Create the Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("TASKY")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("TASKY Apps")
    
    # Set application properties (using compatible attributes)
    try:
        # Try to set high DPI attributes if available
        if hasattr(Qt, 'ApplicationAttribute') and hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
            app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'ApplicationAttribute') and hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
            app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except Exception as e:
        print(f"Warning: Could not set high DPI attributes: {e}")
    
    # Create and show the main window
    main_window = MainWindow()
    main_window.show()
    
    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
