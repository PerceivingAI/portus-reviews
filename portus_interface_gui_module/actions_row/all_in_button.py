# portus_interface_gui_module/actions_row/all_in_button.py

import threading
import time
import flet as ft

from portus_core_module.core_manager import run_app
from portus_config_module.config_writer import update_yaml_value
from portus_config_module.config_manager import (
    reload_config,
    CONFIG,
    get_writer_output_folder,
)
from portus_config_module.config_manager import get_writer_output_folder
from portus_interface_gui_module.actions_row.generate_alerts import build_alerts
import portus_theme_module as pt

def _run_cycle(idx: int, log_gui) -> str:
    update_yaml_value(["user_prompt_bank", "selected_prompt"], f"prompt_{idx}")
    update_yaml_value(["hotel_url_bank", "selected_hotel"], f"hotel_{idx}")
    reload_config()
    return run_app(log_gui=log_gui)

def build_all_in_button(page, progress_bar, dlg_result, snack, dlg_message, get_other_button):

    def on_click(e):
        btn_all_in.disabled = True
        get_other_button().disabled = True
        btn_all_in.text = "Running 1/8..."
        progress_bar.visible = True
        page.update()

        # Capture original prompt and hotel
        reload_config()
        original_prompt = CONFIG["user_prompt_bank"]["selected_prompt"]
        original_hotel = CONFIG["hotel_url_bank"]["selected_hotel"]

        def log_gui(msg: str):
            snack.content.value = msg.strip()
            page.open(snack)
            time.sleep(0.75)

        def worker():
            try:
                for idx in range(1, 8):
                    btn_all_in.text = f"Running {idx}/8..."
                    page.update()
                    output_path = _run_cycle(idx, log_gui)
            except Exception as ex:
                snack.content.value = f"[ERROR] {ex}"
                snack.open = True
            finally:
                # Restore original tab
                update_yaml_value(["user_prompt_bank", "selected_prompt"], original_prompt)
                update_yaml_value(["hotel_url_bank", "selected_hotel"], original_hotel)
                reload_config()

                btn_all_in.text = "All In"
                btn_all_in.disabled = False
                get_other_button().disabled = False
                progress_bar.visible = False

                output_path = get_writer_output_folder()

                dlg_message.value = f"All 8 cycles completed.\n\n{output_path}"
                dlg_result.open = True
                page.update()

        threading.Thread(target=worker, daemon=True).start()

    btn_all_in = pt.elevated_main_button(
        text="All In",
        tooltip=pt.custom_button_tooltip("Run user prompts 1‑8 (Ctrl+Shift-G)"),
        height=55,
        width=170,
        text_style=ft.TextStyle(size=pt.FONT_SIZE_TITLE, weight=ft.FontWeight.W_600),
        on_click=on_click,
    )
    return btn_all_in
