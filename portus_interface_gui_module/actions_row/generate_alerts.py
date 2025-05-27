# portus_interface_gui_module/actions_row/generate_alerts.py

import flet as ft
import portus_theme_module as pt

dlg_message = ft.Text(
    "The pipeline completed successfully.",
    size=pt.FONT_SIZE_DEFAULT,
    color=pt.COLOR_GREY,
)

def build_alerts(page: ft.Page) -> tuple[ft.AlertDialog, ft.SnackBar, ft.Text]:
    def close_dialog(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=False,
        title=ft.Text(
            "Process Complete",
            size=pt.FONT_SIZE_TITLE,
            color=pt.COLOR_MAIN_ACCENT,
        ),
        content=dlg_message,
        actions=[
            ft.TextButton("OK", on_click=close_dialog, style=pt.text_button())
        ],
        bgcolor=pt.COLOR_DARK_GREY,
        shape=ft.RoundedRectangleBorder(radius=pt.BORDER_RADIUS)
    )

    snack = ft.SnackBar(
        content=ft.Text(
            "", 
            color=pt.COLOR_GREY, 
            size=pt.FONT_SIZE_DEFAULT
        ),
        open=False,
        bgcolor=pt.COLOR_DARK_GREY,
        show_close_icon=True,
        close_icon_color=pt.COLOR_MAIN_ACCENT,
        duration=3000,
        elevation=3,
        padding=ft.Padding(15, 0, 2, 5),
        dismiss_direction=ft.DismissDirection.DOWN,
    )

    page.overlay.append(dialog)
    page.snack_bar = snack

    return dialog, snack, dlg_message

