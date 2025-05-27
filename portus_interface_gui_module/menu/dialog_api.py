# portus_interface_gui_module/menu/dialog_api.py

import os, time, threading
import flet as ft
from dotenv import load_dotenv

from portus_config_module.config_defaults import ENV_PATH
from portus_config_module.config_writer import update_env_value
import portus_theme_module as pt

def build_api_dialog() -> ft.AlertDialog:
    # 1) Load current keys
    load_dotenv(ENV_PATH, override=True)
    openai_key = "" if os.getenv("OPENAI_API_KEY", "").startswith("your-") else os.getenv("OPENAI_API_KEY", "")
    google_key = "" if os.getenv("GOOGLE_API_KEY", "").startswith("your-") else os.getenv("GOOGLE_API_KEY", "")
    xai_key    = "" if os.getenv("XAI_API_KEY", "").startswith("your-") else os.getenv("XAI_API_KEY", "")
    apify_key = "" if os.getenv("APIFY_API_KEY", "").startswith("your-") else os.getenv("APIFY_API_KEY", "")

    # 2) Input fields inside containers
    def make_input_container(label, value):
        return ft.Container(
            content=ft.TextField(
                label=label,
                #label_style=ft.TextStyle(color=pt.COLOR_MAIN_ACCENT),
                label_style=ft.TextStyle(color=pt.COLOR_GREY),
                text_style=ft.TextStyle(color=pt.COLOR_TEXT, size=pt.FONT_SIZE_LABEL),
                cursor_color=pt.COLOR_MAIN_ACCENT,
                value=value,
                password=True,
                width=300,
                height=50,
                bgcolor=pt.COLOR_TRANSPARENT,
                border_color=pt.COLOR_MAIN_ACCENT,
                border_radius=pt.BORDER_RADIUS,
                text_align="left",
                content_padding=ft.Padding(8, 0, 8, 20),

            ),
            width=300,
            height=50
        )

    openai_input_container = make_input_container("OpenAI API Key", openai_key)
    google_input_container = make_input_container("Google API Key", google_key)
    xai_input_container    = make_input_container("XAI API Key",    xai_key)
    apify_input_container = make_input_container("Apify API Key", apify_key)

    # Get actual fields back out to use them later
    openai_input = openai_input_container.content
    google_input = google_input_container.content
    xai_input    = xai_input_container.content
    apify_input = apify_input_container.content

    # 3) Eye button inside 50x50 container
    def make_toggle(field: ft.TextField) -> ft.Container:
        btn = ft.IconButton(
            icon=ft.Icons.VISIBILITY_OFF,
            tooltip="Show/hide API key",
            icon_color=pt.COLOR_MAIN_ACCENT,
            **pt.icon_sec_button()
        )
        def _toggle(_):
            field.password = not field.password
            btn.icon = ft.Icons.VISIBILITY if not field.password else ft.Icons.VISIBILITY_OFF
            field.update(); btn.update()
        btn.on_click = _toggle
        return ft.Container(content=btn, width=50, height=50, alignment=ft.Alignment(0, 0)
)

    openai_toggle = make_toggle(openai_input)
    google_toggle = make_toggle(google_input)
    xai_toggle    = make_toggle(xai_input)
    apify_toggle = make_toggle(apify_input)

    # 4) Save button with visual feedback
    save_btn = pt.elevated_main_button(text="Save", height=40, width=75, text_style=ft.TextStyle(color=pt.COLOR_BG, size=pt.FONT_SIZE_DEFAULT,  weight=ft.FontWeight.W_600))
    def save_api_keys(_):
        update_env_value("OPENAI_API_KEY", openai_input.value.strip())
        update_env_value("GOOGLE_API_KEY", google_input.value.strip())
        update_env_value("XAI_API_KEY",    xai_input.value.strip())
        update_env_value("APIFY_API_KEY", apify_input.value.strip())
        save_btn.text = "✓"
        #save_btn.icon = ft.Icons.CHECK_SHARP
        #save_btn.icon_color = pt.COLOR_GREY
        save_btn.update()
        def _revert():
            time.sleep(0.6)
            save_btn.icon = None
            save_btn.text = "Save"
            save_btn.update()
        threading.Thread(target=_revert, daemon=True).start()
    save_btn.on_click = save_api_keys

    # 5) Reset eye icons when dialog closes
    def on_dismiss(_):
        for fld, tog in (
            (xai_input,    xai_toggle),
            (openai_input, openai_toggle),
            (google_input, google_toggle),
            (apify_input, apify_toggle),
        ):
            fld.password = True
            tog.content.icon = ft.Icons.VISIBILITY_OFF
            fld.update(); tog.update()

    # 6) Row layout with fixed-size containers
    def row(input_container, toggle_container):
        return ft.Container(
            content=ft.Row(
                [input_container, toggle_container],
                alignment="center",
                vertical_alignment="center"
            ),
            padding=0
        )

    # 7) Final dialog
    dlg = ft.AlertDialog(
        title=ft.Container(
            content=ft.Text(
                "API Keys",
                style=ft.TextStyle(
                    color=pt.COLOR_MAIN_ACCENT,
                    size=pt.FONT_SIZE_TITLE
                ),
            ),
            bgcolor=pt.COLOR_TRANSPARENT,
            padding=ft.Padding(-4, 0, 0, 0)  # match content_padding left
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    row(openai_input_container, openai_toggle),
                    row(google_input_container, google_toggle),
                    row(xai_input_container,    xai_toggle),
                    row(apify_input_container, apify_toggle),
                ],
                spacing=10,
                alignment="center",
                #tight=False,  # Let it size naturally based on rows
            ),
            height=250,
            padding=0,
            bgcolor=pt.COLOR_TRANSPARENT,
            border_radius=pt.BORDER_RADIUS,
        ),
        actions=[save_btn],
        actions_alignment="end",
        actions_padding=ft.Padding(20, 5, 20, 20),
        content_padding=ft.Padding(20, 10, 20, 5),
        inset_padding=0,
        modal=False,
        on_dismiss=on_dismiss,
        bgcolor=pt.COLOR_DARK_GREY,
        #bgcolor='green',
        shape=ft.RoundedRectangleBorder(radius=pt.BORDER_RADIUS)
    )

    dlg.key = "API_DIALOG"
    return dlg
