# portus_interface_gui_module/top_bar/output_folder.py

import flet as ft
from pathlib import Path
from portus_config_module.config_manager import get_writer_output_folder, set_output_folder, CONFIG
import portus_theme_module as pt

def build_output_folder_row(page: ft.Page) -> tuple[ft.Container, ft.Text, ft.IconButton, ft.FilePicker]:
    """Builds the output folder row wrapped in a container. Returns the container, text, button, and picker."""

    raw = CONFIG["writer_config"].get("output_folder", "").strip()
    current_path = raw if raw else ""

    default_message = "Select an output folder or leave empty to default to Downloads"

    out_path_text = ft.Text(
        current_path if current_path else default_message,
        overflow=ft.TextOverflow.ELLIPSIS,
        expand=True,
        color=pt.COLOR_GREY,
        size=pt.FONT_SIZE_DEFAULT,
    )

    def result_handler(e: ft.FilePickerResultEvent):
        if e.path:
            set_output_folder(e.path)
            out_path_text.value = e.path
        else:
            out_path_text.value = default_message
        out_path_text.update()

    folder_picker = ft.FilePicker(on_result=result_handler)
    page.overlay.append(folder_picker)

    btn_folder = ft.IconButton(
        icon=ft.Icons.FOLDER_OPEN,
        tooltip=pt.custom_tooltip("Pick the Output Folder (Ctrl+O)"),
        on_click=lambda e: folder_picker.get_directory_path(),
        icon_color=pt.COLOR_MAIN_ACCENT,
        **pt.icon_sec_button(),
    )

    folder_row = ft.Row(
        [btn_folder, out_path_text],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    wrapped = ft.Container(
        content=folder_row,
        alignment=ft.Alignment(0.0, 1.0),
        bgcolor=pt.COLOR_TRANSPARENT,
        #bgcolor='red',
        border_radius=ft.RoundedRectangleBorder(radius=pt.BORDER_RADIUS),
        border=ft.Border(
            left=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
            top=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
            right=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
            bottom=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
        ),
        padding=ft.Padding(0, 0, 0, 0),
        margin=ft.Margin(0, 0, 0, 0),
        width=700,
        height=50,
        expand=False,
    )

    return wrapped, out_path_text, btn_folder, folder_picker
