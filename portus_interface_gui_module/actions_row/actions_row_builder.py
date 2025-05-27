# portus_interface_gui_module/actions_row/actions_row_builder.py

import flet as ft
from .generate_button import build_generate_button
from .all_in_button   import build_all_in_button
from .site_toggles  import build_site_toggles
from .job_toggles import build_job_toggles

def build_actions_row(
    page: ft.Page,
    progress_bar: ft.ProgressBar,
    dlg_result: ft.AlertDialog,
    snack: ft.SnackBar,
    dlg_message,
) -> tuple[ft.Row, dict]:
    """
    Build the full actions row and return:
      • the Row ready to add to the page
      • a dict of its child controls for shortcut access
    """
    site_toggles = build_site_toggles()
    job_toggles = build_job_toggles()

    btn_generate = None
    btn_all_in = None

    btn_generate = build_generate_button(
        page, progress_bar, dlg_result, snack, dlg_message,
        get_other_button=lambda: btn_all_in
    )

    btn_all_in = build_all_in_button(
        page, progress_bar, dlg_result, snack, dlg_message,
        get_other_button=lambda: btn_generate
    )

    sites = ft.Row([ft.Container(width=0), *site_toggles], spacing=5)
    jobs = ft.Row([ft.Container(width=0), *job_toggles], spacing=5)

    buttons = ft.Row([btn_all_in, btn_generate], spacing=10)

    row = ft.Row(
        [ft.Container(width=0), sites, ft.Container(expand=True), jobs, ft.Container(expand=True), buttons, ft.Container(width=7)],
        alignment=ft.MainAxisAlignment.START,
    )

    controls = {
        "btn_generate": btn_generate,
        "btn_all_in":   btn_all_in,
    }
    return row, controls
