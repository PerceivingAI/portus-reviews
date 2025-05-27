# portus_theme_module\buttons.py

import flet as ft

from .palette import (
    COLOR_MAIN_ACCENT,
    COLOR_GREY,
    COLOR_DARK_GREY,
    COLOR_BG,
    COLOR_HOVER_MAIN,
    COLOR_HOVER_ALT,
    COLOR_HOVER_T,
    COLOR_TRANSPARENT,
)
from .metrics import (
    BORDER_RADIUS,
    ICON_MAIN_SIZE,
    ICON_SMALL_SIZE,
    ICON_MID_SIZE,
)

# ───── base helper ─────────────────────────────────────────────────────
def _icon_button_style(*, icon_size: int, **kw) -> dict:
    return {
        "icon_size": icon_size,
        "style": ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
            bgcolor={
                ft.ControlState.HOVERED: COLOR_HOVER_MAIN,
                ft.ControlState.DEFAULT: COLOR_TRANSPARENT,
            },
            padding=ft.Padding(8, 8, 8, 8),
        ),
        **kw,
    }

# ───── public builders ─────────────────────────────────────────────────
def icon_main_button(**kw) -> dict:
    return _icon_button_style(icon_size=ICON_MAIN_SIZE, **kw)

def icon_sec_button(**kw) -> dict:
    return _icon_button_style(icon_size=ICON_SMALL_SIZE, **kw)

def pop_menu_button(**kw) -> dict:
    return {
        "icon_color": COLOR_GREY,
        "icon_size": ICON_MID_SIZE,
        "bgcolor": COLOR_BG,
        "style": ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
            bgcolor={
                ft.ControlState.HOVERED: COLOR_HOVER_T,
                ft.ControlState.DEFAULT: COLOR_TRANSPARENT,
            },
        ),
        **kw,
    }

def pop_menu_button_sec(**kw) -> dict:
    return {
        "icon_color": COLOR_MAIN_ACCENT,
        "icon_size": ICON_SMALL_SIZE,
        "bgcolor": COLOR_BG,
        "style": ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
            bgcolor={
                ft.ControlState.HOVERED: COLOR_HOVER_ALT,
                ft.ControlState.DEFAULT: COLOR_TRANSPARENT,
            },
        ),
        **kw,
    }

def floating_main_button(*, icon_name: str, tooltip: str, on_click, icon_size: int = ICON_MAIN_SIZE, **kw) -> dict:
    return {
        "content": ft.Icon(name=icon_name, size=icon_size),
        "tooltip": tooltip,
        "height": 42,
        "width": 42,
        "bgcolor": COLOR_MAIN_ACCENT,
        "focus_color": COLOR_HOVER_MAIN,
        "foreground_color": COLOR_MAIN_ACCENT,
        "elevation": 0,
        "highlight_elevation": 0,
        "hover_elevation": 0,
        "disabled_elevation": 0,
        "focus_elevation": 0,
        "shape": ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
        "on_click": on_click,
        **kw,
    }

def text_button(**kwargs) -> ft.ButtonStyle:
    return ft.ButtonStyle(
        bgcolor=pt.COLOR_MAIN_BUTTON,
        color=COLOR_BG,
        shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS),
        text_style=ft.TextStyle(weight=ft.FontWeight.W_600),
        overlay_color={
            ft.ControlState.HOVERED: COLOR_MAIN_ACCENT,
            ft.ControlState.FOCUSED: COLOR_TRANSPARENT,
            ft.ControlState.DEFAULT: COLOR_TRANSPARENT,
        },
        **kwargs
    )

import flet as ft
import portus_theme_module.palette as pt
import portus_theme_module.typography as typo
import portus_theme_module.metrics as metrics

def elevated_main_button(
    text: str = "Submit",
    icon: str | None = None,
    tooltip: str | None = None,
    on_click=None,
    width: int | None = None,
    height: int | None = None,
    expand: bool = False,
    **kw
) -> ft.ElevatedButton:
    """
    Returns a standardized ElevatedButton with consistent Portus styling.
    You can override any kwarg as needed (e.g. style, content, etc.).
    """
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        tooltip=tooltip,
        on_click=on_click,
        expand=expand,
        width=width,
        height=height,
        bgcolor=pt.COLOR_MAIN_BUTTON,
        color=pt.COLOR_BG,
        icon_color=pt.COLOR_TEXT,
        elevation=2,
        style=ft.ButtonStyle(
            padding=ft.Padding(14, 10, 14, 10),
            shape=ft.RoundedRectangleBorder(radius=metrics.BORDER_RADIUS),
            text_style=kw.pop("text_style", None),
            overlay_color={
                ft.ControlState.HOVERED: pt.COLOR_MAIN_ACCENT,
                ft.ControlState.FOCUSED: pt.COLOR_TRANSPARENT,
                ft.ControlState.DEFAULT: pt.COLOR_TRANSPARENT,
            },
        ),
        **kw,
    )

__all__ = [n for n in globals() if n.startswith(("icon_", "pop_", "floating_", "text_button_style", "elevated_main_button",))]
