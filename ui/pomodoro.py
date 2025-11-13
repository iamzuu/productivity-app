"""Pomodoro timer UI section for Productivity Tracker."""
import flet as ft
from core.pomodoro import PomodoroTimer


def build_pomodoro_section(page: ft.Page):
    """
    Build the Pomodoro timer section with UI and event handlers.
    
    Args:
        page: The Flet page instance.
        
    Returns:
        tuple: (pomodoro_container, timer, handler_dict)
        where handler_dict contains: start_timer, stop_timer
    """
    # Pomodoro timer display
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

    # Initialize timer
    timer = PomodoroTimer()

    def on_timer_tick(time_str):
        """Update timer display."""
        timer_display.value = time_str
        page.update()

    def on_timer_complete(session_type):
        """Handle timer completion."""
        timer_status.value = f"✨ {session_type} Complete!"
        page.update()

    timer.on_tick = on_timer_tick
    timer.on_complete = on_timer_complete

    def start_timer(e):
        """Start the Pomodoro timer."""
        timer.start()
        start_button.disabled = True
        stop_button.disabled = False
        page.update()

    def stop_timer(e):
        """Stop the Pomodoro timer."""
        timer.stop()
        timer_display.value = "25:00"
        timer_status.value = ""
        start_button.disabled = False
        stop_button.disabled = True
        page.update()

    start_button.on_click = start_timer
    stop_button.on_click = stop_timer

    # Pomodoro container
    pomodoro_container = ft.Container(
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
    )

    handler_dict = {
        "start_timer": start_timer,
        "stop_timer": stop_timer,
    }

    return pomodoro_container, timer, handler_dict
