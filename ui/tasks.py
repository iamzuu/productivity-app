"""Task management UI section for Productivity Tracker.

Features:
- Preconfigured subject options (mata kuliah) as a Dropdown.
- Subject-colored accents for task cards.
- View switcher: "By Deadline" / "By Subject".
"""
import flet as ft
from core.storage import load_tasks, save_tasks

BORDER_RADIUS = 12

# Preconfigured subjects (mata kuliah)
SUBJECT_OPTIONS = [
    "Data Sains",
    "Etos Sandi V",
    "Hukum dan Etika Profesi",
    "Keamanan Internet of Things",
    "Metode Perancangan Modul Kripto",
    "Perancangan Papan Sirkuit",
    "Pemrosesan Sinyal Digital",
    "Sistem Tertanam",
]

SUBJECT_COLORS = {
    "Data Sains": "#7c3aed",
    "Etos Sandi V": "#ef5350",
    "Hukum dan Etika Profesi": "#42a5f5",
    "Keamanan Internet of Things": "#ab47bc",
    "Metode Perancangan Modul Kripto": "#ffa726",
    "Perancangan Papan Sirkuit": "#26a69a",
    "Pemrosesan Sinyal Digital": "#29b6f6",
    "Sistem Tertanam": "#8d6e63",
}


def build_task_section(page: ft.Page, theme: dict):
    """Build task input UI and task list with grouping options."""
    tasks = load_tasks()
    selected_deadline = None

    # Fields
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

    mata_kuliah = ft.Dropdown(
        hint_text="Pilih Mata Kuliah",
        options=[ft.dropdown.Option(s, text_style=ft.TextStyle(size=14, color=theme["text_primary"])) for s in SUBJECT_OPTIONS],
        value=SUBJECT_OPTIONS[0],
        expand=True,
        filled=True,
        fill_color=theme["surface"],
        border_color=theme["border"],
        focused_border_color=theme["primary"],
        border_width=1.5,
        text_style=ft.TextStyle(size=14, color=theme["text_primary"]),
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

    deadline_display = ft.Text("📅 No deadline", size=12, color=theme["text_primary"], weight="w500")

    date_picker = ft.DatePicker()
    page.overlay.append(date_picker)

    add_button = ft.ElevatedButton("Add Task", width=120, height=48, bgcolor=theme["primary"], color="white")

    # Compact view selector (no label) — moved to the task list header
    view_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("By Deadline"), ft.dropdown.Option("By Subject")],
        value="By Deadline",
        width=140,
        filled=True,
        bgcolor=theme["surface"],
        border_color=theme["border"],
        text_size=13,
    )

    tasks_column = ft.Column(spacing=12)

    # Helpers
    def render_task_card(i, task):
        title_text = task.get("title", "Untitled")
        subject = task.get("mata_kuliah", "")
        deadline_text = task.get("deadline", "No deadline")
        desc = task.get("deskripsi", "")
        done = task.get("done", False)

        accent = SUBJECT_COLORS.get(subject, theme.get("primary"))

        details = [
            ft.Text(title_text, size=15, color=theme["text_secondary"] if done else theme["text_primary"], weight="bold"),
        ]
        if subject:
            details.append(ft.Text(f"📚 {subject}", size=12, color=theme["text_secondary"], weight="w500"))
        details.append(ft.Text(f"📅 {deadline_text}", size=12, color=theme["danger"], weight="w500"))
        if desc:
            details.append(ft.Text(desc, size=12, color=theme["text_secondary"], max_lines=2))

        task_details = ft.Column(details, expand=True, spacing=6)

        delete_btn = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=theme["danger"], on_click=lambda e, idx=i: delete_task(idx))
        checkbox = ft.Checkbox(value=done, on_change=lambda e, idx=i: toggle_task(idx), fill_color=theme["primary"])

        card_inner = ft.Row([checkbox, task_details, delete_btn], alignment="spaceBetween", spacing=12)

        card = ft.Row([
            ft.Container(width=6, bgcolor=accent),
            ft.Container(content=card_inner, padding=12, bgcolor=theme["surface"], border_radius=BORDER_RADIUS, expand=True)
        ], spacing=0, alignment="start")

        # Return each task wrapped in a container (boxed card style)
        return ft.Container(
            content=card,
            padding=0,
            margin=ft.margin.only(bottom=10),
            border_radius=8,
            bgcolor=theme["surface"],
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color="rgba(0, 0, 0, 0.06)", offset=ft.Offset(0, 2)),
        )

    def build_task_ui():
        tasks_column.controls.clear()
        mode = view_dropdown.value

        if mode == "By Deadline":
            groups = {}
            for idx, t in enumerate(tasks):
                d = t.get("deadline", "No deadline")
                groups.setdefault(d, []).append((idx, t))

            def sort_key(d):
                return (1, "") if d == "No deadline" else (0, d)

            for d in sorted(groups.keys(), key=sort_key):
                tasks_column.controls.append(ft.Text(f"📅 {d}", size=14, weight="bold", color=theme.get("primary")))
                for idx, t in groups[d]:
                    tasks_column.controls.append(render_task_card(idx, t))
        else:
            subjects_seen = {s: [] for s in SUBJECT_OPTIONS}
            others = []
            for idx, t in enumerate(tasks):
                s = t.get("mata_kuliah", "")
                if s in subjects_seen:
                    subjects_seen[s].append((idx, t))
                else:
                    others.append((idx, t))

            for s in SUBJECT_OPTIONS:
                lst = subjects_seen.get(s, [])
                if not lst:
                    continue
                accent = SUBJECT_COLORS.get(s, theme.get("primary"))
                tasks_column.controls.append(ft.Text(f"📚 {s}", size=14, weight="bold", color=accent))
                for idx, t in lst:
                    tasks_column.controls.append(render_task_card(idx, t))

            if others:
                tasks_column.controls.append(ft.Text("Uncategorized", size=14, weight="bold", color=theme.get("text_primary")))
                for idx, t in others:
                    tasks_column.controls.append(render_task_card(idx, t))

    def add_task(e):
        nonlocal selected_deadline
        title = task_title.value.strip()
        subject = mata_kuliah.value or ""
        desc = deskripsi.value.strip()
        if not title:
            return
        tasks.append({"title": title, "done": False, "deadline": selected_deadline or "No deadline", "mata_kuliah": subject, "deskripsi": desc})
        save_tasks(tasks)
        task_title.value = ""
        mata_kuliah.value = SUBJECT_OPTIONS[0]
        deskripsi.value = ""
        selected_deadline = None
        deadline_display.value = "📅 No deadline"
        date_picker.value = None
        task_title.focus()
        build_task_ui()
        page.update()

    def toggle_task(index):
        if 0 <= index < len(tasks):
            tasks[index]["done"] = not tasks[index]["done"]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def delete_task(index):
        if 0 <= index < len(tasks):
            del tasks[index]
            save_tasks(tasks)
            build_task_ui()
            page.update()

    def on_date_selected(e):
        nonlocal selected_deadline
        if date_picker.value:
            selected_deadline = str(date_picker.value).split()[0]
            deadline_display.value = f"📅 {selected_deadline}"
        else:
            selected_deadline = None
            deadline_display.value = "📅 No deadline"
        page.update()

    def open_date_picker(e):
        page.open(date_picker)

    add_button.on_click = add_task
    date_picker.on_change = on_date_selected
    task_title.on_submit = add_task
    view_dropdown.on_change = lambda e: (build_task_ui(), page.update())

    build_task_ui()

    input_container = ft.Container(
        content=ft.Column([
            ft.Text("Add New Task", size=16, weight="bold", color=theme["text_primary"]),
            # Title full width on its own row
            task_title,
            # Subject full width on its own row
            mata_kuliah,
            deskripsi,
            ft.Row([ft.IconButton(icon=ft.Icons.CALENDAR_TODAY, icon_color=theme["primary"], on_click=open_date_picker), deadline_display, ft.Container(expand=True), add_button], alignment="spaceBetween", spacing=10, vertical_alignment="center"),
        ], spacing=12),
        padding=20,
        bgcolor=theme["surface"],
        border_radius=BORDER_RADIUS,
        margin=ft.margin.only(left=16, right=16, top=16, bottom=30),
        border=ft.border.all(1, theme["border"]),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=4, color="rgba(0, 0, 0, 0.08)", offset=ft.Offset(0, 2)),
    )

    # Task list container: header (Your Tasks + view selector) then boxed list
    header_row = ft.Row(
        [
            ft.Text("Your Tasks", size=16, weight="bold", color=theme["text_primary"]),
            ft.Container(expand=True),
            view_dropdown,
        ],
        alignment="center",
    )

    task_list_container = ft.Container(
        content=ft.Column([header_row, ft.Divider(height=1, color=theme["border"]), tasks_column]),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=theme["surface_alt"],
        border_radius=BORDER_RADIUS,
        margin=ft.margin.only(left=16, right=16, bottom=16),
    )

    handler_dict = {"add_task": add_task, "toggle_task": toggle_task, "delete_task": delete_task, "build_task_ui": build_task_ui, "tasks": tasks}

    return input_container, task_list_container, deadline_display, handler_dict
