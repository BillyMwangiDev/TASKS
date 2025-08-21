# TASKY - Your Personal Task Assistant 📋

**TASKY** is a modern, elegant desktop task management application built with Python and PyQt6. It features a beautiful dark/light theme system, real-time notifications, and an intuitive interface designed for productivity.

![TASKY Screenshot](https://img.shields.io/badge/TASKY-Desktop%20App-blue?style=for-the-badge&logo=python)

## ✨ Features

### 🎯 **Core Functionality**
- **Task Management**: Create, edit, delete, and mark tasks as complete
- **Smart Notifications**: Windows toast notifications with sound alerts
- **Due Date Tracking**: Real-time countdown to task deadlines
- **Search & Filter**: Find tasks quickly with real-time search
- **Persistent Storage**: SQLite database for reliable data persistence

### 🎨 **Modern UI/UX**
- **Dual Theme System**: Beautiful dark and dimmed light modes
- **Responsive Design**: Compact, resizable window that adapts to your needs
- **Professional Appearance**: Clean, sticky-note inspired interface
- **Custom Icons**: Intuitive emoji-based icons for all actions
- **Ultra-Compact**: Optimized for small screens and productivity

### 🔔 **Smart Notifications**
- **Windows Toast**: Native Windows 10/11 notifications
- **Sound Alerts**: Audio notifications for task reminders
- **Custom Popups**: Prominent notification dialogs
- **Background Monitoring**: Continuous task monitoring
- **Snooze Function**: Dismiss or snooze notifications

## 🚀 Installation

### Prerequisites
- **Python 3.8+** (3.9+ recommended)
- **Windows 10/11** (for notifications)
- **Git** (for cloning)

### Quick Install

#### Option 1: Clone & Install
```bash
# Clone the repository
git clone https://github.com/yourusername/TASKY.git
cd TASKY

# Install dependencies
pip install -r requirements.txt

# Run TASKY
python main.py
```

#### Option 2: Download & Install
1. Download the latest release from [Releases](https://github.com/yourusername/TASKY/releases)
2. Extract the ZIP file
3. Open Command Prompt in the extracted folder
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python main.py`

### Dependencies
```
PyQt6>=6.9.1
win10toast>=0.0.3
```

## 📖 User Manual

### Getting Started

#### 1. **Launch TASKY**
- Run `python main.py` or double-click `run.bat`
- TASKY starts in dark mode by default
- The main window displays your task list

#### 2. **Add Your First Task**
- Click the **➕ Add** button
- Fill in the task details:
  - **Title**: Brief task description
  - **Description**: Detailed information (optional)
  - **Due Date**: When the task is due
  - **Completed**: Check if already done
- Click **Save** to create the task

#### 3. **Manage Tasks**
- **Edit**: Select a task and click **✏️ Edit**
- **Complete**: Select and click **✓ Done**
- **Delete**: Select and click **🗑️ Del**
- **Refresh**: Click **🔄** to reload tasks

### Interface Guide

#### **Header Section**
- **📋 TASKY**: App logo and title
- **☀️🌙**: Theme toggle (click to switch themes)
- **🔔 Status**: Notification system status indicator

#### **Search Bar**
- **🔍 Search**: Type to filter tasks in real-time
- Searches across title, description, and due dates

#### **Task Table**
- **Title**: Task name (expandable column)
- **Description**: Brief preview (truncated if long)
- **Due Date**: When task is due (MM/DD HH:MM format)
- **Status**: ✓ Done or ⏰ Pending
- **Time Until Due**: Real-time countdown

#### **Color Coding**
- **Green**: Completed tasks
- **Red**: Overdue tasks
- **Purple**: Selected row
- **Alternating**: Row backgrounds for readability

### Theme System

#### **Dark Mode** (Default)
- **Outer Background**: Dark grey (#1f2937)
- **Inner Surface**: Medium grey (#374151)
- **Text**: Light colors for contrast
- **Accents**: Purple (#8b5cf6) and Blue (#3b82f6)

#### **Light Mode** (Dimmed)
- **Outer Background**: Soft light grey (#e5e7eb)
- **Inner Surface**: Gentle off-white (#f8fafc)
- **Text**: Dark colors for readability
- **Accents**: Same purple and blue scheme

### Notifications

#### **Types of Notifications**
1. **Windows Toast**: Native system notifications
2. **Custom Popup**: Prominent dialog with task details
3. **Sound Alert**: Audio notification
4. **Console Output**: Fallback for debugging

#### **Notification Actions**
- **Dismiss**: Close the notification
- **Snooze**: Remind again later
- **Click**: Focus the TASKY window

#### **Settings**
- Notifications appear 15 seconds before due time
- Background monitoring runs continuously
- Sound notifications use system sounds

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Add Task | Ctrl+N (not implemented yet) |
| Edit Task | Enter (when row selected) |
| Delete Task | Delete (when row selected) |
| Refresh | F5 (not implemented yet) |
| Search | Ctrl+F (focus search box) |

### Tips & Tricks

#### **Productivity Tips**
- Use descriptive titles for quick identification
- Set realistic due dates with buffer time
- Use the search to find specific tasks quickly
- Mark tasks complete as you finish them

#### **Window Management**
- Resize the window to fit your screen
- Use compact mode for small displays
- Toggle themes based on lighting conditions
- Keep TASKY running for notifications

#### **Data Management**
- Tasks are automatically saved to SQLite
- Database file: `tasks.db` in the app directory
- Backup the database file for data safety
- Export functionality coming soon

## 🛠️ Development

### Project Structure
```
TASKY/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── models.py              # Task data model
├── database.py            # SQLite database operations
├── notifications.py       # Notification system
├── scheduler.py           # Background task monitoring
├── ui/                    # User interface components
│   ├── __init__.py       # UI package initialization
│   ├── main_window.py    # Main application window
│   ├── task_dialog.py    # Task creation/editing dialog
│   ├── theme_manager.py  # Theme management system
│   └── notification_popup.py  # Custom notification dialog
├── run.bat               # Windows batch launcher
├── run.ps1               # PowerShell launcher
└── test_app.py           # Core functionality testing
```

### Key Components

#### **MainWindow** (`ui/main_window.py`)
- Main application interface
- Task table and management controls
- Theme switching and search functionality

#### **TaskDialog** (`ui/task_dialog.py`)
- Modal dialog for task creation/editing
- Form validation and data handling
- Compact, user-friendly design

#### **ThemeManager** (`ui/theme_manager.py`)
- Dynamic theme switching system
- CSS-like stylesheet generation
- Color palette management

#### **NotificationManager** (`notifications.py`)
- Multi-layered notification system
- Windows toast integration
- Fallback mechanisms for reliability

#### **TaskScheduler** (`scheduler.py`)
- Background task monitoring
- Asynchronous notification scheduling
- Thread-safe operation

### Development Setup

#### **Environment Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8
```

#### **Running Tests**
```bash
# Test core functionality
python test_app.py

# Run with specific Python version
python3.9 main.py
```

#### **Code Style**
- **Formatting**: Black code formatter
- **Linting**: Flake8 for code quality
- **Type Hints**: Python type annotations
- **Documentation**: Docstrings for all functions

### Building & Distribution

#### **Requirements for Distribution**
- Python 3.8+ runtime
- PyQt6 libraries
- Windows 10/11 for full functionality

#### **Creating Executable**
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name TASKY main.py

# The executable will be in dist/TASKY.exe
```

#### **Package Structure**
```
TASKY-Distribution/
├── TASKY.exe           # Main executable
├── tasks.db            # Database (if exists)
├── README.txt          # Installation instructions
└── LICENSE             # License information
```

## 🔧 Troubleshooting

### Common Issues

#### **"ModuleNotFoundError: No module named 'PyQt6'"**
```bash
# Solution: Install PyQt6
pip install PyQt6

# If using specific Python version:
python3.9 -m pip install PyQt6
```

#### **"ModuleNotFoundError: No module named 'win10toast'"**
```bash
# Solution: Install win10toast
pip install win10toast

# Alternative: Use pip3
pip3 install win10toast
```

#### **Notifications Not Working**
- Ensure Windows 10/11 is up to date
- Check notification permissions in Windows Settings
- Verify TASKY is running in the background
- Check system sound settings

#### **Database Errors**
- Ensure write permissions in the app directory
- Check if `tasks.db` is locked by another process
- Restart TASKY if database is corrupted
- Backup and delete database file if needed

#### **UI Display Issues**
- Update graphics drivers
- Check Windows DPI settings
- Try different theme modes
- Restart the application

### Performance Optimization

#### **For Large Task Lists**
- Use search to filter tasks
- Close unused applications
- Ensure adequate RAM (2GB+ recommended)
- Regular database maintenance

#### **Background Performance**
- Notification system uses minimal resources
- Scheduler runs in separate thread
- Database operations are optimized
- Memory usage scales with task count

## 📝 Changelog

### Version 1.0.0 (Current)
- ✨ Initial release with core functionality
- 🎨 Dark and dimmed light themes
- 🔔 Windows notifications with sound
- 📱 Responsive, compact UI design
- 🔍 Real-time search functionality
- 💾 SQLite database persistence
- ⚡ Background task monitoring

### Planned Features
- 📊 Task statistics and analytics
- 📅 Calendar view integration
- 🔄 Task templates and recurring tasks
- 📤 Import/export functionality
- 🎯 Priority levels and categories
- 🌐 Cloud synchronization
- 📱 Mobile companion app

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Ways to Contribute**
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Fix bugs and implement features
- 🎨 Enhance the UI/UX
- 🧪 Add tests and improve reliability

### **Development Guidelines**
- Fork the repository
- Create a feature branch
- Make your changes
- Add tests if applicable
- Submit a pull request
- Follow the code style guide

### **Code Standards**
- Python 3.8+ compatibility
- Type hints for all functions
- Comprehensive docstrings
- Error handling and logging
- Cross-platform considerations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyQt6**: Modern Python GUI framework
- **SQLite**: Lightweight database engine
- **Windows Toast**: Native notification system
- **Open Source Community**: For inspiration and tools

## 📞 Support

### **Getting Help**
- 📖 Check this documentation first
- 🐛 Report issues on GitHub
- 💬 Ask questions in Discussions
- 📧 Contact: your.email@example.com

### **Resources**
- [PyQt6 Documentation](https://doc.qt.io/qtforpython/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Windows Toast Notifications](https://docs.microsoft.com/en-us/windows/apps/design/shell/tiles-and-notifications/)

---

**Made with ❤️ by the TASKY Team**

*TASKY - Your Personal Task Assistant*
