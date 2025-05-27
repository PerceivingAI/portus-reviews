# portus_interface_gui_module\actions_row\generate_button.py

import threading
import time

import flet as ft
from portus_core_module.core_manager import run_app
import portus_theme_module as pt
from portus_config_module.config_manager import get_writer_output_folder
from portus_interface_gui_module.actions_row.generate_alerts import build_alerts


def build_generate_button(page, progress_bar, dlg_result, snack, dlg_message, get_other_button,) -> ft.ElevatedButton:

    def on_click(e):
        btn_generate.text = "Processing..."
        btn_generate.disabled = True
        get_other_button().disabled = True 
        progress_bar.visible = True
        page.update()

        def log_gui(msg: str):
            snack.content.value = msg.strip()
            page.open(snack)
            time.sleep(0.75)

        def run_pipeline():
            try:
                output_path = run_app(log_gui=log_gui)
            except Exception as ex:
                snack.content.value = f"[ERROR] {str(ex)}"
                snack.open = True
                page.update()
            finally:
                btn_generate.text = "Process"
                btn_generate.disabled = False
                get_other_button().disabled = False
                progress_bar.visible = False

                output_path = get_writer_output_folder()

                dlg_message.value = f"The pipeline completed successfully.\n\n{output_path}"
                dlg_result.open = True
                page.update()

        thread_pipeline = threading.Thread(target=run_pipeline, daemon=True)
        thread_pipeline.start()

    btn_generate = pt.elevated_main_button(
        text="Process",
        tooltip=pt.custom_button_tooltip("Run full app pipeline (Ctrl+G)"),
        height=55,
        width=170,
        text_style=ft.TextStyle(size=pt.FONT_SIZE_TITLE, weight=ft.FontWeight.W_600),
        on_click=on_click
    )

    return btn_generate
