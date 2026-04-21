import json
import logging
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal

from database import DatabaseManager
from models import Task, Category
from ui.theme_manager import ThemeManager

logger = logging.getLogger(__name__)


def _ok(payload) -> str:
    return json.dumps({"ok": True, "data": payload})


def _err(message: str) -> str:
    logger.warning("Bridge error: %s", message)
    return json.dumps({"ok": False, "error": message})


class TaskyBridge(QObject):
    """Bridge class to expose Python database methods to JavaScript."""

    dataChanged = pyqtSignal()

    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.theme_manager = ThemeManager.instance()

    def _task_to_dict(self, task: Task):
        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "projectId": str(task.category_id) if task.category_id else None,
            "tags": [t.strip() for t in task.tags.split(",")] if task.tags else [],
            "dueDate": task.due_date.isoformat() if task.due_date else None,
            "createdAt": task.created_at.isoformat() if task.created_at else None,
            "completedAt": task.completed_at.isoformat() if task.completed_at else None,
            "parentId": str(task.parent_task_id) if task.parent_task_id else None,
            "focusMinutes": task.time_spent,
            "priority": task.priority,
            "notes": task.notes,
            "isRecurring": task.is_recurring,
            "recurrenceRule": task.recurrence_rule,
        }

    def _session_to_dict(self, s):
        return {
            "id": str(s.id),
            "taskId": str(s.task_id),
            "startedAt": s.started_at.isoformat() if s.started_at else None,
            "endedAt": s.ended_at.isoformat() if s.ended_at else None,
            "durationMinutes": s.duration_minutes,
            "sessionType": s.session_type,
            "completed": s.completed,
        }

    def _project_to_dict(self, cat: Category):
        return {
            "id": str(cat.id),
            "name": cat.name,
            "color": cat.color,
            "isArchived": cat.is_archived,
        }

    @pyqtSlot(result=str)
    def getData(self):
        try:
            tasks = self.db_manager.get_all_tasks()
            all_tasks = []
            for t in tasks:
                all_tasks.append(self._task_to_dict(t))
                for st in self.db_manager.get_subtasks(t.id):
                    all_tasks.append(self._task_to_dict(st))

            categories = self.db_manager.get_categories()
            return _ok({
                "tasks": all_tasks,
                "projects": [self._project_to_dict(c) for c in categories],
                "focusSessions": [self._session_to_dict(s) for s in self.db_manager.get_recent_focus_sessions()],
                "theme": self.theme_manager.current_theme,
            })
        except Exception as e:
            logger.exception("getData failed")
            return _err(str(e))

    @pyqtSlot(str, result=str)
    def addTask(self, task_json: str):
        try:
            data = json.loads(task_json)
        except json.JSONDecodeError as e:
            return _err(f"Invalid JSON: {e}")
        try:
            title = data.get("title", "").strip()
            if not title:
                return _err("title is required")
            pid = data.get("projectId")
            task = Task(
                id=None,
                title=title,
                description=data.get("description", ""),
                due_date=datetime.fromisoformat(data["dueDate"]) if data.get("dueDate") else datetime.now(),
                completed=bool(data.get("completed", False)),
                category_id=int(pid) if pid not in (None, "", "0") else None,
                tags=",".join(data.get("tags", [])),
                parent_task_id=int(data["parentId"]) if data.get("parentId") else None,
                priority=int(data.get("priority", 2)),  # Default to MEDIUM
                notes=data.get("notes", ""),
                is_recurring=bool(data.get("isRecurring", False)),
                recurrence_rule=data.get("recurrenceRule"),
            )
            new_id = self.db_manager.add_task(task)
            self.dataChanged.emit()
            return _ok(str(new_id))
        except Exception as e:
            logger.exception("addTask failed")
            return _err(str(e))

    @pyqtSlot(str, str, result=str)
    def updateTask(self, task_id: str, updates_json: str):
        try:
            tid = int(task_id)
        except (ValueError, TypeError):
            return _err(f"Invalid task_id: {task_id!r}")
        try:
            updates = json.loads(updates_json)
        except json.JSONDecodeError as e:
            return _err(f"Invalid JSON: {e}")
        try:
            task = self.db_manager.get_task_by_id(tid)
            if not task:
                return _err(f"Task {tid} not found")
            if "title" in updates:
                task.title = updates["title"]
            if "description" in updates:
                task.description = updates["description"]
            if "completed" in updates:
                task.completed = bool(updates["completed"])
                task.completed_at = datetime.now() if task.completed else None
            if "projectId" in updates:
                pid = updates["projectId"]
                task.category_id = int(pid) if pid not in (None, "", "0") else None
            if "tags" in updates:
                task.tags = ",".join(updates["tags"])
            if "focusMinutes" in updates:
                task.time_spent = int(updates["focusMinutes"])
            if "priority" in updates:
                task.priority = int(updates["priority"])
            if "notes" in updates:
                task.notes = updates["notes"]
            if "isRecurring" in updates:
                task.is_recurring = bool(updates["isRecurring"])
            if "recurrenceRule" in updates:
                task.recurrence_rule = updates["recurrenceRule"]
            self.db_manager.update_task(task)
            self.dataChanged.emit()
            return _ok(None)
        except Exception as e:
            logger.exception("updateTask failed")
            return _err(str(e))

    @pyqtSlot(str, result=str)
    def deleteTask(self, task_id: str):
        try:
            self.db_manager.delete_task(int(task_id))
            self.dataChanged.emit()
            return _ok(None)
        except Exception as e:
            logger.exception("deleteTask failed")
            return _err(str(e))

    @pyqtSlot(str, result=str)
    def toggleTask(self, task_id: str):
        try:
            tid = int(task_id)
            task = self.db_manager.get_task_by_id(tid)
            if not task:
                return _err(f"Task {tid} not found")
            task.completed = not task.completed
            task.completed_at = datetime.now() if task.completed else None
            self.db_manager.update_task(task)
            self.dataChanged.emit()
            return _ok(None)
        except Exception as e:
            logger.exception("toggleTask failed")
            return _err(str(e))

    @pyqtSlot(str, result=str)
    def addProject(self, project_json: str):
        try:
            data = json.loads(project_json)
        except json.JSONDecodeError as e:
            return _err(f"Invalid JSON: {e}")
        try:
            name = data.get("name", "").strip()
            if not name:
                return _err("name is required")
            cat = Category(
                id=None,
                name=name,
                color=data.get("color", "#8b5cf6"),
                icon="📁",
            )
            self.db_manager.add_category(cat)
            self.dataChanged.emit()
            return _ok(None)
        except Exception as e:
            logger.exception("addProject failed")
            return _err(str(e))

    @pyqtSlot(str, result=str)
    def deleteProject(self, project_id: str):
        try:
            self.db_manager.delete_category(int(project_id))
            self.dataChanged.emit()
            return _ok(None)
        except Exception as e:
            logger.exception("deleteProject failed")
            return _err(str(e))

    @pyqtSlot(str, str, result=str)
    def updateProject(self, project_id: str, updates_json: str):
        try:
            pid = int(project_id)
            updates = json.loads(updates_json)
            cat = self.db_manager.get_category_by_id(pid)
            if not cat:
                return _err(f"Project {pid} not found")
            if "name" in updates:
                cat.name = updates["name"]
            if "color" in updates:
                cat.color = updates["color"]
            if "isArchived" in updates:
                cat.is_archived = bool(updates["isArchived"])
            self.db_manager.update_category(cat)
            self.dataChanged.emit()
            return _ok(None)
        except Exception as e:
            logger.exception("updateProject failed")
            return _err(str(e))

    @pyqtSlot(result=str)
    def toggleTheme(self):
        try:
            self.theme_manager.toggle_theme()
            self.dataChanged.emit()
            return _ok(None)
        except Exception as e:
            logger.exception("toggleTheme failed")
            return _err(str(e))

    # ── API key management (OS keychain) ─────────────────────────────────────

    @pyqtSlot(str, result=str)
    def saveApiKey(self, key: str):
        """Store the Anthropic API key in the OS keychain and activate it immediately."""
        try:
            from key_storage import save_key
            key = key.strip()
            if not key:
                return _err("API key cannot be empty")
            if not key.startswith("sk-ant-"):
                return _err("That doesn't look like a valid Anthropic API key (should start with sk-ant-)")
            save_key(key)
            import os
            os.environ["ANTHROPIC_API_KEY"] = key
            return _ok({"configured": True})
        except Exception as e:
            logger.exception("saveApiKey failed")
            return _err(str(e))

    @pyqtSlot(result=str)
    def getApiKeyStatus(self):
        """Return whether an API key is configured. Never returns the key itself."""
        try:
            from key_storage import key_is_configured
            return _ok({"configured": key_is_configured()})
        except Exception as e:
            logger.exception("getApiKeyStatus failed")
            return _err(str(e))

    @pyqtSlot(result=str)
    def clearApiKey(self):
        """Remove the API key from the OS keychain and environment."""
        try:
            from key_storage import delete_key
            import os
            delete_key()
            os.environ.pop("ANTHROPIC_API_KEY", None)
            return _ok({"configured": False})
        except Exception as e:
            logger.exception("clearApiKey failed")
            return _err(str(e))

    # ── Streak ────────────────────────────────────────────────────────────────

    @pyqtSlot(result=str)
    def getStreak(self):
        try:
            data = self.db_manager.get_analytics_data(days=1)
            return _ok({"streak": data["streak"]})
        except Exception as e:
            logger.exception("getStreak failed")
            return _err(str(e))

    # ── AI features ───────────────────────────────────────────────────────────

    @pyqtSlot(result=str)
    def isAIAvailable(self):
        import os
        return _ok({"available": bool(os.environ.get("ANTHROPIC_API_KEY"))})

    @pyqtSlot(str, result=str)
    def aiBreakdown(self, task_json: str):
        try:
            data = json.loads(task_json)
        except json.JSONDecodeError as e:
            return _err(f"Invalid JSON: {e}")
        try:
            from ai_service import AIService
            ai = AIService()
            if not ai.is_available():
                return _err("ANTHROPIC_API_KEY not set. Add it to your environment to enable AI features.")
            subtasks = ai.breakdown_task(
                title=data.get("title", ""),
                description=data.get("description", ""),
            )
            return _ok({"subtasks": subtasks})
        except Exception as e:
            logger.exception("aiBreakdown failed")
            return _err(str(e))

    @pyqtSlot(str, result=str)
    def aiCapture(self, text: str):
        try:
            from ai_service import AIService
            ai = AIService()
            if not ai.is_available():
                return _err("ANTHROPIC_API_KEY not set.")
            tasks = ai.capture_tasks_from_text(text)
            return _ok({"tasks": tasks})
        except Exception as e:
            logger.exception("aiCapture failed")
            return _err(str(e))

    @pyqtSlot(result=str)
    def aiDigest(self):
        try:
            from ai_service import AIService
            ai = AIService()
            stats = self.db_manager.get_analytics_data(days=7)
            digest = ai.generate_weekly_digest(stats)
            return _ok({"digest": digest, "stats": stats})
        except Exception as e:
            logger.exception("aiDigest failed")
            return _err(str(e))

    # ── Analytics ─────────────────────────────────────────────────────────────

    @pyqtSlot(result=str)
    def getAnalytics(self):
        try:
            data = self.db_manager.get_analytics_data()
            return _ok(data)
        except Exception as e:
            logger.exception("getAnalytics failed")
            return _err(str(e))
