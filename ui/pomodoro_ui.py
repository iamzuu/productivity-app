"""
Pomodoro Timer UI component: displays timer and controls with elegant styling.
"""
import flet as ft
from typing import Callable, Optional
from core.pomodoro import PomodoroTimer


def build_pomodoro_section(
    on_timer_callback: Callable[[str], None],
    on_complete_callback: Optional[Callable[[str], None]] = None,
) -> tuple[ft.Container, PomodoroTimer]:
    """
    Build the Pomodoro timer section with modern design.
    
    Args:
        on_timer_callback: callback to update timer display (receives time string)
        on_complete_callback: callback when timer completes (receives session type)
    
    Returns:
        Tuple of (container widget, PomodoroTimer instance)
    """
    # Timer display
    timer_label = ft.Text(
        "25:00",
        size=48,
        weight="bold",
        color="#7c3aed",
        text_align="center",
    )

    # Completion alert (hidden by default)
    alert_text = ft.Text(
        "",
        size=14,
        color="#42a5f5",
        text_align="center",
        weight="w500",
    )

    # Control buttons
    start_button = ft.ElevatedButton(
        "▶ Start",
        width=120,
        height=45,
        color="#ffffff",
        bgcolor="#7c3aed",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )

    stop_button = ft.OutlinedButton(
        "⏹ Stop",
        width=120,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    # Initialize timer
    timer = PomodoroTimer(work_minutes=25, break_minutes=5)

    def handle_timer_tick(time_str: str):
        """Update the timer display."""
        timer_label.value = time_str
        alert_text.value = ""
        try:
            on_timer_callback(time_str)
        except:
            pass

    def handle_timer_complete(session_type: str):
        """Show alert when timer completes."""
        alert_text.value = f"✨ {session_type} session complete! Take a break."
        try:
            if on_complete_callback:
                on_complete_callback(session_type)
        except:
            pass

    timer.on_tick = handle_timer_tick
    timer.on_complete = handle_timer_complete

    def on_start(e):
        timer.start()
        start_button.disabled = True
        stop_button.disabled = False
        try:
            start_button.update()
            stop_button.update()
        except:
            pass

    def on_stop(e):
        timer.stop()
        start_button.disabled = False
        stop_button.disabled = True
        alert_text.value = ""
        try:
            start_button.update()
            stop_button.update()
            alert_text.update()
        except:
            pass

    start_button.on_click = on_start
    stop_button.on_click = on_stop
    stop_button.disabled = True

    # Layout
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "⏲️ Pomodoro Timer",
                    size=18,
                    weight="w600",
                    color="#333",
                ),
                timer_label,
                alert_text,
                ft.Row(
                    [start_button, stop_button],
                    alignment="center",
                    spacing=12,
                ),
            ],
            alignment="center",
            spacing=16,
            horizontal_alignment="center",
        ),
        padding=ft.padding.all(24),
        bgcolor="#f5f3ff",
        border_radius=12,
        border=ft.border.all(1, "#e9d5ff"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color="#0000000d",
            offset=ft.Offset(0, 3),
        ),
    )

    return container, timer
