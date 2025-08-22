# 🎯 TASKY - Your Personal Task Assistant

[![Build Status](https://github.com/yourusername/TASKY/workflows/Build%20TASKY/badge.svg)](https://github.com/yourusername/TASKY/actions) [![Test Status](https://github.com/yourusername/TASKY/workflows/Test%20TASKY/badge.svg)](https://github.com/yourusername/TASKY/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

**A modern, feature-rich task management application built with Python and PyQt6**

---

## 🚀 **Quick Start**

### **Download & Run (Recommended)**
1. **Download** the latest release from [Releases](https://github.com/BillyMwangiDev/TASKY/releases)
2. **Extract** the ZIP file to any folder
3. **Double-click** `TASKY.exe` to run
4. **No Python installation required!** 🎉

### **Build from Source**
```bash
# Clone the repository
git clone https://github.com/yourusername/TASKY.git
cd TASKY

# Install dependencies
pip install -r requirements.txt

# Build executable
python build.py

# Run the application
python main.py
```

---

## ✨ **Features**

| Feature | Description |
|---------|-------------|
| 🎯 **Task Management** | Create, edit, delete, and complete tasks |
| ⏱️ **Time Tracking** | Monitor time spent on tasks |
| 🔔 **Smart Notifications** | Windows toast notifications with sound |
| 🎨 **Theme System** | Dark and light modes |
| 🔍 **Real-time Search** | Find tasks instantly |
| 📊 **Live Statistics** | Track productivity metrics |
| ⌨️ **Keyboard Shortcuts** | Fast navigation and actions |
| 💾 **SQLite Database** | Reliable data persistence |
| 🖥️ **Modern UI** | Clean, responsive interface |

---

## 🖼️ **Screenshots**

*[Add screenshots here when you have them]*

---

## 📋 **System Requirements**

- **OS**: Windows 10/11
- **RAM**: 100MB minimum
- **Storage**: 50MB available space
- **Python**: 3.8+ (for development only)

---

## 🛠️ **Development Setup**

### **Prerequisites**
- Python 3.8+
- pip package manager



### **Project Structure**
```
TASKY/
├── main.py                 # Application entry point
├── models.py               # Data models
├── database.py             # Database management
├── notifications.py        # Notification system
├── scheduler.py            # Task scheduling
├── ui/                     # User interface modules
│   ├── main_window.py      # Main application window
│   ├── task_dialog.py      # Task creation/editing dialog
│   └── theme_manager.py    # Theme management
├── build.py                # Build script for executables
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🔨 **Building Executables**

### **Automatic Build**
```bash
# Windows
build.bat

# PowerShell
.\build.ps1

# Python
python build.py
```

### **Manual Build**
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name=TASKY main.py
```

---

## 📱 **Usage Guide**

### **Basic Operations**
- **Add Task**: Click ➕ Add button or press `Ctrl+N`
- **Edit Task**: Select task and press `Enter` or click ✏️ Edit
- **Complete Task**: Select task and click ✓ Done
- **Delete Task**: Select task and press `Delete` or click 🗑️ Del
- **Search**: Use `Ctrl+F` to focus search box

### **Time Tracking**
1. Select a pending task
2. Click ⏱️ Track to start timing
3. Click ⏹️ Stop when finished
4. View total time spent in the "Time Spent" column

### **Theme Switching**
- Click the ☀️🌙 button to toggle themes
- Use `Ctrl+T` keyboard shortcut
- Theme preference is automatically saved

### **Keyboard Shortcuts**
| Action | Shortcut |
|--------|----------|
| Add Task | `Ctrl+N` |
| Edit Task | `Enter` |
| Delete Task | `Delete` |
| Refresh | `F5` |
| Search | `Ctrl+F` |
| Theme Toggle | `Ctrl+T` |

---

## 🔔 **Notification System**

TASKY provides smart notifications:
- **Due Date Alerts**: 15 seconds before tasks are due
- **Multiple Formats**: Windows toast, custom popups, sound
- **Background Monitoring**: Works even when minimized
- **Snooze Options**: Dismiss or postpone notifications

---

## 🎨 **Customization**

### **Themes**
- **Dark Mode**: Easy on the eyes for evening use
- **Light Mode**: Dimmed for comfortable daytime use
- **Custom Colors**: Purple and blue accent scheme

### **Window Management**
- **Resizable**: Flexible window dimensions
- **Compact Design**: Ultra-compact header elements
- **Responsive Layout**: Adapts to different screen sizes

---

## 🚧 **Troubleshooting**

### **Common Issues**

#### **Notifications Not Working**
- Ensure Windows notifications are enabled
- Check system notification permissions
- Verify Windows 10/11 is up to date

#### **Build Errors**
- Install PyInstaller: `pip install pyinstaller`
- Ensure all dependencies are installed
- Check Python version compatibility

#### **Runtime Errors**
- Verify SQLite database permissions
- Check available disk space
- Ensure Windows compatibility

### **Getting Help**
- 📖 Read the [User Manual](USER_MANUAL.md)
- 🐛 Report bugs via [GitHub Issues](https://github.com/yourusername/TASKY/issues)
- 💡 Request features via [GitHub Discussions](https://github.com/yourusername/TASKY/discussions)

---

## 🤝 **Contributing**

We welcome contributions! Here's how you can help:

### **Ways to Contribute**
- 🐛 **Report Bugs**: Find and report issues
- 💡 **Suggest Features**: Share your ideas
- 🔧 **Improve Code**: Submit code improvements
- 📚 **Update Documentation**: Help keep docs current
- 🧪 **Test Features**: Try new functionality

### **Development Guidelines**
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation for changes
- Use descriptive commit messages

### **Pull Request Process**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **PyQt6**: Modern Python GUI framework
- **SQLite**: Lightweight database engine
- **win10toast**: Windows notification integration
- **PyInstaller**: Executable packaging

---

## 📞 **Support & Community**

- 📧 **Email**: [billymwangi200@gmail.com]


---

## 🌟 **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/TASKY&type=Date)](https://star-history.com/#yourusername/TASKY&Date)

---

**Made with ❤️ by the TASKY Team**

*TASKY - Your Personal Task Assistant*

---

<div align="center">

**If TASKY helps you stay organized, please give us a ⭐ star!**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/TASKY?style=social)](https://github.com/yourusername/TASKY/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/TASKY?style=social)](https://github.com/yourusername/TASKY/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/yourusername/TASKY?style=social)](https://github.com/yourusername/TASKY/watchers)

</div>
