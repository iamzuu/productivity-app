"""Tab-based navigation for Productivity Tracker - Modernized with theme support."""
import flet as ft
from ui.tasks import build_task_section
from ui.pomodoro import build_pomodoro_section
from ui.theme import get_theme, THEME_NAMES, THEME_KEYS


def build_tabs(page: ft.Page, theme_state: dict):
    """
    Build a tabbed interface with Tasks, Pomodoro, and Settings tabs with theme support.
    
    Args:
        page: The Flet page instance.
        theme_state: Dictionary with current_theme key.
        
    Returns:
        ft.Tabs: The tabs component with all sections.
    """
    # Get current theme
    theme = get_theme(theme_state.get("current_theme", "light_blue"))
    
    # Build task section
    input_container, task_list_container, date_display, task_handlers = build_task_section(page, theme)

    # Build pomodoro section
    pomodoro_container, timer, pomodoro_handlers = build_pomodoro_section(page, theme)

    # Tasks tab content
    tasks_content = ft.Column(
        [
            input_container,
            ft.Container(
                content=ft.Text("📝 Your Tasks", size=18, weight="bold", color=theme["text_primary"]),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                bgcolor="transparent",
                border_radius=0,
                margin=ft.margin.only(left=16, right=16, top=20, bottom=12),
            ),
            task_list_container,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    # Pomodoro tab content
    pomodoro_content = ft.Column(
        [
            ft.Container(
                content=ft.Text("⏲️ Pomodoro Timer", size=18, weight="bold", color=theme["text_primary"]),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                bgcolor="transparent",
                border_radius=0,
                margin=ft.margin.only(left=16, right=16, top=20, bottom=12),
            ),
            pomodoro_container,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    # Theme selector dropdown
    theme_dropdown = ft.Dropdown(
        label="Theme",
        options=[ft.dropdown.Option(name) for name in THEME_NAMES],
        value=THEME_NAMES[THEME_KEYS.index(theme_state.get("current_theme", "light_blue"))],
        width=150,
        filled=True,
        bgcolor=theme["surface"],
        border_color=theme["border"],
        text_size=13,
    )

    def on_theme_change(e):
        """Handle theme change."""
        selected_name = theme_dropdown.value
        theme_index = THEME_NAMES.index(selected_name)
        theme_key = THEME_KEYS[theme_index]
        if hasattr(page, 'apply_theme'):
            page.apply_theme(theme_key)

    theme_dropdown.on_change = on_theme_change

    # Settings tab content
    settings_content = ft.Column(
        [
            ft.Container(
                content=ft.Text("⚙️ Settings", size=18, weight="bold", color=theme["text_primary"]),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                bgcolor="transparent",
                border_radius=0,
                margin=ft.margin.only(left=16, right=16, top=20, bottom=12),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Appearance", size=15, weight="bold", color=theme["text_primary"]),
                        ft.Divider(height=1, color=theme["border"]),
                        ft.Row(
                            [
                                ft.Text("Theme", size=13, color=theme["text_secondary"]),
                                theme_dropdown,
                            ],
                            alignment="spaceBetween",
                            spacing=10,
                        ),
                        ft.Divider(height=1, color=theme["border"]),
                        ft.Text("Pomodoro Duration", size=15, weight="bold", color=theme["text_primary"]),
                        ft.Divider(height=1, color=theme["border"]),
                        ft.Row(
                            [
                                ft.Text("Work (minutes):", size=12, color=theme["text_secondary"]),
                                ft.TextField(
                                    value="25",
                                    width=80,
                                    input_filter=ft.NumbersOnlyInputFilter(),
                                    border_color=theme["border"],
                                    focused_border_color=theme["primary"],
                                    bgcolor=theme["surface"],
                                    text_size=12,
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            [
                                ft.Text("Break (minutes):", size=12, color=theme["text_secondary"]),
                                ft.TextField(
                                    value="5",
                                    width=80,
                                    input_filter=ft.NumbersOnlyInputFilter(),
                                    border_color=theme["border"],
                                    focused_border_color=theme["primary"],
                                    bgcolor=theme["surface"],
                                    text_size=12,
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Divider(height=1, color=theme["border"]),
                        ft.ElevatedButton(
                            "Save Settings",
                            width=200,
                            bgcolor=theme["primary"],
                            color="white",
                            elevation=2,
                        ),
                    ],
                    spacing=14,
                ),
                padding=20,
                bgcolor=theme["surface"],
                border_radius=12,
                margin=ft.margin.only(left=16, right=16, bottom=16),
                border=ft.border.all(1, theme["border"]),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color="rgba(0, 0, 0, 0.08)",
                    offset=ft.Offset(0, 2),
                ),
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    # Create tabs with modern styling
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        indicator_color=theme["primary"],
        label_color=theme["text_secondary"],
        unselected_label_color=theme["text_secondary"],
        tabs=[
            ft.Tab(
                text="📝 Tasks",
                content=tasks_content,
            ),
            ft.Tab(
                text="⏲️ Pomodoro",
                content=pomodoro_content,
            ),
            ft.Tab(
                text="⚙️ Settings",
                content=settings_content,
            ),
        ],
        expand=True,
    )

    return tabs
    return tabs
