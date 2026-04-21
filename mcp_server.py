#!/usr/bin/env python3
"""
TASKY MCP Server — exposes your task database to Claude Desktop.

Setup (add to Claude Desktop's claude_desktop_config.json):
{
  "mcpServers": {
    "tasky": {
      "command": "python",
      "args": ["/absolute/path/to/TASKS/mcp_server.py"]
    }
  }
}

Then in Claude Desktop you can say:
  "What are my overdue tasks?"
  "Create a task: Deploy new feature, due Friday, high priority"
  "Mark task 12 as complete"
  "How productive was I this week?"
"""
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from database import DatabaseManager
from models import Task

db = DatabaseManager()
server = Server("tasky")


def _task_dict(t) -> dict:
    return {
        "id": t.id,
        "title": t.title,
        "priority": t.priority,
        "priority_label": {1: "High", 2: "Medium", 3: "Low", 4: "None"}.get(t.priority, "?"),
        "completed": t.completed,
        "due_date": t.due_date.isoformat() if t.due_date else None,
        "project_id": t.category_id,
        "tags": t.tags,
        "notes": (t.notes or "")[:200],
        "time_spent_minutes": t.time_spent,
    }


@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="get_tasks",
            description="List tasks filtered by status or time window",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "enum": ["all", "today", "overdue", "week", "completed"],
                        "default": "all",
                        "description": "Which tasks to return",
                    },
                },
            },
        ),
        types.Tool(
            name="create_task",
            description="Create a new task in TASKY",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title (required)"},
                    "priority": {
                        "type": "integer",
                        "enum": [1, 2, 3, 4],
                        "description": "1=High 2=Medium 3=Low 4=None",
                        "default": 2,
                    },
                    "due_date": {
                        "type": "string",
                        "description": "ISO date string e.g. 2026-04-25. Omit for no due date.",
                    },
                    "notes": {"type": "string", "description": "Optional notes"},
                    "project_id": {"type": "integer", "description": "Category/project ID"},
                },
                "required": ["title"],
            },
        ),
        types.Tool(
            name="complete_task",
            description="Mark a task complete or reopen it",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                    "completed": {"type": "boolean", "default": True},
                },
                "required": ["task_id"],
            },
        ),
        types.Tool(
            name="update_task",
            description="Update any fields on an existing task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "priority": {"type": "integer", "enum": [1, 2, 3, 4]},
                    "due_date": {"type": "string"},
                    "notes": {"type": "string"},
                    "project_id": {"type": "integer"},
                },
                "required": ["task_id"],
            },
        ),
        types.Tool(
            name="delete_task",
            description="Permanently delete a task",
            inputSchema={
                "type": "object",
                "properties": {"task_id": {"type": "integer"}},
                "required": ["task_id"],
            },
        ),
        types.Tool(
            name="list_projects",
            description="List all projects/categories with task counts",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_analytics",
            description="Get productivity analytics: streak, completion rate, focus time",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "default": 7,
                        "description": "Days of history to analyze (max 30)",
                    }
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "get_tasks":
            f = arguments.get("filter", "all")
            if f == "today":
                tasks = db.get_tasks_due_today()
            elif f == "overdue":
                tasks = db.get_overdue_tasks()
            elif f == "week":
                tasks = db.get_tasks_due_this_week()
            elif f == "completed":
                tasks = db.get_tasks_by_filter(completed=True)
            else:
                tasks = db.get_all_tasks()
            result = [_task_dict(t) for t in tasks]
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "create_task":
            due_raw = arguments.get("due_date")
            due_dt = datetime.fromisoformat(due_raw) if due_raw else datetime.now()
            task = Task(
                id=None,
                title=arguments["title"],
                description="",
                due_date=due_dt,
                completed=False,
                priority=arguments.get("priority", 2),
                category_id=arguments.get("project_id"),
                notes=arguments.get("notes", ""),
            )
            task_id = db.add_task(task)
            msg = f"Created task #{task_id}: '{arguments['title']}'"
            return [types.TextContent(type="text", text=msg)]

        elif name == "complete_task":
            task_id = int(arguments["task_id"])
            completed = bool(arguments.get("completed", True))
            db.mark_task_completed(task_id, completed)
            status = "completed" if completed else "reopened"
            return [types.TextContent(type="text", text=f"Task #{task_id} {status}.")]

        elif name == "update_task":
            task_id = int(arguments["task_id"])
            task = db.get_task_by_id(task_id)
            if not task:
                return [types.TextContent(type="text", text=f"Task #{task_id} not found.")]
            if "title" in arguments:
                task.title = arguments["title"]
            if "priority" in arguments:
                task.priority = int(arguments["priority"])
            if "due_date" in arguments:
                task.due_date = datetime.fromisoformat(arguments["due_date"])
            if "notes" in arguments:
                task.notes = arguments["notes"]
            if "project_id" in arguments:
                task.category_id = arguments["project_id"]
            db.update_task(task)
            return [types.TextContent(type="text", text=f"Task #{task_id} updated.")]

        elif name == "delete_task":
            task_id = int(arguments["task_id"])
            db.delete_task(task_id)
            return [types.TextContent(type="text", text=f"Task #{task_id} deleted.")]

        elif name == "list_projects":
            projects = db.get_categories()
            counts = db.get_task_count_by_category()
            result = [
                {
                    "id": p.id,
                    "name": p.name,
                    "color": p.color,
                    "archived": p.is_archived,
                    "active_tasks": counts.get(p.id, 0),
                }
                for p in projects
            ]
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_analytics":
            days = min(int(arguments.get("days", 7)), 30)
            data = db.get_analytics_data(days=days)
            return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
