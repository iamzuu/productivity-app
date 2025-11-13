"""Task management UI section for Productivity Tracker."""
import flet as ft
from core.storage import load_tasks, save_tasks


def build_task_section(page: ft.Page):
    """
    Build the task input and task list section.
    
    Args:
        page: The Flet page instance.
        
    Returns:
        tuple: (input_container, task_list_container, task_input, date_display, 
                date_picker, tasks_column, handler_dict)
        where handler_dict contains: add_task, toggle_task, delete_task, 
                                     on_date_selected, open_date_picker, build_task_ui
    """
    # Load tasks
    tasks = load_tasks()
    selected_date = None

    # Input field
    task_input = ft.TextField(
        label="What's your next task?",
        text_style=ft.TextStyle(size=14, color="black"),
        label_style=ft.TextStyle(color="gray", size=13),
        filled=True,
        fill_color="white",
        border_color="#cccccc",
        focused_border_color="#7c3aed",
        color="black",
        min_lines=1,
        max_lines=3,
        expand=True,
    )

    add_button = ft.ElevatedButton(
        text="Add Task",
        width=100,
        height=50,
        bgcolor="#7c3aed",
        color="white",
    )

    # Date display
    date_display = ft.Text(
        "📅 No date",
        size=12,
        color="black",
    )

    # Date picker
    date_picker = ft.DatePicker()
    page.overlay.append(date_picker)

    # Task list column
    tasks_column = ft.Column(spacing=10)

    # Event handlers
    def build_task_ui():
        """Rebuild the task list UI."""
        tasks_column.controls.clear()
        for i, task in enumerate(tasks):
            date_text = task.get('date', 'No date')
            title_text = task.get("title", "Untitled")
            is_done = task.get("done", False)

            # Task card
            task_row = ft.Row(
                [
                    ft.Checkbox(
                        value=is_done,
                        on_change=lambda e, idx=i: toggle_task(idx),
                        fill_color="#7c3aed",
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                title_text,
                                size=14,
                                color="gray" if is_done else "black",
                                weight="bold",
                            ),
                            ft.Text(
                                f"📅 {date_text}",
                                size=12,
                                color="darkred",
                                weight="w500",
                            ),
                        ],
                        expand=True,
                        spacing=4,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color="red",
                        on_click=lambda e, idx=i: delete_task(idx),
                    ),
                ],
                alignment="spaceBetween",
            )

            tasks_column.controls.append(
                ft.Container(
                    content=task_row,
                    padding=12,
                    bgcolor="white",
                    border_radius=8,
                    border=ft.border.all(1, "#cccccc"),
                )
            )

    def add_task(e):
        """Add new task."""
        nonlocal selected_date
        title = task_input.value.strip()
        if not title:
            return

        tasks.append({
            "title": title,
            "done": False,
            "date": selected_date,
        })
        save_tasks(tasks)
        task_input.value = ""
        task_input.focus()
        selected_date = None
        date_display.value = "📅 No date"
        date_picker.value = None
        build_task_ui()
        page.update()

    def toggle_task(index):
        """Toggle task done status."""
        if 0 <= index < len(tasks):
            tasks[index]["done"] = not tasks[index]["done"]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def delete_task(index):
        """Delete a task."""
        if 0 <= index < len(tasks):
            del tasks[index]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def on_date_selected(e):
        """Handle date picker change."""
        nonlocal selected_date
        if date_picker.value:
            selected_date = str(date_picker.value).split()[0]
            date_display.value = f"📅 {selected_date}"
        else:
            selected_date = None
            date_display.value = "📅 No date"
        page.update()

    def open_date_picker(e):
        """Open date picker."""
        page.open(date_picker)

    # Wire up event handlers
    add_button.on_click = add_task
    date_picker.on_change = on_date_selected
    task_input.on_submit = add_task

    # Initial task list
    build_task_ui()

    # Input container
    input_container = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [task_input, add_button],
                    spacing=10,
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.CALENDAR_TODAY,
                            icon_color="#7c3aed",
                            on_click=open_date_picker,
                        ),
                        date_display,
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        ),
        padding=16,
        bgcolor="white",
        border_radius=8,
        margin=8,
        border=ft.border.all(2, "#cccccc"),
    )

    # Task list container
    task_list_container = ft.Container(
        content=tasks_column,
        padding=ft.padding.symmetric(horizontal=8, vertical=16),
        bgcolor="white",
        border_radius=8,
        margin=8,
        border=ft.border.all(2, "#cccccc"),
    )

    # Return components and handlers
    handler_dict = {
        "add_task": add_task,
        "toggle_task": toggle_task,
        "delete_task": delete_task,
        "on_date_selected": on_date_selected,
        "open_date_picker": open_date_picker,
        "build_task_ui": build_task_ui,
        "tasks": tasks,
    }

    return input_container, task_list_container, date_display, handler_dict
