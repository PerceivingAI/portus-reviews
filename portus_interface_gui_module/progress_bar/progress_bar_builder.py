# portus_interface_gui_module/progress_bar/progress_bar_builder.py

import flet as ft
import portus_theme_module as pt

def build_progress_container() -> tuple[ft.Container, ft.ProgressBar]:
    """
    Returns a container wrapping an indeterminate horizontal progress bar.
    The container is fixed height and full width. Bar is initially hidden.
    """
    progress_bar = ft.ProgressBar(
        width=float("inf"),
        color=pt.COLOR_MAIN_ACCENT,
        bgcolor=pt.COLOR_TRANSPARENT,
        visible=False,
    )

    container = ft.Container(
        content=progress_bar,
        height=5,
        expand=False,
    )

    return container, progress_bar
