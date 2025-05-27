# portus_interface_gui_module/top_bar/review_number.py

import flet as ft
from portus_config_module.config_writer import update_yaml_value
from portus_config_module.config_manager import reload_config
import portus_theme_module as pt

# ── path to update in config.yaml ──
YAML_PATH_REVIEW_NUMBER = ["scan_config", "scan_general_parameters", "review_number"]

ALLOWED_VALUES = [str(i) for i in range(1, 701)]

def build_review_number() -> tuple[ft.Container, ft.TextField]:
    """Returns the review count row wrapped in a container and the input box for shortcut access."""
    reload_config()
    from portus_config_module.config_manager import CONFIG
    cfg = CONFIG
    cfg_val = str(cfg.get("scan_config", {})
                    .get("scan_general_parameters", {})
                    .get("review_number", 1))
    last_valid = {"val": cfg_val}
    
    num_input = ft.TextField(
        width=55,
        value=cfg_val,
        keyboard_type=ft.KeyboardType.NUMBER,
        focused_border_color=pt.COLOR_MAIN_ACCENT,
        cursor_color=pt.COLOR_MAIN_ACCENT, 
        bgcolor=pt.COLOR_DARK_GREY,
        border_color=pt.COLOR_TRANSPARENT,
        #hover_color=pt.COLOR_TRANSPARENT,
        border_radius=pt.BORDER_RADIUS,
        text_align="center",
        tooltip=pt.custom_tooltip("Input the Number of Reviews (Ctrl+N)"),
        text_style=ft.TextStyle(color=pt.COLOR_GREY),
    )

    def on_change(e: ft.ControlEvent):
        v = e.control.value.strip()
        if v == "":
            return
        if not v.isdigit() or v not in ALLOWED_VALUES:
            e.control.value = last_valid["val"]
        else:
            last_valid["val"] = v
            update_yaml_value(YAML_PATH_REVIEW_NUMBER, int(v))
        e.control.update()

    def on_blur(e: ft.ControlEvent):
        if e.control.value.strip() == "":
            e.control.value = "1"
            last_valid["val"] = "1"
            update_yaml_value(YAML_PATH_REVIEW_NUMBER, 1)
            e.control.update()

    num_input.on_change = on_change
    num_input.on_blur = on_blur

    row = ft.Row(
        [
            ft.Text("# of reviews:", size=pt.FONT_SIZE_DEFAULT, color=pt.COLOR_GREY),
            num_input,
            ft.Text("1–700", size=pt.FONT_SIZE_DEFAULT, color=pt.COLOR_GREY),
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
        width=250,
        height=50,
        expand=False,
    )

    return wrapped, num_input
