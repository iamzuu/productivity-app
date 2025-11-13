"""
Task storage module: handles loading and saving tasks to tasks.json.
"""
import json
import os
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")


def ensure_data_dir():
    """Create the data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from tasks.json. Return empty list if file doesn't exist."""
    ensure_data_dir()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
            # Ensure all tasks have required fields (backward compatibility)
            for item in items:
                if "title" not in item:
                    item["title"] = "Untitled"
                if "done" not in item:
                    item["done"] = False
                if "deadline" not in item:
                    item["deadline"] = None
                if "mata_kuliah" not in item:
                    item["mata_kuliah"] = ""
                if "deskripsi" not in item:
                    item["deskripsi"] = ""
            return items
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Save tasks to tasks.json."""
    ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(tasks: List[Dict[str, Any]], title: str, mata_kuliah: str = "", deadline: str = None, deskripsi: str = "") -> Dict[str, Any]:
    """Add a new task with all parameters and return the created task object."""
    task = {
        "title": title.strip(),
        "done": False,
        "deadline": deadline,
        "mata_kuliah": mata_kuliah.strip(),
        "deskripsi": deskripsi.strip(),
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def update_task(tasks: List[Dict[str, Any]], index: int, **kwargs) -> None:
    """Update a task at the given index with provided kwargs."""
    if 0 <= index < len(tasks):
        tasks[index].update(kwargs)
        save_tasks(tasks)


def delete_task(tasks: List[Dict[str, Any]], index: int) -> None:
    """Delete a task at the given index."""
    if 0 <= index < len(tasks):
        del tasks[index]
        save_tasks(tasks)


def toggle_task(tasks: List[Dict[str, Any]], index: int) -> None:
    """Toggle the 'done' status of a task."""
    if 0 <= index < len(tasks):
        tasks[index]["done"] = not tasks[index]["done"]
        save_tasks(tasks)
