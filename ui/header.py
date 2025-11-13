"""Header section with greeting for Productivity Tracker."""
import flet as ft
from core.utils import get_greeting


def build_header() -> ft.Container:
    """
    Build the greeting header section.
    
    Returns:
        ft.Container: The greeting section with dark background and white text.
    """
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
    return greeting
