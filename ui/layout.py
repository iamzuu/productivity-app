"""Main layout composition for Productivity Tracker."""
import flet as ft
from ui.header import build_header
from ui.tabs import build_tabs
from ui.theme import get_theme


def build_page_layout(page: ft.Page, theme_state: dict):
    """
    Build the main page layout with header and tabbed content.
    
    Args:
        page: The Flet page instance.
        theme_state: Dictionary with current_theme key.
        
    Returns:
        ft.Column: The main layout column with header and tabs.
    """
    # Get current theme
    theme = get_theme(theme_state.get("current_theme", "light_blue"))
    
    # Build header
    header = build_header(theme)

    # Build tabbed interface
    tabs = build_tabs(page, theme_state)

    # Main layout
    layout = ft.Column(
        [
            header,
            tabs,
        ],
        spacing=0,
        expand=True,
    )

    return layout
