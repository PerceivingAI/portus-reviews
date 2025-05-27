# portus_interface_gui_module/top_bar/cutoff_date.py

import flet as ft
import re
from datetime import datetime
from portus_config_module.config_writer import update_yaml_value
from portus_config_module.config_manager import reload_config
import portus_theme_module as pt

# ── path to update in config.yaml ──
YAML_PATH_CUTOFF_DATE = ["scan_config", "scan_general_parameters", "cutoff_date"]

def build_cutoff_date() -> tuple[ft.Container, ft.TextField]:
    reload_config()
    from portus_config_module.config_manager import CONFIG
    cfg = CONFIG
    cfg_val = str(cfg.get("scan_config", {})
                    .get("scan_general_parameters", {})
                    .get("cutoff_date", "2024-12-31"))
    last_valid = {"val": cfg_val}
    today = datetime.today()

    date_input = ft.TextField(
        width=125,
        value=cfg_val,
        keyboard_type=ft.KeyboardType.TEXT,
        focused_border_color=pt.COLOR_MAIN_ACCENT,
        cursor_color=pt.COLOR_MAIN_ACCENT, 
        bgcolor=pt.COLOR_DARK_GREY,
        border_color=pt.COLOR_TRANSPARENT,
        border_radius=pt.BORDER_RADIUS,
        text_align="center",
        tooltip=pt.custom_tooltip("Input the Cutoff Date (Ctrl+D)"),
        text_style=ft.TextStyle(color=pt.COLOR_GREY),
    )

    def insert_dashes(s):
        # Returns: YYYY, YYYY-MM, YYYY-MM-DD
        if len(s) <= 4:
            return s
        elif len(s) <= 6:
            return f"{s[:4]}-{s[4:]}"
        else:
            return f"{s[:4]}-{s[4:6]}-{s[6:]}"

    def on_change(e: ft.ControlEvent):
        digits = e.control.value.replace("-", "").strip()

        # Allow clear
        if digits == "":
            e.control.value = ""
            e.control.update()
            return

        # Only digits, max 8
        if not digits.isdigit() or len(digits) > 8:
            e.control.value = last_valid["val"]
            e.control.update()
            return

        # Insert dashes as you type
        e.control.value = insert_dashes(digits)
        e.control.update()

    def on_blur(e: ft.ControlEvent):
        digits = e.control.value.replace("-", "").strip()
        # 8 digits: valid date
        if len(digits) == 8:
            year, month, day = digits[:4], digits[4:6], digits[6:]
            try:
                d = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
                if d > today or int(year) < 1990 or int(month) < 1 or int(month) > 12 or int(day) < 1 or int(day) > 31:
                    raise ValueError
                padded = f"{year}-{month}-{day}"
                last_valid["val"] = padded
                update_yaml_value(YAML_PATH_CUTOFF_DATE, padded)
                e.control.value = padded
            except Exception:
                e.control.value = last_valid["val"]
        # 7 digits: pad day with 0
        elif len(digits) == 7:
            year, month, day = digits[:4], digits[4:6], digits[6:]
            padded = f"{year}-{month}-0{day}"
            try:
                d = datetime.strptime(padded, "%Y-%m-%d")
                if d > today or int(year) < 1990 or int(month) < 1 or int(month) > 12 or int(day) < 1 or int(day) > 9:
                    raise ValueError
                last_valid["val"] = padded
                update_yaml_value(YAML_PATH_CUTOFF_DATE, padded)
                e.control.value = padded
            except Exception:
                e.control.value = last_valid["val"]
        # empty or other: revert to last valid
        else:
            e.control.value = last_valid["val"]
        e.control.update()

    date_input.on_change = on_change
    date_input.on_blur = on_blur

    row = ft.Row(
        [
            ft.Text("cutoff date:", size=pt.FONT_SIZE_DEFAULT, color=pt.COLOR_GREY),
            date_input,
            ft.Text("YYYY-MM-DD", size=pt.FONT_SIZE_DEFAULT, color=pt.COLOR_GREY),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    wrapped = ft.Container(
        content=row,
        alignment=ft.Alignment(0.0, 1.0),
        bgcolor=pt.COLOR_TRANSPARENT,
        border_radius=ft.RoundedRectangleBorder(radius=pt.BORDER_RADIUS),
        border=ft.Border(
            left=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
            top=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
            right=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
            bottom=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
        ),
        padding=ft.Padding(0, 0, 0, 0),
        margin=ft.Margin(0, 0, 0, 0),
        width=375,
        height=50,
        expand=False,
    )

    return wrapped, date_input
