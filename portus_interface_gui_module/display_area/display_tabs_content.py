# portus_interface_gui_module/display_area/display_tabs_content.py

"""
Dynamic builder for user‑N prompt & hotel editor tabs.
Call build_user_content(idx) where idx is 1‑based (1…8).
Returns:
  • Container with all controls
  • reload_fields() callback to refresh from YAML
"""

import time, threading
import flet as ft

from portus_config_module.config_manager import load
from portus_config_module.config_writer import update_yaml_value
import portus_theme_module as pt

def build_user_content(idx: int) -> tuple[ft.Container, callable]:
    prompt_key = f"prompt_{idx}"
    hotel_key  = f"hotel_{idx}"

    cfg = load()
    hotel_name = cfg["hotel_url_bank"][hotel_key][f"{hotel_key}_name"]
    prompt_txt = cfg["user_prompt_bank"][prompt_key]
    ta_url     = cfg["hotel_url_bank"][hotel_key]["tripadvisor"]
    go_url     = cfg["hotel_url_bank"][hotel_key]["google"]
    bk_url     = cfg["hotel_url_bank"][hotel_key]["booking"]
    ex_url     = cfg["hotel_url_bank"][hotel_key]["expedia"]

    prompt_box = ft.TextField(
        value=prompt_txt,
        multiline=True,
        expand=True,
        min_lines=20,
        bgcolor=pt.COLOR_TRANSPARENT,
        border_color=pt.COLOR_MAIN_ACCENT,
        border_radius=pt.BORDER_RADIUS,
        cursor_color=pt.COLOR_MAIN_ACCENT,
        label=f"Prompt {idx}",
        label_style=ft.TextStyle(color=pt.COLOR_GREY),
        text_style=ft.TextStyle(color=pt.COLOR_GREY),
    )

    name_box = pt.expand_width_textfield(label="Hotel/Restaurant Name", value=hotel_name)
    ta_box   = pt.expand_width_textfield(label="Tripadvisor URL", value=ta_url)
    go_box   = pt.expand_width_textfield(label="Google URL",      value=go_url)
    bk_box   = pt.expand_width_textfield(label="Booking URL",     value=bk_url)
    ex_box   = pt.expand_width_textfield(label="Expedia URL",     value=ex_url)

    save_btn = pt.elevated_main_button(
        text="Save",
        height=40,
        width=100,
        text_style=ft.TextStyle(
            color=pt.COLOR_BG,
            size=pt.FONT_SIZE_DEFAULT,
            weight=ft.FontWeight.W_600,
        ),
    )

    def save(_):
        save_btn.text = "✓"
        save_btn.update()

        update_yaml_value(["user_prompt_bank", prompt_key], prompt_box.value.strip())
        update_yaml_value(
            ["hotel_url_bank", hotel_key, f"{hotel_key}_name"],
            name_box.value.strip(),
        )
        update_yaml_value(
            ["hotel_url_bank", hotel_key, "tripadvisor"], ta_box.value.strip()
        )
        update_yaml_value(
            ["hotel_url_bank", hotel_key, "google"], go_box.value.strip()
        )
        update_yaml_value(
            ["hotel_url_bank", hotel_key, "booking"], bk_box.value.strip()
        )
        update_yaml_value(
            ["hotel_url_bank", hotel_key, "expedia"], ex_box.value.strip()
        )
        update_yaml_value(["user_prompt_bank", "selected_prompt"], prompt_key)
        update_yaml_value(["hotel_url_bank", "selected_hotel"], hotel_key)

        def _revert():
            time.sleep(0.6)
            save_btn.text = "Save"
            save_btn.update()

        threading.Thread(target=_revert, daemon=True).start()

    save_btn.on_click = save

    body = ft.Column(
        [
            ft.Row([name_box, save_btn], spacing=10),
            prompt_box,
            ft.Row([ta_box, bk_box], spacing=10),
            ft.Row([go_box, ex_box], spacing=10),
            ft.Container(height=10),
        ],
        spacing=12,
        expand=True,
    )

    user_container = ft.Container(
        content=body,
        bgcolor=pt.COLOR_TRANSPARENT,
        alignment=ft.alignment.top_left,
        expand=True,
        padding=ft.Padding(15, 20, 15, 0),
        border_radius=pt.BORDER_RADIUS,
    )

    def reload_fields():
        cfg = load()
        prompt_box.value = cfg["user_prompt_bank"][prompt_key]
        name_box.value   = cfg["hotel_url_bank"][hotel_key][f"{hotel_key}_name"]
        ta_box.value     = cfg["hotel_url_bank"][hotel_key]["tripadvisor"]
        go_url_new       = cfg["hotel_url_bank"][hotel_key]["google"]
        bk_url_new       = cfg["hotel_url_bank"][hotel_key]["booking"]
        ex_url_new       = cfg["hotel_url_bank"][hotel_key]["expedia"]
        go_box.value, bk_box.value, ex_box.value = go_url_new, bk_url_new, ex_url_new
        prompt_box.update()
        name_box.update()
        ta_box.update()
        go_box.update()
        bk_box.update()
        ex_box.update()

    return user_container, reload_fields

def build_system_content(key: str, label: str) -> tuple[ft.Container, callable]:
    """
    key   : string like 'sys_prompt_a'
    label : string shown on the Tab, e.g. 'System A'
    """
    cfg = load()
    sys_text = cfg["model_parameters"]["system_prompt_bank"].get(key, "")

    sys_box = ft.TextField(
        value=sys_text,
        multiline=True,
        expand=True,
        min_lines=25,
        bgcolor=pt.COLOR_TRANSPARENT,
        border_color=pt.COLOR_MAIN_ACCENT,
        border_radius=pt.BORDER_RADIUS,
        cursor_color=pt.COLOR_MAIN_ACCENT,
        label=label,
        label_style=ft.TextStyle(color=pt.COLOR_GREY),
        text_style=ft.TextStyle(color=pt.COLOR_GREY),
    )

    save_btn = pt.elevated_main_button(
        text="Save",
        height=40,
        width=100,
        text_style=ft.TextStyle(
            color=pt.COLOR_BG,
            size=pt.FONT_SIZE_DEFAULT,
            weight=ft.FontWeight.W_600,
        ),
    )

    def save(_):
        save_btn.text = "✓"; save_btn.update()

        update_yaml_value(
            ["model_parameters", "system_prompt_bank", key],
            sys_box.value.strip(),
        )
        update_yaml_value(
            ["model_parameters", "system_prompt_bank", "selected_system_prompt"],
            key,
        )

        def _revert():
            time.sleep(0.6)
            save_btn.text = "Save"
            save_btn.update()

        threading.Thread(target=_revert, daemon=True).start()

    save_btn.on_click = save

    body = ft.Column(
        [ft.Row([ft.Container(expand=True), save_btn]), sys_box],
        spacing=17,
        expand=True,
    )

    container = ft.Container(
        content=body,
        bgcolor=pt.COLOR_TRANSPARENT,
        alignment=ft.alignment.top_left,
        expand=True,
        padding=ft.Padding(15, 25, 15, 24),
        border_radius=pt.BORDER_RADIUS,
    )

    def reload_fields():
        cfg = load()
        sys_box.value = cfg["model_parameters"]["system_prompt_bank"].get(key, "")
        sys_box.update()

    return container, reload_fields