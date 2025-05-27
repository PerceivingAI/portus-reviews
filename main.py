# main.py

import sys
import os
import certifi
from portus_config_module.config_validator import validate_or_create

validate_or_create()

# --- Runtime Environment Setup ------------------------------------
os.environ['SSL_CERT_FILE'] = certifi.where()
# print("SSL_CERT_FILE set to:", os.environ['SSL_CERT_FILE'])

os.environ["FLET_OFFLINE"] = "true"
# print("FLET_OFFLINE set to:", os.environ["FLET_OFFLINE"])

base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
flet_view_path = os.path.join(base_dir, "flet_desktop", "app", "flet")
os.environ["FLET_VIEW_PATH"] = flet_view_path
# print("FLET_VIEW_PATH set to:", os.environ["FLET_VIEW_PATH"])

# flet_exe_path = os.path.join(flet_view_path, "flet.exe")
# if os.path.isfile(flet_exe_path):
#     print("✅ flet.exe found at:", flet_exe_path)
# else:
#     print("❌ flet.exe NOT found at:", flet_exe_path)

# --- CLI / GUI Switch -----------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # CLI mode if any args are passed
        from portus_core_module.core_manager import run_app
        run_app()
    else:
        # GUI is the default
        from portus_interface_gui_module.main_layout import main_view
        import flet as ft
        ft.app(target=main_view)