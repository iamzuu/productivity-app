"""Theme system for Productivity Tracker - Light Blue, Dark Blue, and Pink themes."""

# Light Blue Theme (Current)
LIGHT_BLUE_THEME = {
    "name": "Light Blue",
    "primary": "#007bff",
    "primary_hover": "#0056b3",
    "primary_light": "#e7f1ff",
    "secondary": "#6c757d",
    "success": "#28a745",
    "danger": "#dc3545",
    "background": "#ffffff",
    "surface": "#ffffff",
    "surface_alt": "#f5f5f5",
    "border": "#e0e0e0",
    "text_primary": "#1a1a1a",
    "text_secondary": "#666666",
    "header_bg": "#007bff",
    "header_text": "#ffffff",
}

# Dark Blue Theme
DARK_BLUE_THEME = {
    "name": "Dark Blue",
    "primary": "#007bff",
    "primary_hover": "#0056b3",
    "primary_light": "#1a3a5c",
    "secondary": "#b0b0b0",
    "success": "#28a745",
    "danger": "#ff6b6b",
    "background": "#1a1a1a",
    "surface": "#2d2d2d",
    "surface_alt": "#3d3d3d",
    "border": "#4d4d4d",
    "text_primary": "#ffffff",
    "text_secondary": "#b0b0b0",
    "header_bg": "#0056b3",
    "header_text": "#ffffff",
}

# Pink Theme
PINK_THEME = {
    "name": "Pink",
    "primary": "#ff1493",  # Deep Pink
    "primary_hover": "#c71585",  # Medium Violet Red
    "primary_light": "#ffe4f0",
    "secondary": "#ff69b4",  # Hot Pink
    "success": "#50c878",
    "danger": "#ff4757",
    "background": "#fff5f9",
    "surface": "#ffffff",
    "surface_alt": "#ffe4f0",
    "border": "#ffc0d9",
    "text_primary": "#1a1a1a",
    "text_secondary": "#666666",
    "header_bg": "#ff1493",
    "header_text": "#ffffff",
}

# Available themes
THEMES = {
    "light_blue": LIGHT_BLUE_THEME,
    "dark_blue": DARK_BLUE_THEME,
    "pink": PINK_THEME,
}

THEME_NAMES = ["Light Blue", "Dark Blue", "Pink"]
THEME_KEYS = list(THEMES.keys())

def get_theme(theme_key: str) -> dict:
    """Get theme by key. Defaults to light blue if not found."""
    return THEMES.get(theme_key, LIGHT_BLUE_THEME)

def get_all_themes() -> dict:
    """Get all available themes."""
    return THEMES
