# portus_interface_gui_module/menu/dialog_settings.py

import time
import threading
import flet as ft

from portus_config_module.config_manager import load, TEMPERATURE, MAX_OUTPUT_TOKENS, TOP_P, STREAM, XAI_ADD_PARAMS
from portus_config_module.config_writer import update_yaml_value
import portus_theme_module as pt

def build_general_parameters_container() -> tuple[ft.Container, ft.Slider, ft.Slider, ft.Switch, ft.TextField]:
    temperature = ft.Slider(
        min=0, max=1, divisions=10,
        value=TEMPERATURE,
        label=str(round(TEMPERATURE, 1)),
        active_color=pt.COLOR_MAIN_ACCENT,
        tooltip="Temperature (0–1)",
        width=200
    )

    def on_change_temp(e):
        e.control.label = str(round(e.control.value, 1))
        e.control.update()

    temperature.on_change = on_change_temp

    top_p = ft.Slider(
        min=0, max=1, divisions=10,
        value=TOP_P,
        label=str(round(TOP_P, 1)),
        active_color=pt.COLOR_MAIN_ACCENT,
        tooltip="Top‑P (0–1)",
        width=200
    )

    def on_change_top_p(e):
        e.control.label = str(round(e.control.value, 1))
        e.control.update()

    top_p.on_change = on_change_top_p

    stream = ft.Switch(
        value=STREAM or False,
        active_color=pt.COLOR_MAIN_ACCENT,
        track_outline_color=pt.COLOR_TRANSPARENT,
    )

    max_tokens = pt.main_textfield(
        label="Max Output Tokens",
        value=str(MAX_OUTPUT_TOKENS),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^([1-9]\d{0,5}|1000000)?$",
            replacement_string=""
        )
    )

    layout = ft.Column(
        controls=[
            ft.Row(
                [
                    ft.Text("Temperature", size=pt.FONT_SIZE_DEFAULT, color=pt.COLOR_GREY, width=110),
                    temperature
                ],
                vertical_alignment="center"
            ),
            ft.Row(
                [
                    ft.Text("Top P", size=pt.FONT_SIZE_DEFAULT, color=pt.COLOR_GREY, width=110),
                    top_p
                ],
                vertical_alignment="center"
            ),
            ft.Container(

            ),
            ft.Row(
                [
                    ft.Text("Stream", size=pt.FONT_SIZE_DEFAULT, color=pt.COLOR_GREY, width=110), ft.Container(width=9),
                    stream
                ],
                vertical_alignment="start"
            ),
            ft.Container(
                height=24
            ),
            max_tokens
        ],
        spacing=10,
        tight=True
    )

    container = ft.Container(content=layout, padding=0)
    return container, temperature, top_p, stream, max_tokens

def build_xai_additional_container() -> tuple[ft.Container, ft.Dropdown]:
    reasoning_effort = ft.Dropdown(
        value=XAI_ADD_PARAMS["reasoning_effort"],
        border_color=pt.COLOR_MAIN_ACCENT,
        border_radius=pt.BORDER_RADIUS,
        bgcolor=pt.COLOR_BG,
        options=[
            ft.dropdown.Option("low"),
            ft.dropdown.Option("mid"),
            ft.dropdown.Option("high")
        ],
        text_style=ft.TextStyle(color=pt.COLOR_GREY),
        width=180
    )

    layout = ft.Column(
        controls=[
            ft.Row(
                [
                    ft.Text("Reasoning", size=pt.FONT_SIZE_DEFAULT, color=pt.COLOR_GREY, width=110),
                    reasoning_effort
                ],
                vertical_alignment="center"
            )
        ],
        spacing=10,
        tight=True
    )

    container = ft.Container(content=layout, padding=0)
    return container, reasoning_effort

def build_settings_dialog() -> ft.AlertDialog:
    cfg = load()

    # ── Input fields ────────────────────────────────────────────────
    openai_model   = pt.main_textfield(label="OpenAI Model ID", value=cfg["mode"]["api"]["openai"]["model"])
    openai_url     = pt.main_textfield(label="OpenAI Base URL", value=cfg["mode"]["api"]["openai"]["base_url"])
    google_model   = pt.main_textfield(label="Google Model ID", value=cfg["mode"]["api"]["google"]["model"])
    google_url     = pt.main_textfield(label="Google Base URL", value=cfg["mode"]["api"]["google"]["base_url"])
    xai_model      = pt.main_textfield(label="xAI Model ID", value=cfg["mode"]["api"]["xai"]["model"])
    xai_url        = pt.main_textfield(label="xAI Base URL", value=cfg["mode"]["api"]["xai"]["base_url"])

    gp_container, temperature, top_p, stream, max_tokens = build_general_parameters_container()
    xai_container, reasoning_effort = build_xai_additional_container()

    # ── Save‑button with tick feedback ──────────────────────────────
    save_btn = pt.elevated_main_button(
        text="Save All",
        height=40,
        width=100,
        text_style=ft.TextStyle(color=pt.COLOR_BG, size=pt.FONT_SIZE_DEFAULT, weight=ft.FontWeight.W_600)
    )

    def save_all(_):
        save_btn.text = "✓"
        save_btn.update()

        # Model settings
        update_yaml_value(["mode", "api", "openai", "model"], openai_model.value.strip())
        update_yaml_value(["mode", "api", "openai", "base_url"], openai_url.value.strip())
        update_yaml_value(["mode", "api", "google", "model"], google_model.value.strip())
        update_yaml_value(["mode", "api", "google", "base_url"], google_url.value.strip())
        update_yaml_value(["mode", "api", "xai", "model"], xai_model.value.strip())
        update_yaml_value(["mode", "api", "xai", "base_url"], xai_url.value.strip())

        # General Parameters
        update_yaml_value(["model_parameters", "general_parameters", "temperature"], round(temperature.value, 2))
        update_yaml_value(["model_parameters", "general_parameters", "top_p"], round(top_p.value, 2))
        update_yaml_value(["model_parameters", "general_parameters", "stream"], stream.value)
        update_yaml_value(["model_parameters", "general_parameters", "max_output_tokens"], int(max_tokens.value))

        # xAI Additional
        update_yaml_value(["model_parameters", "xai_additional", "reasoning_effort"], reasoning_effort.value)

        def _revert():
            time.sleep(0.6)
            save_btn.icon = None
            save_btn.text = "Save All"
            save_btn.update()

        threading.Thread(target=_revert, daemon=True).start()

    save_btn.on_click = save_all


    # ── Assemble dialog ─────────────────────────────────────────────
    model_column = ft.Container(
        content=ft.Column(
            [
                ft.Text("Model Settings", weight="bold", color=pt.COLOR_GREY),
                ft.Text("OpenAI", weight="bold", color=pt.COLOR_TEXT), openai_model, openai_url,
                ft.Text("Google", weight="bold", color=pt.COLOR_TEXT), google_model, google_url,
                ft.Text("xAI", weight="bold", color=pt.COLOR_TEXT), xai_model, xai_url,
            ],
            spacing=10, tight=True
        ),
        padding=10,
    )

    param_column = ft.Container(
        content=ft.Column(
            [
                ft.Text("Parameter Values", weight="bold", color=pt.COLOR_GREY),
                ft.Text("General", weight="bold", color=pt.COLOR_TEXT),
                gp_container,
                ft.Text("xAI Additions", weight="bold", color=pt.COLOR_TEXT),
                xai_container,
            ],
            spacing=10,
            tight=True
        ),
        padding=10,
    )

    dlg = ft.AlertDialog(
        title=ft.Container(
            content=ft.Text(
                "Model Parameters",
                style=ft.TextStyle(color=pt.COLOR_MAIN_ACCENT, size=pt.FONT_SIZE_TITLE),
            ),
            bgcolor=pt.COLOR_TRANSPARENT,
            padding=ft.Padding(4, 0, 0, 0)
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Row([model_column, param_column], spacing=30, vertical_alignment="start"),
                        width=670
                    ),
                    ft.Container(expand=True)
                ],
                spacing=11,
                expand=True,
            ),
            height=500,
            padding=0,
            bgcolor=pt.COLOR_TRANSPARENT,
            border_radius=pt.BORDER_RADIUS,
        ),
        actions=[save_btn],
        actions_alignment="end",
        actions_padding=ft.Padding(20, 0, 20, 20),
        content_padding=ft.Padding(20, 10, 20, 5),
        inset_padding=0,
        modal=False,
        bgcolor=pt.COLOR_DARK_GREY,
        shape=ft.RoundedRectangleBorder(radius=pt.BORDER_RADIUS)
    )

    dlg.key = "SETTINGS_DIALOG"
    return dlg
