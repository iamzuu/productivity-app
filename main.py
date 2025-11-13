"""
Productivity Tracker - Simplified working version.
"""
import flet as ft
from core.storage import load_tasks, save_tasks
from core.utils import get_greeting


def main(page: ft.Page):
    """Main app function."""
    page.title = "Productivity Tracker"
    page.window_width = 500
    page.window_height = 900
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#eeeeee"

    # App state
    tasks = load_tasks()
    selected_date = None

    # ===== UI Components =====

    # Greeting
    greeting = ft.Container(
        content=ft.Text(
            get_greeting(),
            size=18,
            weight="bold",
            color="white",
        ),
        padding=20,
        bgcolor="#1a3a3a",
        border_radius=12,
        margin=8,
    )

    # Input field - WHITE BG, BLACK TEXT
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

    date_picker = ft.DatePicker()
    page.overlay.append(date_picker)

    # Task list (will be populated)
    tasks_column = ft.Column(spacing=10)

    # Pomodoro timer
    timer_display = ft.Text(
        "25:00",
        size=56,
        weight="bold",
        color="white",
        text_align="center",
    )

    timer_status = ft.Text(
        "",
        size=14,
        color="yellow",
        text_align="center",
    )

    start_button = ft.ElevatedButton(
        "▶ Start",
        width=120,
        height=45,
        bgcolor="#7c3aed",
        color="white",
    )

    stop_button = ft.ElevatedButton(
        "⏹ Stop",
        width=120,
        height=45,
        bgcolor="red",
        color="white",
    )

    # ===== Event Handlers =====

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

    # Pomodoro timer logic
    from core.pomodoro import PomodoroTimer

    timer = PomodoroTimer()

    def on_timer_tick(time_str):
        timer_display.value = time_str
        page.update()

    def on_timer_complete(session_type):
        timer_status.value = f"✨ {session_type} Complete!"
        page.update()

    timer.on_tick = on_timer_tick
    timer.on_complete = on_timer_complete

    def start_timer(e):
        timer.start()
        start_button.disabled = True
        stop_button.disabled = False
        page.update()

    def stop_timer(e):
        timer.stop()
        timer_display.value = "25:00"
        timer_status.value = ""
        start_button.disabled = False
        stop_button.disabled = True
        page.update()

    start_button.on_click = start_timer
    stop_button.on_click = stop_timer

    # ===== Main Layout =====
    page.add(
        ft.Column(
            [
                # Greeting
                greeting,

                # Input section
                ft.Container(
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
                ),

                # Tasks header
                ft.Container(
                    content=ft.Text("📝 Your Tasks", size=16, weight="bold", color="white"),
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    bgcolor="#1a3a3a",
                    border_radius=8,
                    margin=8,
                ),

                # Task list
                ft.Container(
                    content=tasks_column,
                    padding=ft.padding.symmetric(horizontal=8, vertical=16),
                    bgcolor="white",
                    border_radius=8,
                    margin=8,
                    border=ft.border.all(2, "#cccccc"),
                ),

                # Pomodoro section
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("⏲️ Pomodoro Timer", size=16, weight="bold", color="white"),
                            timer_display,
                            timer_status,
                            ft.Row(
                                [start_button, stop_button],
                                alignment="center",
                                spacing=12,
                            ),
                        ],
                        alignment="center",
                        spacing=16,
                    ),
                    padding=20,
                    bgcolor="#1a3a3a",
                    border_radius=8,
                    margin=8,
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        ),
    )


if __name__ == "__main__":
    ft.app(target=main)

