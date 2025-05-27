# portus_interface_gui_module/display/display_builder.py

import flet as ft
from portus_interface_gui_module.display_area.display_tabs import build_system_tabs, build_user_tabs
import portus_theme_module as pt

def build_display() -> tuple[ft.Container, ft.TextField, ft.Row]:
    """
    Returns:
      • Container holding the display section (prompt + gallery)
      • The TextField for prompt input (for access by main_layout & shortcuts)
    """

    left_pane = ft.Container(
        content=build_user_tabs(),
        expand=6,
        height=1000,
        bgcolor=pt.COLOR_DARK_GREY,
        border_radius=pt.BORDER_RADIUS,
    )

    right_pane = ft.Container(
        content=build_system_tabs(),
        expand=4,
        height=1000,
        bgcolor=pt.COLOR_DARK_GREY,
        border_radius=pt.BORDER_RADIUS,
    )

    container = ft.Container(
        content=ft.Row(
            controls=[left_pane, right_pane],
            expand=True,
        ),
        padding=0,
        expand=True,
        bgcolor=pt.COLOR_TRANSPARENT,
        border_radius=pt.BORDER_RADIUS,
    )

    return container

