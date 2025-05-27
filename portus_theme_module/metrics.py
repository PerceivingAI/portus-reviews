# portus_theme_module\metrics.py

"""
Window, chat and component size tokens.
"""

# Window
DEFAULT_WINDOW_WIDTH  = 1327
DEFAULT_WINDOW_HEIGHT = 810
MIN_WINDOW_WIDTH      = 850
MIN_WINDOW_HEIGHT     = 670

# Chat / input
DEFAULT_CHAT_WIDTH    = 780
DEFAULT_INPUT_WIDTH   = 850
MIN_CHAT_WIDTH        = 370
MIN_CHAT_HEIGHT       = 700

# Radii
BORDER_RADIUS         = 2

# Icons
ICON_MAIN_SIZE        = 32
ICON_MID_SIZE         = 30
ICON_SMALL_SIZE       = 28
ICON_TINY_SIZE        = 22

__all__ = [n for n in globals() if n.isupper()]
