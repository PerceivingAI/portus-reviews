# portus_interface_gui_module/menu/menu_button.py

import flet as ft
from portus_interface_gui_module.menu.dialog_settings import build_settings_dialog
from portus_interface_gui_module.menu.dialog_api import build_api_dialog
import portus_theme_module as pt

def build_menu_button(dlg_help, page) -> ft.PopupMenuButton:
    def open_static(dlg):
        def handler(e):
            page.dialog = dlg
            dlg.open = True
            page.update()
        return handler

    def open_settings_dialog(e):
        dlg = build_settings_dialog()
        dlg.key = "SETTINGS_DIALOG"          

        # Remove any previous Settings dialog
        for ctl in list(page.overlay):
            if getattr(ctl, "key", None) == "SETTINGS_DIALOG":
                page.overlay.remove(ctl)

        page.overlay.append(dlg)
        page.dialog = dlg
        dlg.open = True
        page.update()

    def open_api_dialog(e):
        dlg = build_api_dialog()
        dlg.key = "API_DIALOG"              

        # Remove any previous API dialog
        for ctl in list(page.overlay):
            if getattr(ctl, "key", None) == "API_DIALOG":
                page.overlay.remove(ctl)

        page.overlay.append(dlg)
        page.dialog = dlg
        dlg.open = True
        page.update()

    return ft.PopupMenuButton(
        icon=ft.Icons.MENU_SHARP,
        tooltip=pt.custom_tooltip("Menu"),
        menu_position=ft.PopupMenuPosition.UNDER,
        offset=ft.Offset(0, 0),
        padding=ft.Padding(7, 7, 7, 7),
        **pt.pop_menu_button_sec(),
        items=[
        ft.PopupMenuItem(
            content=ft.Text("API Keys (Ctrl+A)", color=pt.COLOR_GREY),
            on_click=open_api_dialog
        ),
        ft.PopupMenuItem(
            content=ft.Text("Settings (Ctrl+,)", color=pt.COLOR_GREY),
            on_click=open_settings_dialog
        ),
        ft.PopupMenuItem(
            content=ft.Text("Help (Ctrl+H)", color=pt.COLOR_GREY),
            on_click=open_static(dlg_help)
        ),
    ]
    )
