# portus_interface_gui_module\actions_row\job_toggles.py

import flet as ft
from portus_config_module.config_manager import reload_config, CONFIG
from portus_config_module.config_writer import update_yaml_value
import portus_theme_module as pt

JOBS_PATH = ["jobs"]

def build_job_toggles() -> list[ft.Container]:
    reload_config()
    job_states = CONFIG.get("jobs", {})

    def make_toggle(job_key: str, label: str) -> ft.Container:
        def on_toggle_job(e: ft.ControlEvent):
            update_yaml_value(JOBS_PATH + [job_key], e.control.value)

        return ft.Container(
            content=ft.Switch(
                label=label.title(),
                value=job_states.get(job_key, False),
                on_change=on_toggle_job,
                active_color=pt.COLOR_MAIN_ACCENT,
                track_outline_color=pt.COLOR_TRANSPARENT,
                label_style=ft.TextStyle(color=pt.COLOR_GREY, size=pt.FONT_SIZE_LABEL),
            ),
            alignment=ft.alignment.center_left,
            padding=0,
            bgcolor=pt.COLOR_TRANSPARENT,
            height=50,
            width=95,
        )

    return [
        make_toggle("scan",  "Scan"),
        make_toggle("clean", "Clean"),
        make_toggle("reply", "Reply"),
        make_toggle("sa",    "S_A"),
    ]
