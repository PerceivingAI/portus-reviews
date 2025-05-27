# portus_theme_module\dialogs.py

import flet as ft

from .palette import (
    COLOR_TEXT,
    COLOR_DARK_GREY,
    COLOR_GREY,
    COLOR_RED,
    COLOR_TRANSPARENT,
    COLOR_HOVER_ALT,
)
from .metrics import BORDER_RADIUS
from .typography import FONT_SIZE_DEFAULT

def alert_dialog(
    title: str,
    on_confirm,
    on_cancel=None,
    confirm_label: str = "Delete",
    cancel_label: str = "Cancel",
) -> ft.AlertDialog:
    return ft.AlertDialog(
        title=ft.Text(
            title,
            color=COLOR_TEXT,
            size=22,
            weight=ft.FontWeight.W_500,
        ),
        bgcolor=COLOR_DARK_GREY,
        modal=False,
        barrier_color=None,
        shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
        elevation=8,
        content_padding=ft.Padding(20, 20, 20, 0),
        actions_padding=ft.Padding(20, 0, 20, 20),
        actions_alignment=ft.MainAxisAlignment.END,
        action_button_padding=ft.Padding(8, 0, 8, 0),
        inset_padding=ft.Padding(24, 40, 24, 40),
        actions=[
            ft.TextButton(
                cancel_label,
                width=75,
                height=45,
                style=ft.ButtonStyle(
                    color=COLOR_GREY,
                    bgcolor=COLOR_TRANSPARENT,
                    overlay_color=COLOR_HOVER_ALT,
                    shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
                    text_style=ft.TextStyle(size=FONT_SIZE_DEFAULT, weight=ft.FontWeight.W_400),
                ),
                on_click=on_cancel,
            ),
            ft.TextButton(
                confirm_label,
                width=75,
                height=45,
                style=ft.ButtonStyle(
                    color=COLOR_RED,
                    bgcolor=COLOR_TRANSPARENT,
                    overlay_color=COLOR_HOVER_ALT,
                    shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
                    text_style=ft.TextStyle(size=FONT_SIZE_DEFAULT, weight=ft.FontWeight.W_400),
                ),
                on_click=on_confirm,
            ),
        ],
    )

__all__ = ["alert_dialog"]
