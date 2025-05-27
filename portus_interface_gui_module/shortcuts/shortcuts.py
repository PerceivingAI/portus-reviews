# portus_interface_gui_module/shortcuts/shortcuts.py

import flet as ft
from portus_interface_gui_module.menu.dialog_api import build_api_dialog
from portus_interface_gui_module.menu.dialog_settings import build_settings_dialog
from portus_config_module.config_writer import update_yaml_value

SHORTCUTS = {
    "CTRL+G": "generate",      # Generate responses
    "CTRL+O": "folder",        # Pick output folder
    "CTRL+N": "num_input",     # Focus on the num_input
    "CTRL+D": "date_input",    # Focus on the date_input
    "CTRL+A": "dialog_api",    # Open API dialog
    "CTRL+,": "dialog_settings",  # Open Settings
    "CTRL+S": "save_dialog",
    "CTRL+H": "dialog_help",   # Open Help
    "CTRL+P": "prompt",        # Focus prompt box
    "CTRL+SHIFT+G": "all_in",  # Trigger All In button
    "CTRL+1": "provider_openai",
    "CTRL+2": "provider_google",
    "CTRL+3": "provider_xai",
}

def attach_shortcuts(page: ft.Page, w: dict):
    """Bind keyboard shortcuts to widget actions."""
    def _on_key(e: ft.KeyboardEvent):
        mods = []
        if e.ctrl:
            mods.append("CTRL")
        if e.shift:
            mods.append("SHIFT")
        if e.alt:
            mods.append("ALT")
        key = "+".join(mods + [e.key.upper()])

        cmd = SHORTCUTS.get(key)
        if not cmd:
            return

        match cmd:
            case "generate":
                w["btn_generate"].on_click(None)

            case "all_in":
                w["btn_all_in"].on_click(None)
            case "folder":
                w["btn_folder"].on_click(None)
            case "num_input":
                w["num_input"].focus()
                page.update()
            case "date_input":
                w["date_input"].focus()
                page.update()
            case "dialog_api":
                dlg = build_api_dialog()
                page.overlay.append(dlg)
                page.dialog = dlg
                dlg.open = True
                page.update()
            case "dialog_settings":
                dlg = build_settings_dialog()
                page.overlay.append(dlg)
                page.dialog = dlg
                dlg.open = True
                page.update()
            case "save_dialog":
                dlg = page.dialog
                if dlg and dlg.open:
                    for action in dlg.actions:
                        if (
                            isinstance(action, ft.ElevatedButton)
                            and action.text
                            and action.text.lower().replace("\u00a0", " ").startswith("save")
                        ):
                            action.on_click(None)
                            break
            case s if s.startswith("dialog_"):
                w[s].open = True
                page.update()
            case "prompt":
                w["prompt"].focus()

            case "provider_openai":
                update_yaml_value(["mode", "api", "default_provider"], "openai")
                w["provider_label"].value = "OpenAI"
                w["provider_label"].update()
                w["provider_menu"].update()

            case "provider_google":
                update_yaml_value(["mode", "api", "default_provider"], "google")
                w["provider_label"].value = "Google"
                w["provider_label"].update()
                w["provider_menu"].update()

            case "provider_xai":
                update_yaml_value(["mode", "api", "default_provider"], "xai")
                w["provider_label"].value = "xAI"
                w["provider_label"].update()
                w["provider_menu"].update()

    page.on_keyboard_event = _on_key
