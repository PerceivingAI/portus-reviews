# portus_interface_gui_module/top_bar/provider_menu.py

import flet as ft
from typing import Callable

from portus_config_module.config_manager import load
from portus_config_module.config_writer import update_yaml_value
import portus_theme_module as pt

PROVIDER_LABELS = {
    "openai": "OpenAI",
    "google": "google",
    "xai": "xAI"
}

def build_provider_menu(
    on_change: Callable[[str], None] = None,
    *,
    menu_position: ft.PopupMenuPosition = ft.PopupMenuPosition.UNDER,
    offset: ft.Offset = ft.Offset(0, 0),
) -> ft.Container:
    """
    Builds a dropdown menu to select the current provider.
    Reads from and updates config.yaml directly.
    """
    cfg = load()
    current_provider = cfg["mode"]["api"]["default_provider"]
    on_change = on_change or (lambda *_: None)

    selected_txt = ft.Text(
        PROVIDER_LABELS.get(current_provider, current_provider),
        color=pt.COLOR_MAIN_ACCENT,
        size=pt.FONT_SIZE_DEFAULT,
        weight=ft.FontWeight.W_500,
    )

    def handle_select(provider: str):
        update_yaml_value(["mode", "api", "default_provider"], provider.lower())
        selected_txt.value = PROVIDER_LABELS.get(provider, provider)
        container.update()
        on_change(provider.lower())

    menu_items = [
        ft.PopupMenuItem(
            content=ft.Text(
                f"{PROVIDER_LABELS[p]} (Ctrl+{i+1})",
                color=pt.COLOR_GREY,
                size=pt.FONT_SIZE_LABEL,
                weight=ft.FontWeight.W_500
            ),
            height=40,
            on_click=lambda e, p=p: handle_select(p)
        )
        for i, p in enumerate(PROVIDER_LABELS)
    ]


    popup = ft.PopupMenuButton(
        icon=ft.Icons.ARROW_DROP_DOWN_SHARP,
        tooltip=pt.custom_tooltip("Select provider"),
        items=menu_items,
        menu_position=menu_position,
        offset=offset,
        padding=ft.Padding(7, 7, 7, 7),
        **pt.pop_menu_button()  # <- centralized button style
    )

    container = ft.Container(
        content=ft.Row(
            [popup, selected_txt],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
        alignment=ft.Alignment(0.0, 1.0),
        bgcolor=pt.COLOR_TRANSPARENT,
        #bgcolor='red',
        border_radius=ft.RoundedRectangleBorder(radius=pt.BORDER_RADIUS),
        border=ft.Border(
            left=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
            top=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
            right=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
            bottom=ft.BorderSide(0, pt.COLOR_TRANSPARENT),
        ),
        padding=ft.Padding(0, 0, 0, 0),
        margin=ft.Margin(0, 0, 0, 0),
        width=150,
        height=50,
        expand=False,
    )

    return container, popup, selected_txt

