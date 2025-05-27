# portus_interface_gui_module/menu/dialog_help.py

import flet as ft
import portus_theme_module as pt
from portus_interface_gui_module.shortcuts.shortcuts import SHORTCUTS

def build_help_dialog() -> ft.AlertDialog:
    shortcut_items = [f"{k:<15} — {v}" for k, v in SHORTCUTS.items()]
    mid = (len(shortcut_items) + 1) // 2
    col1 = [ft.Text(s, size=pt.FONT_SIZE_LABEL, color=pt.COLOR_TEXT) for s in shortcut_items[:mid]]
    col2 = [ft.Text(s, size=pt.FONT_SIZE_LABEL, color=pt.COLOR_TEXT) for s in shortcut_items[mid:]]

    content = ft.Column(
        [
            ft.Text(
                "About",
                size=pt.FONT_SIZE_LABEL + 2,
                color=pt.COLOR_MAIN_ACCENT,
            ),
            ft.Text(
                "PortusReviews scrapes data, stores raw data, creates a clean Excel document "
                "\nwith the chosen columns, and uses that to generate replies and a sentiment "
                "\nanalysis report using OpenAI, Google, or xAI LLM models.",
                size=pt.FONT_SIZE_LABEL,
                color=pt.COLOR_TEXT,
            ),
            ft.Text(""),
            ft.Text(
                "Credits",
                size=pt.FONT_SIZE_LABEL + 2,
                color=pt.COLOR_MAIN_ACCENT,
            ),
            ft.Text(
                "Developed by PerceivingAI — All components are open-source."
                "\nhttps://x.com/PerceivingAI"
                "\n\nFlet is licensed under the Apache License, Version 2.0. See the LICENSE file for details. ",
                size=pt.FONT_SIZE_LABEL,
                color=pt.COLOR_TEXT,
            ),
            ft.Text(""),
            ft.Text(
                "Shortcuts",
                size=pt.FONT_SIZE_LABEL + 2,
                color=pt.COLOR_MAIN_ACCENT,
            ),
            ft.Row(
                [
                    ft.Column(col1, expand=True, spacing=2),
                    ft.Column(col2, expand=True, spacing=2),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True,
            ),
        ],
        tight=True,
        expand=False,
        height=450,
        spacing=10,
    )

    return ft.AlertDialog(
        title=ft.Text(
            "Help / Shortcuts",
            size=pt.FONT_SIZE_TITLE,
            color=pt.COLOR_MAIN_ACCENT
        ),
        content=content,
        modal=False,
        bgcolor=pt.COLOR_DARK_GREY,
        shape=ft.RoundedRectangleBorder(radius=pt.BORDER_RADIUS)
    )
