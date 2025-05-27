# portus_theme_module/__init__.py

"""
Unified entry‑point for Portus theme utilities.

Usage:
    import portus_theme_module as pt

    pt.apply_theme(page)
    my_button = ft.IconButton(**pt.icon_main_button())
    color     = pt.palette.COLOR_MAIN_ACCENT
"""
from portus_theme_module.palette import *                    # colors & aliases
from portus_theme_module.metrics import *                    # sizes & radii
from portus_theme_module.typography import *                 # fonts
from portus_theme_module.elements import *

from portus_theme_module.theme import apply_theme, themed, ThemeContext

from portus_theme_module.buttons import (
    icon_main_button,
    icon_sec_button,
    pop_menu_button,
    pop_menu_button_sec,
    floating_main_button,
    text_button,
    elevated_main_button,
)

from portus_theme_module.dialogs import alert_dialog
from portus_theme_module.containers import wrap_label, file_tag_style

# Re‑export sub‑modules for direct access if desired
import importlib
palette   = importlib.import_module(__name__ + ".palette")
metrics   = importlib.import_module(__name__ + ".metrics")
typography = importlib.import_module(__name__ + ".typography")

__all__ = [
    # core helpers
    "apply_theme",
    "themed",
    "ThemeContext",
    # style builders
    "icon_main_button",
    "icon_sec_button",
    "pop_menu_button",
    "pop_menu_button_sec",
    "floating_main_button",
    "text_button",
    "alert_dialog",
    "wrap_label",
    "file_tag_style",
    "main_textfield",
    "width_textfield",
    "custom_tooltip",
    "custom_button_tooltip",
    "custom_tab",
    "custom_tab_container"
    # direct access to tokens
    "palette",
    "metrics",
    "typography",
]
