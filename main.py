"""
Productivity Tracker - Main Entry Point
Clean and modular architecture with UI separated into modules.
"""
import flet as ft
from ui.layout import build_page_layout


def main(page: ft.Page):
    """
    Main app function.
    
    Initializes the page and builds the layout from UI modules.
    """
    # Configure page
    page.title = "Productivity Tracker"
    page.window_width = 500
    page.window_height = 900
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#eeeeee"

    # Build and add the main layout
    layout = build_page_layout(page)
    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)


