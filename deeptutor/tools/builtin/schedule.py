"""Schedule and Classwork management tools."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from loguru import logger
from deeptutor.core.tool_protocol import BaseTool, ToolDefinition, ToolParameter, ToolResult

DB_PATH = Path("schedule.json")


def _load_db() -> dict[str, Any]:
    if not DB_PATH.exists():
        return {"schedules": [], "classworks": []}
    try:
        return json.loads(DB_PATH.read_text("utf-8"))
    except json.JSONDecodeError:
        return {"schedules": [], "classworks": []}


def _save_db(data: dict[str, Any]) -> None:
    DB_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), "utf-8")


class ScheduleTool(BaseTool):
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="manage_schedule",
            description="View or update class schedules. Action can be 'view', 'add', or 'delete'.",
            parameters=[
                ToolParameter(name="action", type="string", description="One of: 'view', 'add', 'delete'"),
                ToolParameter(
                    name="class_name", 
                    type="string", 
                    description="Name of the class", 
                    required=False
                ),
                ToolParameter(
                    name="time", 
                    type="string", 
                    description="Time of the class (e.g., '10:00 AM')", 
                    required=False
                ),
                ToolParameter(
                    name="day", 
                    type="string", 
                    description="Day of the week", 
                    required=False
                )
            ],
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        action = kwargs.get("action", "view")
        db = _load_db()
        schedules = db.get("schedules", [])

        if action == "view":
            if not schedules:
                return ToolResult(content="No schedules found.")
            formatted = "\n".join([f"- {s['class_name']} on {s['day']} at {s['time']}" for s in schedules])
            return ToolResult(content=f"Current Schedules:\n{formatted}")

        elif action == "add":
            class_name = kwargs.get("class_name")
            time = kwargs.get("time")
            day = kwargs.get("day")
            if not all([class_name, time, day]):
                return ToolResult(content="Missing required parameters: class_name, time, or day", success=False)
            
            schedules.append({"class_name": class_name, "time": time, "day": day})
            db["schedules"] = schedules
            _save_db(db)
            return ToolResult(content=f"Successfully added {class_name} on {day} at {time}.")

        elif action == "delete":
            class_name = kwargs.get("class_name")
            if not class_name:
                return ToolResult(content="Missing required parameter: class_name", success=False)
            
            filtered = [s for s in schedules if s['class_name'] != class_name]
            if len(filtered) == len(schedules):
                return ToolResult(content=f"Class {class_name} not found.", success=False)
            
            db["schedules"] = filtered
            _save_db(db)
            return ToolResult(content=f"Successfully deleted {class_name}.")

        return ToolResult(content="Invalid action. Use 'view', 'add', or 'delete'.", success=False)


class ClassworkTool(BaseTool):
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="manage_classwork",
            description="View or update classwork/assignments. Action can be 'view', 'add', or 'delete'.",
            parameters=[
                ToolParameter(name="action", type="string", description="One of: 'view', 'add', 'delete'"),
                ToolParameter(
                    name="class_name", 
                    type="string", 
                    description="Name of the class", 
                    required=False
                ),
                ToolParameter(
                    name="assignment", 
                    type="string", 
                    description="Description of the assignment", 
                    required=False
                ),
                ToolParameter(
                    name="due_date", 
                    type="string", 
                    description="Due date for the assignment", 
                    required=False
                )
            ],
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        action = kwargs.get("action", "view")
        db = _load_db()
        classworks = db.get("classworks", [])

        if action == "view":
            if not classworks:
                return ToolResult(content="No classworks found.")
            formatted = "\n".join([f"- {cw['class_name']}: {cw['assignment']} (Due: {cw['due_date']})" for cw in classworks])
            return ToolResult(content=f"Current Classworks:\n{formatted}")

        elif action == "add":
            class_name = kwargs.get("class_name")
            assignment = kwargs.get("assignment")
            due_date = kwargs.get("due_date")
            if not all([class_name, assignment, due_date]):
                return ToolResult(content="Missing required parameters: class_name, assignment, or due_date", success=False)
            
            classworks.append({"class_name": class_name, "assignment": assignment, "due_date": due_date})
            db["classworks"] = classworks
            _save_db(db)
            return ToolResult(content=f"Successfully added assignment for {class_name}.")

        elif action == "delete":
            class_name = kwargs.get("class_name")
            if not class_name:
                return ToolResult(content="Missing required parameter: class_name", success=False)
            
            filtered = [cw for cw in classworks if cw['class_name'] != class_name]
            if len(filtered) == len(classworks):
                return ToolResult(content=f"Classwork for {class_name} not found.", success=False)
            
            db["classworks"] = filtered
            _save_db(db)
            return ToolResult(content=f"Successfully deleted classwork for {class_name}.")

        return ToolResult(content="Invalid action. Use 'view', 'add', or 'delete'.", success=False)
