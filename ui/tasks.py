"""Task management UI section for Productivity Tracker - Modernized with theme support."""
import flet as ft
from core.storage import load_tasks, save_tasks

BORDER_RADIUS = 12


def build_task_section(page: ft.Page, theme: dict):
    """
    Build the task input and task list section with modern styling and theme support.
    
    Args:
        page: The Flet page instance.
        theme: Theme dictionary with color definitions.
        
    Returns:
        tuple: (input_container, task_list_container, deadline_display, handler_dict)
    """
    # Load tasks
    tasks = load_tasks()
    selected_deadline = None

    # Input fields with theme-aware styling
    task_title = ft.TextField(
        label="Task Title",
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
        label_style=ft.TextStyle(color=theme["text_secondary"], size=13),
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        color=theme["text_primary"],
        expand=True,
        content_padding=ft.padding.all(12),
    )

    mata_kuliah = ft.TextField(
        label="Mata Kuliah / Subject",
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
        label_style=ft.TextStyle(color=theme["text_secondary"], size=13),
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        color=theme["text_primary"],
        expand=True,
        content_padding=ft.padding.all(12),
    )

    deskripsi = ft.TextField(
        label="Deskripsi Tugas / Description",
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
        label_style=ft.TextStyle(color=theme["text_secondary"], size=13),
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        color=theme["text_primary"],
        min_lines=3,
        max_lines=5,
        expand=True,
        content_padding=ft.padding.all(12),
    )

    deadline_display = ft.Text(
        "📅 No deadline",
        size=12,
        color=theme["text_primary"],
        weight="w500",
    )

    # Date picker
    date_picker = ft.DatePicker()
    page.overlay.append(date_picker)

    add_button = ft.ElevatedButton(
        text="Add Task",
        width=120,
        height=48,
        bgcolor=theme["primary"],
        color="white",
        elevation=2,
    )

    # Task list column
    tasks_column = ft.Column(spacing=12)

    # Event handlers
    def build_task_ui():
        """Rebuild the task list UI with modern cards."""
        tasks_column.controls.clear()
        for i, task in enumerate(tasks):
            title_text = task.get("title", "Untitled")
            mata_kuliah_text = task.get("mata_kuliah", "")
            deadline_text = task.get("deadline", "No deadline")
            deskripsi_text = task.get("deskripsi", "")
            is_done = task.get("done", False)

            # Build task details column
            details_content = [
                ft.Text(
                    title_text,
                    size=15,
                    color=theme["text_secondary"] if is_done else theme["text_primary"],
                    weight="bold",
                ),
            ]
            
            if mata_kuliah_text:
                details_content.append(
                    ft.Text(
                        f"📚 {mata_kuliah_text}",
                        size=12,
                        color=theme["text_secondary"],
                        weight="w500",
                    )
                )
            
            details_content.append(
                ft.Text(
                    f"📅 {deadline_text}",
                    size=12,
                    color=theme["danger"],
                    weight="w500",
                )
            )
            
            if deskripsi_text:
                details_content.append(
                    ft.Text(
                        deskripsi_text,
                        size=12,
                        color=theme["text_secondary"],
                        max_lines=2,
                    )
                )

            task_details = ft.Column(
                details_content,
                expand=True,
                spacing=6,
            )

            # Delete button with hover effect
            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=theme["danger"],
                icon_size=20,
                on_click=lambda e, idx=i: delete_task(idx),
                hover_color="rgba(220, 53, 69, 0.1)",
            )

            task_row = ft.Row(
                [
                    ft.Checkbox(
                        value=is_done,
                        on_change=lambda e, idx=i: toggle_task(idx),
                        fill_color=theme["primary"],
                    ),
                    task_details,
                    delete_btn,
                ],
                alignment="spaceBetween",
                spacing=12,
            )

            tasks_column.controls.append(
                ft.Container(
                    content=task_row,
                    padding=16,
                    bgcolor=theme["surface"],
                    border_radius=BORDER_RADIUS,
                    border=ft.border.all(1, theme["border"]),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        color="rgba(0, 0, 0, 0.08)",
                        offset=ft.Offset(0, 2),
                    ),
                )
            )

    def add_task(e):
        """Add new task with all parameters."""
        nonlocal selected_deadline
        title = task_title.value.strip()
        subject = mata_kuliah.value.strip()
        desc = deskripsi.value.strip()
        
        if not title:
            return

        tasks.append({
            "title": title,
            "done": False,
            "deadline": selected_deadline or "No deadline",
            "mata_kuliah": subject,
            "deskripsi": desc,
        })
        save_tasks(tasks)
        
        # Clear inputs
        task_title.value = ""
        mata_kuliah.value = ""
        deskripsi.value = ""
        selected_deadline = None
        deadline_display.value = "📅 No deadline"
        date_picker.value = None
        
        task_title.focus()
        build_task_ui()
        page.update()

    def toggle_task(index):
        """Toggle task done status."""
        if 0 <= index < len(tasks):
            tasks[index]["done"] = not tasks[index]["done"]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def delete_task(index):
        """Delete a task."""
        if 0 <= index < len(tasks):
            del tasks[index]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def on_date_selected(e):
        """Handle date picker change."""
        nonlocal selected_deadline
        if date_picker.value:
            selected_deadline = str(date_picker.value).split()[0]
            deadline_display.value = f"📅 {selected_deadline}"
        else:
            selected_deadline = None
            deadline_display.value = "📅 No deadline"
        page.update()

    def open_date_picker(e):
        """Open date picker."""
        page.open(date_picker)

    # Wire up event handlers
    add_button.on_click = add_task
    date_picker.on_change = on_date_selected
    task_title.on_submit = add_task

    # Initial task list
    build_task_ui()

    # Input container with modern styling
    input_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Add New Task",
                    size=16,
                    weight="bold",
                    color=theme["text_primary"],
                ),
                task_title,
                mata_kuliah,
                deskripsi,
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.CALENDAR_TODAY,
                            icon_color=theme["primary"],
                            icon_size=20,
                            on_click=open_date_picker,
                        ),
                        deadline_display,
                        ft.Container(expand=True),
                        add_button,
                    ],
                    alignment="spaceBetween",
                    spacing=10,
                    vertical_alignment="center",
                ),
            ],
            spacing=12,
        ),
        padding=20,
        bgcolor=theme["surface"],
        border_radius=BORDER_RADIUS,
        margin=ft.margin.only(left=16, right=16, top=16, bottom=30),
        border=ft.border.all(1, theme["border"]),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color="rgba(0, 0, 0, 0.08)",
            offset=ft.Offset(0, 2),
        ),
    )

    # Task list container with modern styling
    task_list_container = ft.Container(
        content=tasks_column,
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=theme["surface_alt"],
        border_radius=BORDER_RADIUS,
        margin=ft.margin.only(left=16, right=16, bottom=16),
    )

    # Return components and handlers
    handler_dict = {
        "add_task": add_task,
        "toggle_task": toggle_task,
        "delete_task": delete_task,
        "build_task_ui": build_task_ui,
        "tasks": tasks,
    }

    return input_container, task_list_container, deadline_display, handler_dict

"""Task management UI section for Productivity Tracker - Modernized with theme support."""
import flet as ft
from core.storage import load_tasks, save_tasks

BORDER_RADIUS = 12


def build_task_section(page: ft.Page, theme: dict):
    """
    Build the task input and task list section with modern styling and theme support.
    
    Args:
        page: The Flet page instance.
        theme: Theme dictionary with color definitions.
        
    Returns:
        tuple: (input_container, task_list_container, deadline_display, handler_dict)
    """
    # Load tasks
    tasks = load_tasks()
    selected_deadline = None

    # Input fields with theme-aware styling
    task_title = ft.TextField(
        label="Task Title",
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
        label_style=ft.TextStyle(color=theme["text_secondary"], size=13),
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        color=theme["text_primary"],
        expand=True,
        content_padding=ft.padding.all(12),
    )

    mata_kuliah = ft.TextField(
        label="Mata Kuliah / Subject",
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
        label_style=ft.TextStyle(color=theme["text_secondary"], size=13),
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        color=theme["text_primary"],
        expand=True,
        content_padding=ft.padding.all(12),
    )

    deskripsi = ft.TextField(
        label="Deskripsi Tugas / Description",
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
        label_style=ft.TextStyle(color=theme["text_secondary"], size=13),
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        color=theme["text_primary"],
        min_lines=3,
        max_lines=5,
        expand=True,
        content_padding=ft.padding.all(12),
    )

    deadline_display = ft.Text(
        "📅 No deadline",
        size=12,
        color=theme["text_primary"],
        weight="w500",
    )

    # Date picker
    date_picker = ft.DatePicker()
    page.overlay.append(date_picker)

    add_button = ft.ElevatedButton(
        text="Add Task",
        width=120,
        height=48,
        bgcolor=theme["primary"],
        color="white",
        elevation=2,
    )

    # Task list column
    tasks_column = ft.Column(spacing=12)

    # Event handlers
    def build_task_ui():
        """Rebuild the task list UI with modern cards."""
        tasks_column.controls.clear()
        for i, task in enumerate(tasks):
            title_text = task.get("title", "Untitled")
            mata_kuliah_text = task.get("mata_kuliah", "")
            deadline_text = task.get("deadline", "No deadline")
            deskripsi_text = task.get("deskripsi", "")
            is_done = task.get("done", False)

            # Build task details column
            details_content = [
                ft.Text(
                    title_text,
                    size=15,
                    color=theme["text_secondary"] if is_done else theme["text_primary"],
                    weight="bold",
                ),
            ]
            
            if mata_kuliah_text:
                details_content.append(
                    ft.Text(
                        f"📚 {mata_kuliah_text}",
                        size=12,
                        color=theme["text_secondary"],
                        weight="w500",
                    )
                )
            
            details_content.append(
                ft.Text(
                    f"📅 {deadline_text}",
                    size=12,
                    color=theme["danger"],
                    weight="w500",
                )
            )
            
            if deskripsi_text:
                details_content.append(
                    ft.Text(
                        deskripsi_text,
                        size=12,
                        color=theme["text_secondary"],
                        max_lines=2,
                    )
                )

            task_details = ft.Column(
                details_content,
                expand=True,
                spacing=6,
            )

            # Delete button with hover effect
            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=theme["danger"],
                icon_size=20,
                on_click=lambda e, idx=i: delete_task(idx),
                hover_color="rgba(220, 53, 69, 0.1)",
            )

            task_row = ft.Row(
                [
                    ft.Checkbox(
                        value=is_done,
                        on_change=lambda e, idx=i: toggle_task(idx),
                        fill_color=theme["primary"],
                    ),
                    task_details,
                    delete_btn,
                ],
                alignment="spaceBetween",
                spacing=12,
            )

            tasks_column.controls.append(
                ft.Container(
                    content=task_row,
                    padding=16,
                    bgcolor=theme["surface"],
                    border_radius=BORDER_RADIUS,
                    border=ft.border.all(1, theme["border"]),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        color="rgba(0, 0, 0, 0.08)",
                        offset=ft.Offset(0, 2),
                    ),
                )
            )

    def add_task(e):
        """Add new task with all parameters."""
        nonlocal selected_deadline
        title = task_title.value.strip()
        subject = mata_kuliah.value.strip()
        desc = deskripsi.value.strip()
        
        if not title:
            return

        tasks.append({
            "title": title,
            "done": False,
            "deadline": selected_deadline or "No deadline",
            "mata_kuliah": subject,
            "deskripsi": desc,
        })
        save_tasks(tasks)
        
        # Clear inputs
        task_title.value = ""
        mata_kuliah.value = ""
        deskripsi.value = ""
        selected_deadline = None
        deadline_display.value = "📅 No deadline"
        date_picker.value = None
        
        task_title.focus()
        build_task_ui()
        page.update()

    def toggle_task(index):
        """Toggle task done status."""
        if 0 <= index < len(tasks):
            tasks[index]["done"] = not tasks[index]["done"]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def delete_task(index):
        """Delete a task."""
        if 0 <= index < len(tasks):
            del tasks[index]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def on_date_selected(e):
        """Handle date picker change."""
        nonlocal selected_deadline
        if date_picker.value:
            selected_deadline = str(date_picker.value).split()[0]
            deadline_display.value = f"📅 {selected_deadline}"
        else:
            selected_deadline = None
            deadline_display.value = "📅 No deadline"
        page.update()

    def open_date_picker(e):
        """Open date picker."""
        page.open(date_picker)

    # Wire up event handlers
    add_button.on_click = add_task
    date_picker.on_change = on_date_selected
    task_title.on_submit = add_task

    # Initial task list
    build_task_ui()

    # Input container with modern styling
    input_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Add New Task",
                    size=16,
                    weight="bold",
                    color=theme["text_primary"],
                ),
                task_title,
                mata_kuliah,
                deskripsi,
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.CALENDAR_TODAY,
                            icon_color=theme["primary"],
                            icon_size=20,
                            on_click=open_date_picker,
                        ),
                        deadline_display,
                        ft.Container(expand=True),
                        add_button,
                    ],
                    alignment="spaceBetween",
                    spacing=10,
                    vertical_alignment="center",
                ),
            ],
            spacing=12,
        ),
        padding=20,
        bgcolor=theme["surface"],
        border_radius=BORDER_RADIUS,
        margin=ft.margin.only(left=16, right=16, top=16, bottom=30),
        border=ft.border.all(1, theme["border"]),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color="rgba(0, 0, 0, 0.08)",
            offset=ft.Offset(0, 2),
        ),
    )

    # Task list container with modern styling
    task_list_container = ft.Container(
        content=tasks_column,
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=theme["surface_alt"],
        border_radius=BORDER_RADIUS,
        margin=ft.margin.only(left=16, right=16, bottom=16),
    )

    # Return components and handlers
    handler_dict = {
        "add_task": add_task,
        "toggle_task": toggle_task,
        "delete_task": delete_task,
        "build_task_ui": build_task_ui,
        "tasks": tasks,
    }

    return input_container, task_list_container, deadline_display, handler_dict
"""Task management UI section for Productivity Tracker - Modernized with theme support."""
import flet as ft
from core.storage import load_tasks, save_tasks

BORDER_RADIUS = 12


def build_task_section(page: ft.Page, theme: dict):
    """
    Build the task input and task list section with modern styling and theme support.
    
    Args:
        page: The Flet page instance.
        theme: Theme dictionary with color definitions.
        
    Returns:
        tuple: (input_container, task_list_container, deadline_display, handler_dict)
    """
    # Load tasks
    tasks = load_tasks()
    selected_deadline = None

    # Input fields with theme-aware styling
    task_title = ft.TextField(
        label="Task Title",
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
        label_style=ft.TextStyle(color=theme["text_secondary"], size=13),
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        color=theme["text_primary"],
        expand=True,
        content_padding=ft.padding.all(12),
    )

    mata_kuliah = ft.TextField(
        label="Mata Kuliah / Subject",
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
        label_style=ft.TextStyle(color=theme["text_secondary"], size=13),
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        color=theme["text_primary"],
        expand=True,
        content_padding=ft.padding.all(12),
    )

    deskripsi = ft.TextField(
        label="Deskripsi Tugas / Description",
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
        label_style=ft.TextStyle(color=theme["text_secondary"], size=13),
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        color=theme["text_primary"],
        min_lines=3,
        max_lines=5,
        expand=True,
        content_padding=ft.padding.all(12),
    )

    deadline_display = ft.Text(
        "📅 No deadline",
        size=12,
        color=theme["text_primary"],
        weight="w500",
    )

    # Date picker
    date_picker = ft.DatePicker()
    page.overlay.append(date_picker)

    add_button = ft.ElevatedButton(
        text="Add Task",
        width=120,
        height=48,
        bgcolor=theme["primary"],
        color="white",
        elevation=2,
    )

    # Task list column
    tasks_column = ft.Column(spacing=12)

    # Event handlers
    def build_task_ui():
        """Rebuild the task list UI with modern cards."""
        tasks_column.controls.clear()
        for i, task in enumerate(tasks):
            title_text = task.get("title", "Untitled")
            mata_kuliah_text = task.get("mata_kuliah", "")
            deadline_text = task.get("deadline", "No deadline")
            deskripsi_text = task.get("deskripsi", "")
            is_done = task.get("done", False)

            # Build task details column
            details_content = [
                ft.Text(
                    title_text,
                    size=15,
                    color=theme["text_secondary"] if is_done else theme["text_primary"],
                    weight="bold",
                ),
            ]
            
            if mata_kuliah_text:
                details_content.append(
                    ft.Text(
                        f"📚 {mata_kuliah_text}",
                        size=12,
                        color=theme["text_secondary"],
                        weight="w500",
                    )
                )
            
            details_content.append(
                ft.Text(
                    f"📅 {deadline_text}",
                    size=12,
                    color=theme["danger"],
                    weight="w500",
                )
            )
            
            if deskripsi_text:
                details_content.append(
                    ft.Text(
                        deskripsi_text,
                        size=12,
                        color=theme["text_secondary"],
                        max_lines=2,
                    )
                )

            task_details = ft.Column(
                details_content,
                expand=True,
                spacing=6,
            )

            # Delete button with hover effect
            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=theme["danger"],
                icon_size=20,
                on_click=lambda e, idx=i: delete_task(idx),
                hover_color="rgba(211, 47, 47, 0.1)",
            )

            task_row = ft.Row(
                [
                    ft.Checkbox(
                        value=is_done,
                        on_change=lambda e, idx=i: toggle_task(idx),
                        fill_color=theme["primary"],
                    ),
                    task_details,
                    delete_btn,
                ],
                alignment="spaceBetween",
                spacing=12,
            )

            tasks_column.controls.append(
                ft.Container(
                    content=task_row,
                    padding=16,
                    bgcolor=theme["surface"],
                    border_radius=BORDER_RADIUS,
                    border=ft.border.all(1, theme["border"]),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        color="rgba(0, 0, 0, 0.08)",
                        offset=ft.Offset(0, 2),
                    ),
                )
            )

    def add_task(e):
        """Add new task with all parameters."""
        nonlocal selected_deadline
        title = task_title.value.strip()
        subject = mata_kuliah.value.strip()
        desc = deskripsi.value.strip()
        
        if not title:
            return

        tasks.append({
            "title": title,
            "done": False,
            "deadline": selected_deadline or "No deadline",
            "mata_kuliah": subject,
            "deskripsi": desc,
        })
        save_tasks(tasks)
        
        # Clear inputs
        task_title.value = ""
        mata_kuliah.value = ""
        deskripsi.value = ""
        selected_deadline = None
        deadline_display.value = "📅 No deadline"
        date_picker.value = None
        
        task_title.focus()
        build_task_ui()
        page.update()

    def toggle_task(index):
        """Toggle task done status."""
        if 0 <= index < len(tasks):
            tasks[index]["done"] = not tasks[index]["done"]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def delete_task(index):
        """Delete a task."""
        if 0 <= index < len(tasks):
            del tasks[index]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def on_date_selected(e):
        """Handle date picker change."""
        nonlocal selected_deadline
        if date_picker.value:
            selected_deadline = str(date_picker.value).split()[0]
            deadline_display.value = f"📅 {selected_deadline}"
        else:
            selected_deadline = None
            deadline_display.value = "📅 No deadline"
        page.update()

    def open_date_picker(e):
        """Open date picker."""
        page.open(date_picker)

    # Wire up event handlers
    add_button.on_click = add_task
    date_picker.on_change = on_date_selected
    task_title.on_submit = add_task

    # Initial task list
    build_task_ui()

    # Input container with modern styling
    input_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Add New Task",
                    size=16,
                    weight="bold",
                    color=theme["text_primary"],
                ),
                task_title,
                mata_kuliah,
                deskripsi,
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.CALENDAR_TODAY,
                            icon_color=theme["primary"],
                            icon_size=20,
                            on_click=open_date_picker,
                        ),
                        deadline_display,
                        ft.Container(expand=True),
                        add_button,
                    ],
                    alignment="spaceBetween",
                    spacing=10,
                    vertical_alignment="center",
                ),
            ],
            spacing=12,
        ),
        padding=20,
        bgcolor=theme["surface"],
        border_radius=BORDER_RADIUS,
        margin=ft.margin.only(left=16, right=16, top=16, bottom=30),
        border=ft.border.all(1, theme["border"]),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color="rgba(0, 0, 0, 0.08)",
            offset=ft.Offset(0, 2),
        ),
    )

    # Task list container with modern styling
    task_list_container = ft.Container(
        content=tasks_column,
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor="#fafafa",
        border_radius=BORDER_RADIUS,
        margin=ft.margin.only(left=16, right=16, bottom=16),
    )

    # Return components and handlers
    handler_dict = {
        "add_task": add_task,
        "toggle_task": toggle_task,
        "delete_task": delete_task,
        "build_task_ui": build_task_ui,
        "tasks": tasks,
    }

    return input_container, task_list_container, deadline_display, handler_dict
