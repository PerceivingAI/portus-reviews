"""
Global theme helpers and single entry‑point (`apply_theme`) that
returns a read‑only ThemeContext for easy token access.
"""
from __future__ import annotations
from dataclasses import dataclass
import flet as ft

from . import palette, metrics, typography

@dataclass(frozen=True)
class ThemeContext:
    colors:     object = palette
    metrics:    object = metrics
    typography: object = typography

def themed(**kw) -> dict:
    """Merge caller kwargs with Portus defaults (bg, fg, radius)."""
    return {
        "bgcolor":       kw.pop("bg", palette.COLOR_BG),
        "color":         kw.pop("fg", palette.COLOR_TEXT),
        "border_radius": kw.pop("radius", metrics.BORDER_RADIUS),
        **kw,
    }

def apply_theme(control) -> ThemeContext:
    """
    Apply global dark theme to a `ft.Page` (or any control with `.page`)
    and **return** a ThemeContext façade for downstream code.
    """
    page = control if isinstance(control, ft.Page) else control.page
    page.bgcolor = palette.COLOR_BG
    page.fonts = {}
    page.theme = ft.Theme()
    return ThemeContext()
