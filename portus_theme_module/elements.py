import flet as ft
from .palette import (
    COLOR_TEXT,
    COLOR_DARK_GREY,
    COLOR_GREY,
    COLOR_RED,
    COLOR_TRANSPARENT,
    COLOR_HOVER_ALT,
    COLOR_MAIN_ACCENT,
    COLOR_BG,
    COLOR_HOVER,
)
from .metrics import BORDER_RADIUS
from .typography import FONT_SIZE_DEFAULT, FONT_SIZE_LABEL

def main_textfield(
    label: str,
    value: str = "",
    width: int = 300,
    height: int = 50,
    **kwargs
) -> ft.TextField:
    return ft.TextField(
        label=label,
        value=value,
        width=width,
        height=height,
        label_style=ft.TextStyle(color=COLOR_GREY),
        text_style=ft.TextStyle(color=COLOR_TEXT, size=FONT_SIZE_LABEL),
        cursor_color=COLOR_MAIN_ACCENT,
        bgcolor=COLOR_TRANSPARENT,
        border_color=COLOR_MAIN_ACCENT,
        border_radius=BORDER_RADIUS,
        text_align="left",
        content_padding=ft.Padding(8, 0, 8, 20),
        **kwargs
    )

def expand_width_textfield(
    label: str,
    value: str = "",
    height: int = 50,
    **kwargs
) -> ft.TextField:
    return ft.TextField(
        label=label,
        value=value,
        expand=True,
        height=height,
        label_style=ft.TextStyle(color=COLOR_GREY),
        text_style=ft.TextStyle(color=COLOR_TEXT, size=FONT_SIZE_LABEL),
        cursor_color=COLOR_MAIN_ACCENT,
        bgcolor=COLOR_TRANSPARENT,
        border_color=COLOR_MAIN_ACCENT,
        border_radius=BORDER_RADIUS,
        text_align="left",
        content_padding=ft.Padding(8, 0, 8, 20),
        **kwargs
    )

def custom_tooltip(message: str) -> ft.Tooltip:
    return ft.Tooltip(
        message=message,
        bgcolor=COLOR_BG,
        padding=ft.Padding(12, 8, 12, 8),
        border_radius=BORDER_RADIUS,
        text_style=ft.TextStyle(size=FONT_SIZE_LABEL, color=COLOR_GREY),
        text_align=ft.TextAlign.LEFT,
        margin=10,
        prefer_below=True,
        wait_duration=300,
        show_duration=2000,
        exit_duration=200,
        enable_feedback=True,
        enable_tap_to_dismiss=True,
        exclude_from_semantics=False,
        vertical_offset=10,
    )

def custom_button_tooltip(message: str) -> ft.Tooltip:
    return ft.Tooltip(
        message=message,
        bgcolor=COLOR_BG,
        padding=ft.Padding(12, 8, 12, 8),
        border_radius=BORDER_RADIUS,
        text_style=ft.TextStyle(size=FONT_SIZE_LABEL, color=COLOR_GREY),
        text_align=ft.TextAlign.LEFT,
        margin=10,
        prefer_below=True,
        wait_duration=300,
        show_duration=2000,
        exit_duration=200,
        enable_feedback=True,
        enable_tap_to_dismiss=True,
        exclude_from_semantics=False,
        vertical_offset=20,
    )

def custom_tab(tabs: list[ft.Tab], selected_index: int = 0) -> ft.Tabs:
    return ft.Tabs(
        selected_index=selected_index,
        animation_duration=300,
        tabs=tabs,
        divider_height=0,
        expand=1,
        indicator_color=COLOR_MAIN_ACCENT,
        indicator_thickness=5.0,
        indicator_padding=3,
        indicator_tab_size=20,
        label_color=COLOR_MAIN_ACCENT,
        label_text_style=ft.TextStyle(
            size=FONT_SIZE_DEFAULT,
            weight=ft.FontWeight.W_600,
        ),
        unselected_label_color=COLOR_GREY,
        unselected_label_text_style=ft.TextStyle(
            size=FONT_SIZE_DEFAULT,
            weight=ft.FontWeight.W_600,
        ),
    )

def custom_tab_container(text: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(text, color=COLOR_GREY, size=FONT_SIZE_DEFAULT),
        bgcolor=COLOR_TRANSPARENT,
        alignment=ft.alignment.top_left,
        expand=True,
        border_radius=BORDER_RADIUS,
        padding=ft.Padding(15, 10, 15, 10),
    )