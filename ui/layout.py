"""Main layout composition for Productivity Tracker."""
import flet as ft
from ui.header import build_header
from ui.tasks import build_task_section
from ui.pomodoro import build_pomodoro_section


def build_page_layout(page: ft.Page):
    """
    Build the main page layout by composing all sections.
    
    Args:
        page: The Flet page instance.
        
    Returns:
        ft.Column: The main layout column with all sections.
    """
    # Build header
    header = build_header()

    # Build task section
    input_container, task_list_container, date_display, task_handlers = build_task_section(page)

    # Build pomodoro section
    pomodoro_container, timer, pomodoro_handlers = build_pomodoro_section(page)

    # Task header
    task_header = ft.Container(
        content=ft.Text("📝 Your Tasks", size=16, weight="bold", color="white"),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor="#1a3a3a",
        border_radius=8,
        margin=8,
    )

    # Main layout
    layout = ft.Column(
        [
            header,
            input_container,
            task_header,
            task_list_container,
            pomodoro_container,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    return layout
