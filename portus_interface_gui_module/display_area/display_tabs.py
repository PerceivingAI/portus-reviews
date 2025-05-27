# portus_interface_gui_module/display_area/display_tabs.py

import flet as ft
import portus_theme_module as pt

from portus_config_module.config_manager import get_selected_tab, load
from portus_config_module.config_writer import update_yaml_value
from portus_interface_gui_module.display_area.display_tabs_content import build_user_content, build_system_content


# --------------------------------------------------------------------------- #
#  USER TABS
# --------------------------------------------------------------------------- #
def build_user_tabs() -> ft.Container:
    # ---------- Determine which tab should start selected -------------------
    sel_key = get_selected_tab()                 # e.g. "user_3"
    try:
        selected_index = int(sel_key.split("_")[1]) - 1
    except Exception:
        selected_index = 0                       # default to User 1

    # ---------- Build all 9 user tabs dynamically ---------------------------
    tabs: list[ft.Tab] = []
    reloaders: dict[int, callable] = {}

    for idx in range(1, 9):                     # 1..8
        container, reload_cb = build_user_content(idx)
        tabs.append(ft.Tab(text=f"User {idx}", content=container))
        reloaders[idx] = reload_cb

    user_tabs = pt.custom_tab(
        tabs=tabs,
        selected_index=selected_index,
    )

    # ---------- Update YAML + refresh when a tab is selected ----------------
    def _on_change(e: ft.ControlEvent):
        idx = e.control.selected_index + 1       # tab 0 → idx 1
        update_yaml_value(["user_prompt_bank", "selected_prompt"], f"prompt_{idx}")
        update_yaml_value(["hotel_url_bank", "selected_hotel"],   f"hotel_{idx}")
        reloaders[idx]()                         # pull fresh values

    user_tabs.on_change = _on_change

    # ---------- Also write YAML once at app start ---------------------------
    idx0 = selected_index + 1
    update_yaml_value(["user_prompt_bank", "selected_prompt"], f"prompt_{idx0}")
    update_yaml_value(["hotel_url_bank", "selected_hotel"],   f"hotel_{idx0}")
    
    update_yaml_value(["model_parameters", "system_prompt_bank", "selected_system_prompt"],   f"sys_prompt_a")

    return ft.Container(
        content=user_tabs,
        expand=True,
        padding=0,
        bgcolor=pt.COLOR_TRANSPARENT,
        border_radius=pt.BORDER_RADIUS,
    )

# --------------------------------------------------------------------------- #
#  SYSTEM TABS
# --------------------------------------------------------------------------- #
def build_system_tabs() -> ft.Container:
    # --- keys & labels ------------------------------------------------------
    keys_labels = [("sys_prompt_a", "System A"),
                   ("sys_prompt_b", "System B"),
                   ("sys_prompt_c", "System C")]

    tabs: list[ft.Tab] = []
    reloaders: dict[str, callable] = {}

    # --- build each tab -----------------------------------------------------
    for k, lbl in keys_labels:
        cont, reload_cb = build_system_content(k, lbl)
        tabs.append(ft.Tab(text=lbl, content=cont))
        reloaders[k] = reload_cb

    # --- which tab should be active? ---------------------------------------
    cfg = load()
    sel_key = cfg["model_parameters"]["system_prompt_bank"].get(
        "selected_system_prompt", "sys_prompt_a"
    )
    try:
        selected_index = [k for k, _ in keys_labels].index(sel_key)
    except ValueError:
        selected_index = 0

    sys_tabs = pt.custom_tab(tabs=tabs, selected_index=selected_index)

    # --- handler to update YAML & reload -----------------------------------
    def _on_change(e: ft.ControlEvent):
        idx = e.control.selected_index
        sel_key = keys_labels[idx][0]
        update_yaml_value(
            ["model_parameters", "system_prompt_bank", "selected_system_prompt"],
            sel_key,
        )
        reloaders[sel_key]()

    sys_tabs.on_change = _on_change

    # --- write YAML once on start (no reload) ------------------------------
    update_yaml_value(
        ["model_parameters", "system_prompt_bank", "selected_system_prompt"],
        keys_labels[selected_index][0],
    )

    return ft.Container(
        content=sys_tabs,
        expand=True,
        padding=0,
        bgcolor=pt.COLOR_TRANSPARENT,
        border_radius=pt.BORDER_RADIUS,
    )