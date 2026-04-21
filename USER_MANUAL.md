# TASKY User Manual 📖

**Complete Guide to TASKY v2.0.0 — Your Personal Task Assistant**

---

## 🚀 **Quick Start**

### **First Launch**
1. **Install Dependencies** (source only): `pip install -r requirements.txt`
2. **Launch TASKY**: `python main.py` or double-click `TASKY.exe`
3. **Add Your First Task**: Click **＋ New Task** or press `Ctrl+N`

---

## 🖥️ **Interface Overview**

TASKY v2 uses a three-zone layout:

```
┌─────────────────────────────────────────────────────────┐
│  Header: logo · ＋New Task · ⏱Focus · 📊Analytics · ☀️🌙  │
├────────────────┬────────────────────────────────────────┤
│                │  Filter bar (All / Today / Week / …)   │
│   Sidebar      │  ─────────────────────────────────────  │
│  (Smart Lists  │  Task Cards                             │
│  + Categories) │                                         │
│                │                                         │
├────────────────┴────────────────────────────────────────┤
│  Stats bar: Total · Done · Pending · Overdue · Streak   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 **Task Management**

### **Adding a Task**
1. Click **＋ New Task** or press `Ctrl+N`
2. Fill in the task dialog fields (see below)
3. Click **Save**

### **Task Dialog Fields**

| Field | Description |
|-------|-------------|
| **Title** | Short task name (required) |
| **Description** | Optional details |
| **Due Date** | Deadline date and time |
| **Priority** | 🔴 High / 🟡 Medium / 🔵 Low / ⚪ None |
| **Category** | Assign to a user-defined category |
| **Tags** | Comma-separated keywords (with autocomplete) |
| **Estimated Time** | Expected minutes to complete |
| **Notes** | Freeform notes section |
| **Recurrence** | Repeat rule (see Recurring Tasks below) |
| **Subtasks** | Add nested child tasks |

### **Editing a Task**
- Click the ✏️ icon on any task card

### **Completing a Task**
- Click the ✓ icon on the card — the card grays out and moves to completed

### **Deleting a Task**
- Click the 🗑️ icon on the card

### **Duplicating a Task**
- Click the duplicate icon on the card — creates an identical copy

---

## 🗂️ **Sidebar Navigation**

The collapsible left sidebar provides smart views:

| View | Shows |
|------|-------|
| 🗂 All Tasks | All tasks regardless of date |
| 📅 Today | Tasks due today |
| 🔜 Tomorrow | Tasks due tomorrow |
| 📆 This Week | Tasks due within the next 7 days |
| 🔴 Overdue | Tasks past their due date |
| *(Category)* | Tasks belonging to that category |

Click the **◀** collapse button to hide the sidebar and gain more card-list space.

### **Managing Categories**
- Click **＋ Add Category** at the bottom of the sidebar
- Set a name, pick a color, and choose an icon (emoji)
- Delete or edit categories via the context options next to each category name

---

## 🔍 **Filtering & Search**

### **Filter Bar** (above the card list)
| Button | Effect |
|--------|--------|
| All | Show all tasks |
| Today | Tasks due today |
| This Week | Tasks due this week |
| Overdue | Past-due tasks |

### **Search**
- Press `Ctrl+F` or click the search box on the right of the filter bar
- Searches across title, description, and tags in real time
- Clear the box to return to the full view

### **Sort**
- Use the sort dropdown in the filter bar to order by Due Date, Priority, or Creation Date

---

## 🔁 **Recurring Tasks**

When creating or editing a task, choose a **Recurrence** rule:

| Rule | Schedule |
|------|----------|
| No recurrence | One-time task |
| Every day | Daily at the same time |
| Weekdays | Monday–Friday |
| Weekends | Saturday–Sunday |
| Mon / Wed / Fri | Three times a week |
| Monthly (1st) | First day of each month |
| Monthly (15th) | Fifteenth of each month |

When you **complete** a recurring task, TASKY automatically creates the next occurrence.

---

## 📋 **Subtasks**

- Open a task in the task dialog and use the **Subtasks** section to add child tasks
- Subtasks appear nested under the parent card
- Each subtask has its own title and completion state

---

## ⏱️ **Pomodoro Timer**

Open with **⏱ Focus** in the header or `Ctrl+P`.

1. **Select a task** from the dropdown to link the session
2. Set **Work duration** (default 25 min) and **Break duration** (default 5 min)
3. Click **▶ Start** — the circular ring counts down the remaining time
4. When the ring completes, TASKY notifies you and starts the break countdown
5. All completed sessions are logged and appear in Analytics

### **Session Types**
- **Work** (purple ring) — focused work interval
- **Break** (green ring) — short rest

---

## 📊 **Analytics Dashboard**

Open with **📊 Analytics** in the header.

### **Charts**
| Chart | Shows |
|-------|-------|
| Tasks Completed (7 days) | Bar chart of completions per day |
| Focus Minutes (7 days) | Bar chart of tracked Pomodoro minutes per day |

### **Insights**
- **Most Productive Hours** — heat map of when you complete the most tasks
- **Daily totals** — how many Pomodoro minutes you logged today

---

## ⚙️ **Settings**

Open with `Ctrl+,` or **Tools → Settings…**.

### **General Tab**
- Minimize to tray on close (on/off)
- Launch on Windows startup (on/off)
- Default sort order for task list

### **Notifications Tab**
- Enable/disable Windows toast notifications
- Enable/disable in-app popup notifications
- Lead time — how many minutes before due date to alert

### **Pomodoro Tab**
- Default work duration (minutes)
- Default short break duration (minutes)
- Default long break duration (minutes)
- Auto-start next session (on/off)

### **Keyboard Tab**
- View all keyboard shortcuts

### **About Tab**
- Version, license, and links

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

### **Types**
| Type | Description |
|------|-------------|
| Windows Toast | Native OS notification via `winotify` |
| In-App Popup | Overlay dialog inside the TASKY window |

### **Behavior**
- Notifications fire when a task is due (lead time configurable in Settings)
- Each task notified only once per due event
- Background monitoring runs even when TASKY is minimized to the system tray

---

## 🖥️ **System Tray**

- Close the main window → TASKY minimizes to the system tray (if enabled in Settings)
- **Double-click** tray icon → restore the window
- **Right-click** tray icon → menu with: Open, Quick Add, Pomodoro, Quit
- Tray tooltip shows live pending/overdue task counts

### **Quick Add**
Right-click the tray icon → **Quick Add Task** to create a task without opening the full window.

---

## 🎨 **Theme System**

| Theme | Description |
|-------|-------------|
| Dark (default) | Deep navy/slate backgrounds, purple accents |
| Light | Soft grey surfaces, same purple/blue accent palette |

- Toggle with `Ctrl+T` or the ☀️🌙 button — takes effect instantly
- Preference is saved and restored on next launch

---

## 💾 **Data Management**

### **Storage**
- **Database**: SQLite file `tasks.db` in the same folder as TASKY
- **Auto-save**: Every change is committed immediately
- **Migration**: Opening v2 with a v1 database automatically adds new columns

### **Backup**
- Copy `tasks.db` to another location for a manual backup

### **Export**
- **File → Export to CSV…** — comma-separated spreadsheet
- **File → Export to JSON…** — structured JSON array

### **Reset**
- Delete `tasks.db` to wipe all tasks and start fresh (irreversible)

---

## 📊 **Stats Bar**

The bottom bar always shows live totals:

| Label | Meaning |
|-------|---------|
| Total | All tasks in the current view |
| Done | Completed tasks |
| Pending | Incomplete tasks |
| Overdue | Tasks past their due date |
| Streak | Consecutive days with at least one completed task |

---

## 🔧 **Troubleshooting**

### **Notifications Not Working**
- Check **Settings → Notifications** to confirm they are enabled
- Ensure Windows Focus Assist is not blocking notifications
- Verify Windows 10/11 notification permissions for TASKY

### **Database Errors**
- Ensure the folder containing `tasks.db` is writable
- Close any other running TASKY instance
- If the database is corrupted, delete `tasks.db` to reset

### **UI Display Issues**
- Try toggling the theme (`Ctrl+T`)
- Check Windows DPI / scaling settings
- Restart TASKY

### **Performance**
- Use the filter bar to reduce the number of visible cards on very large task lists
- Keep TASKY updated for the latest performance improvements

---

## 🚀 **Advanced Tips**

1. **Priority + filter**: Set all today's tasks to High and filter by Today for a focused view
2. **Pomodoro + analytics**: After a week of using the timer, check Analytics to find your peak hours
3. **Tags for context**: Tag tasks with `@work`, `@home`, or project names, then search by tag
4. **Recurring + categories**: Put daily stand-ups in a "Work" category with a daily recurrence
5. **Export for reporting**: Export to CSV weekly and open in a spreadsheet for custom analysis

---

## 📝 **Version History**

| Version | Date | Summary |
|---------|------|---------|
| 2.0.0 | 2026-04-19 | Sidebar, cards, Pomodoro, analytics, categories, priorities, tags, recurrence, tray |
| 1.0.0 | 2024-08-22 | Initial release — table UI, time tracking, notifications, themes |

See [CHANGELOG.md](CHANGELOG.md) for full details.

---

**Made with ❤️ by the TASKY Team**

*TASKY v2.0.0 — Your Personal Task Assistant*
