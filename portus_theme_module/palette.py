# portus_theme_module\palette.py

"""
Color tokens – **do not edit values here without design approval**.
"""

COLOR_MAIN_ACCENT   = '#008080'
COLOR_MAIN_BUTTON   = '#006767'
COLOR_SEC_ACCENT    = '#36013f'

COLOR_BG            = 'black'
COLOR_TEXT          = '#e6e6e6'
COLOR_SUBTEXT       = '#d0d0d0'

COLOR_HOVER         = '#111111'
COLOR_HOVER_MAIN    = '#111111'
COLOR_HOVER_ALT     = '#1d2024'
COLOR_HOVER_T       = '#1a1a1a'

COLOR_TRANSPARENT   = '#00000000'

COLOR_DARK_GREY     = '#111111'
COLOR_ALERT_GREY    = '#272a2f'
COLOR_GREY          = '#b3b3b3'
COLOR_BORDER        = '#3a3a3a'
COLOR_SHADOW        = '#212121'
COLOR_RED           = 'red'

COLOR_ICON          = COLOR_MAIN_ACCENT
COLOR_TAG           = '#353535'

__all__ = [n for n in globals() if n.startswith("COLOR_")]
