"""Pomodoro timer UI section for Productivity Tracker - Modernized."""
import flet as ft
from core.pomodoro import PomodoroTimer

# Modern color palette
BORDER_RADIUS = 12


def build_pomodoro_section(page: ft.Page, theme: dict):
    """
    Build the Pomodoro timer section with modern UI and event handlers.
    
    Args:
        page: The Flet page instance.
        
    Returns:
        tuple: (pomodoro_container, timer, handler_dict)
        where handler_dict contains: start_timer, stop_timer
    """
    # Pomodoro timer display
    timer_display = ft.Text(
        "25:00",
        size=64,
        weight="bold",
        color=theme.get("primary", "#007bff"),
        text_align="center",
    )

    timer_status = ft.Text(
        "",
        size=14,
        color=theme.get("success", "#28a745"),
        text_align="center",
        weight="w500",
    )

    start_button = ft.ElevatedButton(
        "▶ Start",
        width=130,
        height=48,
        bgcolor=theme.get("primary", "#007bff"),
        color="white",
        elevation=2,
    )

    stop_button = ft.ElevatedButton(
        "⏹ Stop",
        width=130,
        height=48,
        bgcolor=theme.get("danger", "#dc3545"),
        color="white",
        elevation=2,
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

    # disable stop initially
    stop_button.disabled = True

    # Pomodoro container with modern styling
    pomodoro_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("⏲️ Pomodoro Timer", size=18, weight="bold", color=theme.get("text_primary", "#1a1a1a")),
                ft.Divider(height=1, color=theme.get("border", "#e0e0e0")),
                timer_display,
                timer_status,
                ft.Row(
                    [start_button, stop_button],
                    alignment="center",
                    spacing=16,
                ),
            ],
            alignment="center",
            spacing=20,
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=24),
        bgcolor=theme.get("surface", "white"),
        border_radius=BORDER_RADIUS,
        margin=ft.margin.only(left=16, right=16, top=16, bottom=16),
        border=ft.border.all(1, theme.get("border", "#e0e0e0")),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color="rgba(0, 0, 0, 0.08)",
            offset=ft.Offset(0, 2),
        ),
    )

    handler_dict = {
        "start_timer": start_timer,
        "stop_timer": stop_timer,
    }

    return pomodoro_container, timer, handler_dict
