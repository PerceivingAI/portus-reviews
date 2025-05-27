import flet as ft

from .palette import (
    COLOR_TEXT,
    COLOR_TRANSPARENT,
    COLOR_TAG,
    COLOR_SHADOW,
)
from .metrics import BORDER_RADIUS
from .buttons import text_button  # if wrappers need it elsewhere

def wrap_label(control: ft.Control, padding: int = 4) -> ft.Container:
    return ft.Container(
        content=control,
        padding=ft.Padding(padding, padding, padding, padding),
        alignment=ft.alignment.center_left,
    )

def file_tag_style(filename: str, on_remove) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Text(
                    filename,
                    size=12,
                    color=COLOR_TEXT,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    max_lines=1,
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.icons.CLOSE_SHARP,
                    icon_size=12,
                    icon_color=COLOR_TEXT,
                    tooltip="",
                    on_click=on_remove,
                    bgcolor=COLOR_TRANSPARENT,
                    height=24,
                    width=24,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
                        padding=ft.Padding(1, 1, 1, 1),
                    ),
                ),
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        ),
        bgcolor=COLOR_TAG,
        padding=ft.Padding(8, 0, 4, 0),
        border_radius=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
        height=24,
        width=150,
        shadow=ft.BoxShadow(
            color=COLOR_SHADOW,
            blur_radius=2,
            spread_radius=0,
            offset=ft.Offset(1, 1),
            blur_style=ft.ShadowBlurStyle.NORMAL,
        ),
    )

__all__ = ["wrap_label", "file_tag_style"]
