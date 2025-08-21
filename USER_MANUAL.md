# TASKY User Manual 📖

**Complete Guide to Using TASKY - Your Personal Task Assistant**

---

## 🚀 **Quick Start Guide**

### **First Launch**
1. **Install Dependencies**: Run `install.bat` or `install.ps1`
2. **Launch TASKY**: Double-click `run.bat` or run `python main.py`
3. **Add Your First Task**: Click the **➕ Add** button
4. **Start Organizing**: Create, track, and complete tasks

---

## 🎯 **Core Features**

### **1. Task Management**
- **Create Tasks**: Add new tasks with title, description, and due date
- **Edit Tasks**: Modify existing task details anytime
- **Complete Tasks**: Mark tasks as done with one click
- **Delete Tasks**: Remove unwanted tasks permanently
- **Search & Filter**: Find tasks quickly with real-time search

### **2. Time Tracking** ⏱️
- **Start Tracking**: Click **⏱️ Track** to begin timing a task
- **Stop Tracking**: Click **⏹️ Stop** to end timing
- **View Progress**: See total time spent on each task
- **Productivity Insights**: Monitor your time management

### **3. Smart Notifications** 🔔
- **Due Date Alerts**: Get notified before tasks are due
- **Multiple Formats**: Windows toast, custom popups, and sound
- **Background Monitoring**: Works even when TASKY is minimized
- **Snooze Options**: Dismiss or postpone notifications

### **4. Theme System** 🎨
- **Dark Mode**: Easy on the eyes for evening use
- **Light Mode**: Dimmed for comfortable daytime use
- **Quick Toggle**: Switch themes with **☀️🌙** button
- **Keyboard Shortcut**: Press **Ctrl+T** to toggle

---

## ⌨️ **Keyboard Shortcuts**

| Action | Shortcut | Description |
|--------|----------|-------------|
| **Add Task** | `Ctrl+N` | Create a new task |
| **Edit Task** | `Enter` | Edit selected task |
| **Delete Task** | `Delete` | Remove selected task |
| **Refresh** | `F5` | Reload all tasks |
| **Search** | `Ctrl+F` | Focus search box |
| **Theme Toggle** | `Ctrl+T` | Switch dark/light mode |

---

## 🖥️ **Interface Guide**

### **Header Section**
- **📋 TASKY**: App logo and title
- **☀️🌙**: Theme toggle button
- **🔔 Status**: Notification system indicator

### **Search Bar**
- **🔍 Search**: Type to filter tasks in real-time
- **Smart Search**: Searches title, description, and due dates
- **Clear Search**: Delete text to show all tasks

### **Task Table**
| Column | Description | Features |
|--------|-------------|----------|
| **Title** | Task name | Expandable, main identifier |
| **Description** | Task details | Truncated preview (40 chars) |
| **Due Date** | Deadline | MM/DD HH:MM format |
| **Status** | Completion | ✓ Done or ⏰ Pending |
| **Time Until Due** | Countdown | Real-time updates every 30s |
| **Time Spent** | Tracking | Total time spent on task |

### **Button Toolbar**
- **➕ Add**: Create new task
- **✏️ Edit**: Modify selected task
- **✓ Done**: Mark task complete
- **🗑️ Del**: Delete selected task
- **⏱️ Track**: Start/stop time tracking
- **🔄**: Refresh task list

### **Statistics Bar**
- **📊 Tasks**: Total number of tasks
- **Completed**: Number of finished tasks
- **Pending**: Number of active tasks
- **Overdue**: Number of late tasks
- **Color Coding**: Red for overdue, blue for normal

---

## ⏱️ **Time Tracking Guide**

### **Getting Started**
1. **Select a Task**: Click on any pending task
2. **Start Tracking**: Click **⏱️ Track** button
3. **Work on Task**: Focus on your task
4. **Stop Tracking**: Click **⏹️ Stop** when done

### **Time Display**
- **Format**: Hours and minutes (e.g., "2h 30m")
- **Real-time**: Updates as you work
- **Persistent**: Saved between sessions
- **Completed Tasks**: Time tracking disabled

### **Best Practices**
- **Start Early**: Begin tracking when you start working
- **Be Consistent**: Track all time spent on tasks
- **Review Regularly**: Check your time patterns
- **Set Goals**: Use time data to improve estimates

---

## 🔔 **Notification System**

### **Types of Notifications**
1. **Windows Toast**: Native system notifications
2. **Custom Popup**: Prominent dialog with task details
3. **Sound Alert**: Audio notification
4. **Console Output**: Fallback for debugging

### **Notification Actions**
- **Dismiss**: Close the notification
- **Snooze**: Remind again later
- **Click**: Focus the TASKY window

### **Settings & Behavior**
- **Timing**: Notifications appear 15 seconds before due
- **Frequency**: Each task notified only once
- **Background**: Works when TASKY is minimized
- **Sound**: Uses system notification sounds

---

## 🎨 **Theme Customization**

### **Dark Mode** (Default)
- **Outer Background**: Dark grey (#1f2937)
- **Inner Surface**: Medium grey (#374151)
- **Text**: Light colors for contrast
- **Accents**: Purple (#8b5cf6) and Blue (#3b82f6)

### **Light Mode** (Dimmed)
- **Outer Background**: Soft light grey (#e5e7eb)
- **Inner Surface**: Gentle off-white (#f8fafc)
- **Text**: Dark colors for readability
- **Accents**: Same purple and blue scheme

### **Switching Themes**
- **Manual Toggle**: Click **☀️🌙** button
- **Keyboard**: Press **Ctrl+T**
- **Instant**: Changes apply immediately
- **Persistent**: Theme choice remembered

---

## 📱 **Window Management**

### **Resizing**
- **Default Size**: 420x400 pixels
- **Minimum Size**: 380x350 pixels
- **Maximum Size**: 800x700 pixels
- **Flexible**: Resize to fit your screen

### **Layout Options**
- **Compact Mode**: Use smaller window for productivity
- **Expanded View**: Larger window for detailed work
- **Column Adjustments**: Resize table columns as needed
- **Responsive Design**: Adapts to different screen sizes

---

## 💾 **Data Management**

### **Storage**
- **Database**: SQLite file (`tasks.db`)
- **Location**: Same folder as TASKY
- **Automatic**: Saves changes immediately
- **Reliable**: No data loss on crashes

### **Backup & Safety**
- **Manual Backup**: Copy `tasks.db` file
- **Version Control**: Track changes over time
- **Export**: Save tasks to external formats (coming soon)
- **Reset**: Delete database to start fresh

### **Performance**
- **Fast Loading**: Optimized database queries
- **Memory Efficient**: Scales with task count
- **Background Processing**: Non-blocking operations
- **Regular Updates**: Statistics refresh automatically

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Notifications Not Working**
- **Check Windows Settings**: Ensure notifications are enabled
- **Verify Permissions**: Allow TASKY to show notifications
- **Update Windows**: Ensure Windows 10/11 is current
- **Sound Settings**: Check system notification sounds

#### **Database Errors**
- **File Permissions**: Ensure write access to folder
- **File Locked**: Close other instances of TASKY
- **Corrupted Data**: Delete `tasks.db` to reset
- **Disk Space**: Ensure sufficient storage

#### **UI Display Issues**
- **Graphics Drivers**: Update display drivers
- **DPI Settings**: Check Windows scaling
- **Theme Issues**: Try switching themes
- **Restart App**: Close and reopen TASKY

### **Performance Tips**
- **Large Task Lists**: Use search to filter tasks
- **Memory Usage**: Close unused applications
- **Regular Maintenance**: Restart app periodically
- **Database Size**: Monitor `tasks.db` file size

---

## 📊 **Productivity Tips**

### **Task Organization**
- **Clear Titles**: Use descriptive, specific names
- **Realistic Deadlines**: Set achievable due dates
- **Priority Order**: Focus on most important tasks first
- **Regular Review**: Check and update task status

### **Time Management**
- **Track Everything**: Monitor time on all tasks
- **Set Time Goals**: Estimate and track actual time
- **Break Down Tasks**: Split large tasks into smaller ones
- **Review Patterns**: Analyze your time usage

### **Workflow Optimization**
- **Use Shortcuts**: Learn keyboard shortcuts for speed
- **Batch Operations**: Group similar tasks together
- **Regular Updates**: Keep task information current
- **Progress Tracking**: Monitor completion rates

---

## 🚀 **Advanced Features**

### **Search & Filter**
- **Real-time Search**: Type to filter instantly
- **Multi-field Search**: Searches title, description, dates
- **Smart Matching**: Finds partial text matches
- **Clear Results**: Easy to return to full view

### **Statistics & Insights**
- **Task Counts**: Total, completed, pending, overdue
- **Visual Indicators**: Color-coded status information
- **Real-time Updates**: Statistics refresh automatically
- **Productivity Metrics**: Track your progress

### **Customization**
- **Theme Switching**: Dark and light modes
- **Window Sizing**: Flexible window dimensions
- **Column Layout**: Adjustable table columns
- **Button States**: Dynamic button availability

---

## 🔮 **Future Features**

### **Planned Enhancements**
- **Task Categories**: Organize by project or type
- **Priority Levels**: High, medium, low priority
- **Recurring Tasks**: Daily, weekly, monthly tasks
- **Calendar View**: Monthly and weekly calendar
- **Export Options**: CSV, JSON, calendar formats
- **Cloud Sync**: Backup and synchronization
- **Mobile App**: iOS and Android companion

### **User Requests**
- **Custom Notifications**: Personalized alert times
- **Task Templates**: Save common task patterns
- **Time Reports**: Detailed time analysis
- **Integration**: Connect with other productivity tools

---

## 📞 **Support & Help**

### **Getting Help**
- **Documentation**: Check this manual first
- **GitHub Issues**: Report bugs and request features
- **Community**: Join discussions and share tips
- **Contact**: Reach out for direct support

### **Resources**
- **PyQt6 Documentation**: GUI framework details
- **SQLite Guide**: Database information
- **Windows Notifications**: System integration details
- **Python Resources**: Programming language help

---

## 📝 **Changelog**

### **Version 1.0.0** (Current)
- ✨ **Core Task Management**: Create, edit, delete, complete tasks
- 🎨 **Dual Theme System**: Dark and dimmed light modes
- 🔔 **Smart Notifications**: Windows toast with sound alerts
- ⏱️ **Time Tracking**: Monitor time spent on tasks
- 🔍 **Real-time Search**: Find tasks quickly
- 📊 **Live Statistics**: Task counts and productivity metrics
- ⌨️ **Keyboard Shortcuts**: Fast keyboard navigation
- 📱 **Responsive Design**: Compact, resizable interface

---

## 🤝 **Contributing**

### **How to Help**
- **Report Bugs**: Find and report issues
- **Suggest Features**: Share your ideas
- **Improve Code**: Submit code improvements
- **Update Documentation**: Help keep docs current
- **Test Features**: Try new functionality

### **Development**
- **Python 3.8+**: Modern Python features
- **PyQt6**: Cross-platform GUI framework
- **SQLite**: Lightweight database
- **Open Source**: MIT license for freedom

---

**Made with ❤️ by the TASKY Team**

*TASKY - Your Personal Task Assistant*
