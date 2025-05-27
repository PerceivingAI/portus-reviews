# portus_interface_gui_module/actions_row/site_toggles.py

import flet as ft
from portus_config_module.config_manager import reload_config, CONFIG
from portus_config_module.config_writer import update_yaml_value
import portus_theme_module as pt

REVIEW_SITES_PATH = ["review_sites"]

def build_site_toggles() -> list[ft.Container]:
    reload_config()
    site_states = CONFIG.get("review_sites", {})

    def make_toggle(site_key: str, label: str) -> ft.Container:
        def on_toggle_site(e: ft.ControlEvent):
            update_yaml_value(REVIEW_SITES_PATH + [site_key], e.control.value)

        return ft.Container(
            content=ft.Switch(
                label=label.upper(),
                value=site_states.get(site_key, False),
                on_change=on_toggle_site,
                active_color=pt.COLOR_MAIN_ACCENT,
                track_outline_color=pt.COLOR_TRANSPARENT,
                label_style=ft.TextStyle(color=pt.COLOR_GREY, size=pt.FONT_SIZE_LABEL),
            ),
            alignment=ft.alignment.center_left,
            padding=0,
            bgcolor=pt.COLOR_TRANSPARENT,
            #bgcolor='red',
            height=50,
            width=95,
        )

    return [
        make_toggle("tripadvisor", "TA"),
        make_toggle("google", "GO"),
        make_toggle("booking", "BK"),
        make_toggle("expedia", "EX"),
    ]
