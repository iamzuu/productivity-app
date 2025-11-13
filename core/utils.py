"""
Utility functions for the productivity app.
"""
from datetime import datetime
from typing import Optional


def format_date(date_str: Optional[str]) -> str:
    """Format a date string (YYYY-MM-DD) to a human-readable format."""
    if not date_str:
        return "No date"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %b %Y")
    except (ValueError, TypeError):
        return date_str


def is_overdue(date_str: Optional[str]) -> bool:
    """Check if a task date is overdue (before today)."""
    if not date_str:
        return False
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now().date()
        return date_obj.date() < today
    except (ValueError, TypeError):
        return False


def is_today(date_str: Optional[str]) -> bool:
    """Check if a task date is today."""
    if not date_str:
        return False
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now().date()
        return date_obj.date() == today
    except (ValueError, TypeError):
        return False


def get_greeting() -> str:
    """Get a greeting message with current time context."""
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    return f"👋 Hello Zu, {greeting}! What would you like to work on today?"
