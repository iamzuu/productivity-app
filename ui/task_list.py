"""
Task list UI component: displays tasks in elegant cards with date info.
"""
import flet as ft
from typing import Callable, List, Dict, Any
from core.utils import format_date, is_overdue, is_today


def build_task_card(
    task: Dict[str, Any],
    index: int,
    on_toggle: Callable[[int, bool], None],
    on_delete: Callable[[int], None],
    on_click: Callable[[int], None],
) -> ft.Container:
    """
    Build a single task card with modern styling.
    
    Args:
        task: task object
        index: task index in list
        on_toggle: callback when checkbox toggled
        on_delete: callback when delete button clicked
        on_click: callback when task card clicked (for dialog)
    
    Returns:
        A styled Container representing the task card
    """
    title = task.get("title", "Untitled")
    done = task.get("done", False)
    date = task.get("date")

    # Determine date display and color
    date_text = format_date(date)
    if date:
        if is_overdue(date):
            date_color = "#ef5350"  # red for overdue
            date_label = f"📌 {date_text} (Overdue)"
        elif is_today(date):
            date_color = "#42a5f5"  # blue for today
            date_label = f"📅 {date_text} (Today)"
        else:
            date_color = "#ab47bc"  # purple for future
            date_label = f"📅 {date_text}"
    else:
        date_color = "#999"
        date_label = "No date"

    # Task title with strikethrough if done
    title_style = ft.TextStyle(
        decoration="line_through" if done else "none",
        color="#999" if done else "#333",
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Checkbox(
                            value=done,
                            on_change=lambda e, i=index: on_toggle(i, e.control.value),
                            fill_color="#7c3aed" if not done else "#a78bfa",
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    title,
                                    size=16,
                                    weight="w500",
                                    style=title_style,
                                    no_wrap=False,
                                    expand=True,
                                ),
                                ft.GestureDetector(
                                    content=ft.Text(
                                        date_label,
                                        size=12,
                                        color=date_color,
                                        weight="w400",
                                    ),
                                    on_tap=lambda e, i=index: on_click(i),
                                ),
                            ],
                            expand=True,
                            spacing=4,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color="#ef5350",
                            icon_size=18,
                            on_click=lambda e, i=index: on_delete(i),
                        ),
                    ],
                    alignment="spaceBetween",
                    vertical_alignment="center",
                    spacing=10,
                ),
            ],
            spacing=0,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor="#ffffff",
        border_radius=8,
        border=ft.border.all(1, "#e0e0e0") if not done else ft.border.all(1, "#f0f0f0"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color="#0000000d",
            offset=ft.Offset(0, 2),
        ),
        on_hover=lambda e: _on_card_hover(e),
    )


def _on_card_hover(e):
    """Handle card hover effect."""
    if e.data == "true":
        e.control.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color="#0000001a",
            offset=ft.Offset(0, 4),
        )
        e.control.bgcolor = "#f9f9f9"
    else:
        e.control.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color="#0000000d",
            offset=ft.Offset(0, 2),
        )
        e.control.bgcolor = "#ffffff"
    e.control.update()


def build_task_list(
    tasks: List[Dict[str, Any]],
    on_toggle: Callable[[int, bool], None],
    on_delete: Callable[[int], None],
    on_click: Callable[[int], None],
) -> ft.Column:
    """
    Build the task list column with all task cards.
    
    Args:
        tasks: list of task objects
        on_toggle: callback when task checkbox toggled
        on_delete: callback when delete button clicked
        on_click: callback when task clicked
    
    Returns:
        A Column containing all task cards
    """
    task_cards = []
    for i, task in enumerate(tasks):
        card = build_task_card(task, i, on_toggle, on_delete, on_click)
        task_cards.append(card)

    return ft.Column(
        controls=task_cards,
        spacing=10,
    )
