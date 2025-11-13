"""Header section with greeting for Productivity Tracker - Modernized."""
import flet as ft
from core.utils import get_greeting


def build_header(theme: dict) -> ft.Container:
    """
    Build the greeting header section with modern styling.
    
    Args:
        theme: Theme dictionary with color definitions.
    
    Returns:
        ft.Container: The greeting section with modern design.
    """
    greeting = ft.Container(
        content=ft.Text(
            get_greeting(),
            size=20,
            weight="bold",
            color=theme["header_text"],
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=24),
        bgcolor=theme["header_bg"],
        border_radius=0,
        margin=0,
    )
    return greeting
