# portus_interface_gui_module/top_bar/top_bar_builder.py

import flet as ft
from portus_interface_gui_module.top_bar.title import build_title
from portus_interface_gui_module.top_bar.provider_menu import build_provider_menu
from portus_interface_gui_module.top_bar.review_number import build_review_number
from portus_interface_gui_module.top_bar.cutoff_date import build_cutoff_date
from portus_interface_gui_module.menu.menu_button import build_menu_button
from portus_interface_gui_module.top_bar.output_folder import build_output_folder_row

def build_top_bar(
    page: ft.Page, dlg_help
) -> tuple[ft.Column, ft.Row, ft.Row, ft.TextField, ft.Text, ft.IconButton, ft.FilePicker]:
    """
    Return:
      • topbar: Column containing both rows
      • main_row: title, num_row, date_input, menu
      • sec_row: provider_menu, folder row wrapped in Row
      • num_input: # of reviews
      • date_input: cutoff date
      • out_path_text: dynamic folder text
      • btn_folder: folder button
      • folder_picker: file dialog
    """
    title = build_title()
    provider_menu, provider_menu_button, provider_label = build_provider_menu()
    num_row, num_input = build_review_number()
    date_row, date_input = build_cutoff_date()
    menu_btn = build_menu_button(dlg_help, page)
    folder_container, out_path_text, btn_folder, folder_picker = build_output_folder_row(page)

    main_row = ft.Row(
        controls=[
            title,
            ft.Container(width=50),
            date_row,
            ft.Container(width=50),
            num_row,
            ft.Container(expand=True),
            menu_btn,
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    sec_row = ft.Row(
        controls=[
            provider_menu, 
            ft.Container(width=52),
            folder_container
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    topbar = ft.Column(
        controls=[main_row, sec_row],
        spacing=0,
        tight=True,
    )

    return topbar, main_row, sec_row, num_input, date_input, out_path_text, btn_folder, folder_picker, provider_menu_button, provider_label

