# portus_interface_gui_module/main_layout.py

import flet as ft
from pathlib import Path

from portus_interface_gui_module.shortcuts.shortcuts import attach_shortcuts
from portus_interface_gui_module.menu.dialog_builder import build_dialogs
from portus_interface_gui_module.top_bar.top_bar_builder import build_top_bar
from portus_interface_gui_module.actions_row.actions_row_builder import build_actions_row
from portus_interface_gui_module.display_area.display_builder import build_display
from portus_interface_gui_module.progress_bar.progress_bar_builder import build_progress_container
from portus_interface_gui_module.actions_row.generate_alerts import build_alerts
import portus_theme_module as pt

def main_view(page: ft.Page):
    page.title = "PortusReviews"
    ctx = pt.apply_theme(page)
    #page.theme_mode = ft.ThemeMode.DARK
    page.window_focused = True

    # Set initial window size and make it resizable
    page.window.width = pt.DEFAULT_WINDOW_WIDTH
    page.window.height = pt.DEFAULT_WINDOW_HEIGHT
    page.window.min_width = pt.MIN_WINDOW_WIDTH
    page.window.min_height = pt.MIN_WINDOW_HEIGHT
    page.window.resizable = True
    page.window.center()
    page.update()

    # ── Dialogs ──────────────────────────────────────────────────────
    dlg_help = build_dialogs()
    dlg_result, snack, dlg_message = build_alerts(page)
    page.overlay.extend([dlg_help])


    # ── Top bar ──────────────────────────────────────────────────────
    topbar, main_row, sec_row, num_input, date_input, out_path_text, btn_folder, folder_picker, provider_menu_button, provider_label = build_top_bar(page, dlg_help)

    # ── Display box (prompt container) ───────────────────────────────
    display_ctr = build_display()

    # ── Progress bar ─────────────────────────────────────────────────
    progress_ctr, progress_bar = build_progress_container()

    # ── Actions row ──────────────────────────────────────────────────
    actions_row, action_controls = build_actions_row(page, progress_bar, dlg_result, snack, dlg_message)

    # ── Shortcut‑aware widget map ────────────────────────────────────
    widgets = {
        **action_controls,
        "btn_generate": action_controls["btn_generate"],
        #"btn_all_in":   action_controls["btn_all_in"],
        "btn_folder": btn_folder,
        "num_input": num_input,
        "date_input": date_input,
        "dialog_help": dlg_help,
        "provider_menu": provider_menu_button,
        "provider_label": provider_label,
    }
    attach_shortcuts(page, widgets)

    # ── Final assembly ───────────────────────────────────────────────
    page.add(
        ft.Column(
            controls=[
                topbar,
                display_ctr,
                progress_ctr,
                ft.Container(height=10),
                actions_row,
                ft.Container(height=40),
            ],
            expand=True,
            spacing=10,
        )
    )