<!-- Copilot / AI agent guidance for this repository -->
# Productivity Tracker - AI Agent Instructions

## Project Overview
A modern, aesthetic productivity application built with Flet for managing university tasks and focus time. The app features task management with deadlines, an elegant UI inspired by Notion/Todoist, and an integrated Pomodoro timer.

## Quick Start

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the app:**
```bash
python main.py
```

## Project Structure

```
productivity_app/
├── main.py                 # App entry point, main UI orchestration
├── requirements.txt        # Python dependencies (flet)
├── data/
│   └── tasks.json         # Task storage (auto-created)
├── core/
│   ├── __init__.py
│   ├── storage.py         # Task load/save operations
│   ├── pomodoro.py        # PomodoroTimer class with callbacks
│   └── utils.py           # Date formatting, greeting, helper functions
└── ui/
    ├── __init__.py
    ├── task_list.py       # Task card components & task list builder
    └── pomodoro_ui.py     # Pomodoro timer UI section builder
```

## Architecture & Key Patterns

### Data Layer (`core/storage.py`)
- All task I/O goes through `load_tasks()`, `save_tasks()`, and helper functions (`add_task`, `update_task`, `delete_task`, `toggle_task`).
- Tasks stored in `data/tasks.json` with structure: `{"title": str, "done": bool, "date": "YYYY-MM-DD" | null}`.
- Functions ensure `data/` dir exists and handle JSON errors gracefully.

### Pomodoro Timer (`core/pomodoro.py`)
- `PomodoroTimer` class with configurable work/break duration (default 25/5 min).
- Runs in background thread via `start()`. Callbacks: `on_tick(time_str)` and `on_complete(session_type)`.
- Methods: `start()`, `stop()`, `pause()`, `resume()`, `_format_time()`, `_run()`.
- Thread-safe; UI updates happen via callbacks.

### UI Layer (`ui/task_list.py`, `ui/pomodoro_ui.py`)
- `build_task_card()`: Renders individual task with checkbox, title, date, delete button, hover effects, and click handler.
- `build_task_list()`: Assembles all task cards into a Column.
- `build_pomodoro_section()`: Returns (Container, PomodoroTimer). Handles timer display, start/stop buttons, completion alert.
- Cards use soft shadows, rounded corners, pastel colors (white bg, purple accent #7c3aed, error red #ef5350, blue #42a5f5).

### Main App (`main.py`)
- Greeting section with time-aware message ("Good morning/afternoon/evening").
- Input section: TextField for task title + Add button + DatePicker for deadline.
- Task list section: built dynamically from tasks using `build_task_list()`.
- Click task to show dialog with date and status.
- Pomodoro section at bottom.
- All mutations call storage functions and refresh UI.

## UI/UX Design Notes

**Color Palette:**
- Primary accent: `#7c3aed` (purple for buttons, active elements)
- Backgrounds: `#ffffff` (cards), `#f9f9f9` (inputs), `#f5f3ff` (Pomodoro section)
- Text: `#333` (main), `#999` (secondary/disabled)
- Status colors: `#ef5350` (overdue/error), `#42a5f5` (today/info), `#ab47bc` (future dates)

**Styling elements:**
- Cards: white bg, 8px border radius, soft box shadow (spread=0, blur=4, y=2).
- Hover: shadow increases (blur=8, y=4), bg shifts slightly (`#f9f9f9`).
- Buttons: 8px border radius, ElevatedButton for primary (purple), OutlinedButton for secondary.
- Text hierarchy: greeting (18px w500), section headers (18px w600), task title (16px w500), details (12-14px).

## Common Tasks

**Adding a new task field:**
1. Update task structure in comments and test data.
2. Modify `core/storage.py` to handle the new field in `load_tasks()` (ensure backward compat).
3. Update `add_task()` to accept the new parameter.
4. Update `ui/task_list.py` to display it in `build_task_card()`.
5. Update `main.py` input section and dialog to capture/show the field.

**Modifying Pomodoro duration:**
- In `main.py`, pass custom durations to `build_pomodoro_section()` via kwargs, or edit default in `core/pomodoro.py` constructor.

**Changing colors or styling:**
- All color strings and BoxShadow definitions are in UI files (`ui/task_list.py`, `ui/pomodoro_ui.py`, `main.py`).
- Container padding, borders, border_radius are inline — use Flet's `ft.padding`, `ft.border`, `ft.BorderSide` for consistency.

## Event Handling & Callbacks

- Task checkbox: `on_change=lambda e, i=i: on_toggle(...)` — preserves index binding with `i=i`.
- Task delete: IconButton with on_click.
- Task card click: GestureDetector on date text, triggers dialog.
- Add task: TextField `on_submit` or Button `on_click`.
- Date picker: `on_change` updates `selected_date` state variable.
- Pomodoro timer: background thread calls `on_tick` and `on_complete` callbacks.

## Development Workflow

1. **Edit code**: Modify any file in `core/` or `ui/` directly; import in `main.py`.
2. **Test**: Run `python main.py`. UI loads immediately; use the app interactively.
3. **Debug**: Add print statements in callback functions or storage operations.
4. **Refactor**: Keep imports relative (e.g., `from core.storage import ...`); avoid circular dependencies.

## Testing & Validation

- No automated tests currently; validate by running the app and interacting with UI.
- Create sample tasks in `data/tasks.json` manually to test load behavior.
- Check console for any uncaught exceptions in background threads (Pomodoro timer).

## Future Enhancements

- Add task categories/tags.
- Implement task filtering by date or status.
- Add data export (CSV, JSON download).
- Dark mode toggle.
- Task statistics dashboard.
- Recurring tasks.
- Integration with calendar APIs.

## Notes for AI Agents

- All file paths are absolute; data dir is `data/` relative to repo root.
- JSON serialization uses `ensure_ascii=False` to support Unicode task titles.
- `PomodoroTimer` updates UI via callbacks to avoid thread-safety issues.
- Flet's `DatePicker` is modal; selected date accessed via `date_picker_ref.value`.
- Icon names in Flet use `ft.Icons.ICON_NAME` (not lowercase).
- Container `visible` property controls section visibility without removing from layout.
