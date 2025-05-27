# portus_interface_gui_module/top_bar/title.py

import flet as ft
import portus_theme_module as pt

def build_title() -> ft.Container:
    title = ft.Text(
        spans=[
            ft.TextSpan("Portus", style=ft.TextStyle(size=pt.FONT_SIZE_TITLE, weight=ft.FontWeight.W_500, color=pt.COLOR_MAIN_ACCENT)),
            ft.TextSpan("Reviews", style=ft.TextStyle(size=pt.FONT_SIZE_TITLE, weight=ft.FontWeight.W_500, color=pt.COLOR_TEXT)),
        ],
    )

    return ft.Container(
        content=title,
        alignment=ft.Alignment(0.0, 0.0),
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
        width=150,
        height=50,
        expand=False,
    )
