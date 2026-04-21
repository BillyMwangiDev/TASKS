# 📝 Changelog

All notable changes to TASKY will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Cloud synchronization
- Mobile companion app
- Team collaboration features
- Plugin system

---

## [2.0.0] - 2026-04-19

### Added
- 🗂️ **Sidebar navigation** — collapsible left panel with smart lists: All Tasks, Today, Tomorrow, This Week, Overdue, plus per-category views
- 🃏 **Card-based task list** — replaced table with rich task cards showing priority badge, tags, category, time estimate, and subtask count
- 🔍 **Filter bar** — quick-filter buttons (All / Today / This Week / Overdue) combined with inline search and sort
- 🏷️ **Priority system** — High 🔴 / Medium 🟡 / Low 🔵 / None ⚪ with color-coded badges
- 📁 **Categories** — user-defined project categories with custom color and icon; sidebar shows per-category task counts
- 🏷️ **Tags** — free-form tag field with autocomplete from existing tags
- 🔁 **Recurring tasks** — recurrence rules: daily, weekdays, weekends, Mon/Wed/Fri, monthly (1st or 15th); completing a recurring task spawns the next occurrence
- 📋 **Subtasks** — nest child tasks under any parent task
- ⏱️ **Pomodoro timer** — dedicated panel with circular SVG-style progress ring, configurable work/break durations, and session logging (`Ctrl+P`)
- 📊 **Analytics dashboard** — 7-day bar charts for task completions and focused minutes, most-productive-hours breakdown
- ⚙️ **Settings dialog** — tabbed panel: General, Notifications, Pomodoro, Keyboard, About (`Ctrl+,`)
- 🖥️ **System tray** — minimize-to-tray support; right-click tray menu; quick-add dialog from tray icon; tooltip shows pending/overdue counts
- 💾 **Export** — File → Export to CSV… / Export to JSON…
- 🔔 **In-app notification popup** — overlay popup inside the window alongside native Windows toast
- 📊 **Streak counter** — consecutive-day completion streak shown in stats bar
- 🔢 **Estimated time** — optional minutes estimate per task, shown on the card
- 📝 **Notes field** — freeform notes section in the task dialog
- 🗃️ **Task duplication** — duplicate any task with one click
- 📋 **Menu bar** — File, View, Tools, and Help menus with full keyboard shortcut coverage
- 🔑 **New shortcuts** — `Ctrl+P` (Pomodoro), `Ctrl+,` (Settings), `Ctrl+Q` (Quit)
- 🗄️ **Database migrations** — automatic schema upgrade from v1 databases (no data loss)

### Changed
- App version bumped to **2.0.0** (`app.setApplicationVersion("2.0.0")`)
- Minimum window size increased to **800×560** (default 1100×700) for the new layout
- Notification backend switched from `win10toast` to **`winotify`** for better PyInstaller compatibility
- Task dialog redesigned with scrollable body, priority/category/tags/recurrence/subtask fields
- Stats bar now shows Total / Done / Pending / Overdue / Streak
- PyQt6 updated to **6.9.1**

### Removed
- Plain table-based task list (replaced by card list)

---

## [1.0.0] - 2024-08-22

### Added
- ✨ **Core Task Management**: Create, edit, delete, and complete tasks
- 🎨 **Dual Theme System**: Dark and dimmed light modes
- 🔔 **Smart Notifications**: Windows toast notifications with sound alerts
- ⏱️ **Time Tracking**: Monitor time spent on tasks with start/stop functionality
- 🔍 **Real-time Search**: Find tasks quickly with instant filtering
- 📊 **Live Statistics**: Task counts and productivity metrics
- ⌨️ **Keyboard Shortcuts**: `Ctrl+N`, `Ctrl+F`, `Ctrl+T`, `F5`, `Delete`, `Enter`
- 💾 **SQLite Database**: Reliable data persistence
- 🖥️ **Modern UI**: Compact table-based task list

### Technical
- PyQt6 GUI framework
- SQLite database with single `tasks` table
- Background task scheduler for due-date notifications
- Windows toast via `win10toast`

---

## [0.9.0] - 2024-08-21

### Added
- Initial application structure
- Basic task management functionality
- Simple notification system
- Basic UI framework

---

## [0.8.0] - 2024-08-20

### Added
- Time tracking functionality
- Task statistics
- Keyboard shortcuts
- Enhanced search capabilities

### Changed
- Improved button aesthetics
- Compact header design
- Window sizing optimizations

---

## [0.7.0] - 2024-08-19

### Added
- Dark/light theme system
- Notification sound support
- Task completion tracking
- Real-time UI updates

---

## [0.6.0] - 2024-08-18

### Added
- Windows toast notifications
- Background task monitoring
- Due date alerts

---

## [0.5.0] - 2024-08-17

### Added
- Basic PyQt6 application structure
- SQLite database integration
- Task data model
- Simple GUI interface

---

## 📝 **Notes**

- **Breaking Changes**: Marked with ⚠️ in release notes
- **Security**: Security-related changes are highlighted
- **Migration**: v1 databases are automatically migrated on first v2 launch

---

**For more information, see [CONTRIBUTING.md](CONTRIBUTING.md)**
