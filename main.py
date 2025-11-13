"""
Productivity Tracker - Main Entry Point
Clean and modular architecture with UI separated into modules.
Supports multiple themes: Light Blue, Dark Blue, and Pink.
"""
import flet as ft
from ui.layout import build_page_layout
from ui.theme import get_theme, LIGHT_BLUE_THEME


def main(page: ft.Page):
    """
    Main app function with theme support.
    
    Initializes the page with theme and builds the layout from UI modules.
    """
    # Configure page
    page.title = "Productivity Tracker"
    page.window_width = 500
    page.window_height = 900
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    # Theme state (mutable reference for theme switching)
    theme_state = {"current_theme": "light_blue"}
    
    def apply_theme(theme_key: str):
        """Apply theme and refresh layout."""
        theme_state["current_theme"] = theme_key
        theme = get_theme(theme_key)
        page.bgcolor = theme["background"]
        page.clean()
        layout = build_page_layout(page, theme_state)
        page.add(layout)
        page.update()
    
    # Apply initial theme
    initial_theme = get_theme("light_blue")
    page.bgcolor = initial_theme["background"]

    # Build and add the main layout
    layout = build_page_layout(page, theme_state)
    page.add(layout)
    
    # Store apply_theme in page for Settings to access
    page.apply_theme = apply_theme


if __name__ == "__main__":
    ft.app(target=main)


