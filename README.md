# 🎯 TASKY - Your Personal Task Assistant

[![Build Status](https://github.com/yourusername/TASKY/workflows/Build%20TASKY/badge.svg)](https://github.com/yourusername/TASKY/actions) [![Test Status](https://github.com/yourusername/TASKY/workflows/Test%20TASKY/badge.svg)](https://github.com/yourusername/TASKY/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![Version: 2.0.0](https://img.shields.io/badge/version-2.0.0-purple.svg)](CHANGELOG.md)

**A high-fidelity task management application built with a modern React frontend and a robust Python/PyQt6 backend.**

---

## 🚀 **Quick Start**

### **Download & Run (TASKY-Distribution/TASKY.exe)**
1. **Download** the latest release from [Releases](TASKY-Distribution/TASKY.exe)
2. **Extract** the ZIP file to any folder
3. **Double-click** `TASKY.exe` to run
4. **No Python installation required!** 🎉

### **Run from Source**
1. **Frontend Setup**:
   ```bash
   cd web
   pnpm install
   pnpm dev
   ```
2. **Backend Setup**:
   ```bash
   # In a new terminal
   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

### **Build Executable**
```bash
python build.py        # or build.bat / .\build.ps1
```

---

## ✨ **Features**

| 🎨 **Premium UI** | Stunning dark mode interface built with React, Tailwind, and OKLCH colors |
| 🎯 **Task Management** | Create, edit, delete, complete, and duplicate tasks |
| 🔗 **Python Bridge** | Seamless integration between React frontend and SQLite backend |
|  pomodoro_timer **Pomodoro Timer** | High-fidelity focus timer with immersive dark aesthetic |
| 📊 **Analytics** | Real-time analytics dashboard with deep data insights |
| 🔔 **Smart Notifications** | System-level tray alerts and in-app popup overlays |
| 💾 **SQLite Persistence** | Reliable local data persistence with zero configuration |

---

## 📋 **System Requirements**

- **OS**: Windows 10/11
- **RAM**: 150 MB minimum
- **Storage**: 60 MB available space
- **Python**: 3.8+ (for development only)

---

## 🛠️ **Development Setup**

### **Prerequisites**
- Python 3.8+
- pip package manager

### **Install & Run**
```bash
pip install -r requirements.txt
python main.py
```

### **Project Structure**
```
TASKY/
├── main.py                     # Application entry point
├── bridge.py                   # Python-JavaScript communication bridge
├── models.py                   # Data models (Task, Category, etc.)
├── database.py                 # SQLite database management
├── web/                        # React Frontend (Vite, Tailwind, TypeScript)
│   ├── src/                    # Frontend source code
│   └── public/                 # Static assets & qwebchannel.js
├── ui/
│   ├── main_window.py          # PyQt6 host for the WebEngine view
│   ├── tray_manager.py         # System tray management
│   ├── notification_popup.py   # System-level notifications
│   ├── signals.py              # Backend signal bus
│   └── theme_manager.py        # System theme tokens
├── requirements.txt            # Python dependencies
└── package.json                # Node.js dependencies
```

---

## 🔨 **Building Executables**

```bash
# Windows batch
build.bat

# PowerShell
.\build.ps1

# Python
python build.py

# Manual PyInstaller
pyinstaller --onefile --windowed --name=TASKY main.py
```

---

## 📱 **Usage Guide**

### **Basic Operations**
- **Add Task**: Click **＋ New Task** or press `Ctrl+N`
- **Edit Task**: Click ✏️ on a task card
- **Complete Task**: Click ✓ on a task card
- **Delete Task**: Click 🗑️ on a task card
- **Duplicate Task**: Click the duplicate icon on a task card
- **Search**: Use `Ctrl+F` to focus the search box

### **Pomodoro Timer**
1. Click **⏱ Focus** in the header or press `Ctrl+P`
2. Select a task and set work / break durations
3. Start the session — the ring counts down
4. Completed sessions are logged for analytics

### **Analytics**
- Click **📊 Analytics** in the header
- View 7-day completion and time-tracking bar charts
- See your most productive hours breakdown

### **Recurring Tasks**
- When creating/editing a task, choose a recurrence rule
- Supported: Every Day, Weekdays, Weekends, Mon/Wed/Fri, Monthly (1st or 15th)
- Completing a recurring task auto-creates the next occurrence

### **System Tray**
- TASKY minimizes to the tray when you close the window (configurable in Settings)
- Right-click the tray icon for quick actions
- Double-click to restore the window

### **Export**
- **File → Export to CSV…** or **File → Export to JSON…**

---

## ⌨️ **Keyboard Shortcuts**

| Action | Shortcut |
|--------|----------|
| Add Task | `Ctrl+N` |
| Focus Search | `Ctrl+F` |
| Pomodoro Timer | `Ctrl+P` |
| Toggle Theme | `Ctrl+T` |
| Open Settings | `Ctrl+,` |
| Refresh | `F5` |
| Quit | `Ctrl+Q` |

---

## 🔔 **Notification System**

TASKY provides layered notifications:
- **Windows Toast**: Native system notifications via `winotify`
- **In-App Popup**: Overlay popup inside the TASKY window
- **Background Monitoring**: Works even when minimized to tray
- **Configurable Lead Time**: Set how early to alert (Settings → Notifications)

---

## 🎨 **Themes**

- **Dark Mode** (default): Deep navy/slate with purple accents
- **Light Mode**: Soft grey surfaces with consistent purple/blue accents
- Toggle with `Ctrl+T` or the ☀️🌙 button — preference is saved automatically

---

## 🚧 **Troubleshooting**

### **Notifications Not Working**
- Ensure Windows notifications are enabled in system settings
- Check Settings → Notifications within TASKY
- Verify Windows 10/11 is up to date

### **Build Errors**
- Install PyInstaller: `pip install pyinstaller`
- Ensure all dependencies from `requirements.txt` are installed

### **Database Issues**
- Verify write permissions on the folder containing `tasks.db`
- Close any other running TASKY instances before opening
- Delete `tasks.db` to reset all data (⚠️ irreversible)

### **Getting Help**
- 📖 Read the [User Manual](USER_MANUAL.md)
- 🐛 Report bugs via [GitHub Issues](https://github.com/yourusername/TASKY/issues)
- 💡 Request features via [GitHub Discussions](https://github.com/yourusername/TASKY/discussions)

---

## 🤝 **Contributing**

We welcome contributions!

- 🐛 **Report Bugs**: Find and report issues
- 💡 **Suggest Features**: Share your ideas
- 🔧 **Improve Code**: Submit pull requests
- 📚 **Update Documentation**: Help keep docs current

**Guidelines**: Follow PEP 8, add tests for new features, update docs for changes, use descriptive commit messages.

---

## 📄 **License**

MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **PyQt6**: Modern Python GUI framework
- **SQLite**: Lightweight database engine
- **winotify**: Windows toast notifications
- **PyInstaller**: Executable packaging

---

## 📞 **Support**

- 📧 **Email**: [billymwangi200@gmail.com]

---

<div align="center">

**If TASKY helps you stay organized, please give us a ⭐ star!**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/TASKY?style=social)](https://github.com/yourusername/TASKY/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/TASKY?style=social)](https://github.com/yourusername/TASKY/network/members)

</div>

---

**Made with ❤️ by the TASKY Team** · *TASKY v2.0.0 — Your Personal Task Assistant*
