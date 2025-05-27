# ───────────────────────────────────────────────────────────
#  Config manager: loads review_app_config.yaml once and
#  exposes convenient typed getters + published constants.
# ───────────────────────────────────────────────────────────
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict

import ruamel.yaml
from portus_config_module.config_defaults import CONFIG_PATH, DEFAULT_OUTPUT_PATH
from portus_config_module.config_utils import normalize_path

yaml = ruamel.yaml.YAML()

# --------------------------------------------------------------------------- #
#  Load YAML once
# --------------------------------------------------------------------------- #
try:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        CONFIG: Dict[str, Any] = yaml.load(f) or {}
except FileNotFoundError as exc:
    raise RuntimeError(
        f"Config file not found: {CONFIG_PATH}. "
        "Run the validator/reset routine first."
    ) from exc

# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #
class ConfigError(RuntimeError):
    """Raised when a required key is missing in the loaded config."""

def _expect(value: Any, dotted: str):
    if value is None:
        raise ConfigError(f"Missing required key `{dotted}`")
    return value

def load() -> Dict[str, Any]:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.load(f)

def reload_config() -> None:
    global CONFIG
    with CONFIG_PATH.open(encoding="utf-8") as f:
        CONFIG = yaml.load(f) or {}

def save(cfg: Dict[str, Any]) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.dump(cfg, f)

# --------------------------------------------------------------------------- #
#  Mode / provider / model getters
# --------------------------------------------------------------------------- #
def get_provider_mode() -> str:
    reload_config()
    return _expect(CONFIG["mode"]["default_mode"], "mode.default_mode")

def get_provider_name() -> str:
    reload_config()
    mode = get_provider_mode()
    return _expect(CONFIG["mode"][mode]["default_provider"],
                   f"mode.{mode}.default_provider")

def get_model() -> str:
    reload_config()
    mode, provider = get_provider_mode(), get_provider_name()
    return _expect(CONFIG["mode"][mode][provider]["model"],
                   f"mode.{mode}.{provider}.model")

def get_model_url(field: str = "base_url") -> str:
    reload_config()
    mode, provider = get_provider_mode(), get_provider_name()
    return _expect(CONFIG["mode"][mode][provider][field],
                   f"mode.{mode}.{provider}.{field}")

# --------------------------------------------------------------------------- #
#  Prompt & model‑parameter helpers
# --------------------------------------------------------------------------- #
def get_system_prompt() -> str:
    reload_config()
    bank = _expect(CONFIG["model_parameters"]["system_prompt_bank"], "model_parameters.system_prompt_bank")
    selected = _expect(bank["selected_system_prompt"], "model_parameters.system_prompt_bank.selected_system_prompt")
    return _expect(bank[selected], f"model_parameters.system_prompt_bank.{selected}")

def get_general_params() -> Dict[str, Any]:
    reload_config()
    return CONFIG["model_parameters"].get("general_parameters", {})

def get_xai_add_params() -> Dict[str, Any]:
    reload_config()
    return CONFIG["model_parameters"].get("xai_additional", {})

def get_additional_params() -> Dict[str, Any]:
    reload_config()
    return CONFIG["model_parameters"].get("additional", {})

# ----- user prompt ---------------------------------------------------------
def get_user_prompt() -> str:
    reload_config()
    bank = CONFIG["user_prompt_bank"]
    sel  = bank["selected_prompt"]
    return _expect(bank[sel], f"user_prompt_bank.{sel}")

# --------------------------------------------------------------------------- #
#  Review‑app‑specific helpers
# --------------------------------------------------------------------------- #
def get_review_sites() -> Dict[str, bool]:
    reload_config()
    return CONFIG.get("review_sites", {})

# ---------- hotel selection ----------
def get_selected_hotel_key() -> str:
    reload_config()
    return CONFIG["hotel_url_bank"]["selected_hotel"]

def get_selected_hotel_name() -> str:
    reload_config()
    sel = get_selected_hotel_key()
    return CONFIG["hotel_url_bank"][sel].get(f"{sel}_name", "")

def get_selected_hotel_urls() -> Dict[str, str]:
    reload_config()
    sel = get_selected_hotel_key()
    return {
        site: url
        for site, url in CONFIG["hotel_url_bank"][sel].items()
        if site in {"tripadvisor", "google", "booking", "expedia"}
    }

# ---------- scan / clean / writer ----------
def get_scan_general() -> Dict[str, Any]:
    reload_config()
    return CONFIG["scan_config"]["scan_general_parameters"]

def get_actor_extras(actor: str) -> Dict[str, Any]:
    key = {
        "tripadvisor": "tripadvisor_add",
        "google":      "google_add",
        "booking":     "booking_add",
        "expedia":     "expedia_add",
    }[actor]
    return CONFIG["scan_config"].get(key, {})

def get_apify_actors() -> Dict[str, str]:
    reload_config()
    return CONFIG["scan_config"]["apify_actors"]

def get_clean_columns() -> Dict[str, Any]:
    reload_config()
    return CONFIG["clean_config"]["columns_to_keep"]

def get_writer_output_folder() -> Path:
    reload_config()
    raw = CONFIG["writer_config"].get("output_folder", "").strip()
    return normalize_path(raw) if raw else DEFAULT_OUTPUT_PATH

def set_output_folder(path: str) -> None:
    reload_config()
    CONFIG.setdefault("writer_config", {})["output_folder"] = str(normalize_path(path))
    save(CONFIG)

def get_jobs() -> Dict[str, bool]:
    reload_config()
    return CONFIG["jobs"]

def get_selected_tab() -> str:
    reload_config()
    return CONFIG.get("selected_tab")

# --------------------------------------------------------------------------- #
#  Publish a few immutable constants for fast access
# --------------------------------------------------------------------------- #
PROVIDER_MODE     = get_provider_mode()
PROVIDER_NAME     = get_provider_name()
MODEL             = get_model()
BASE_URL          = get_model_url()

SYSTEM_PROMPT     = get_system_prompt()
GENERAL_PARAMS    = get_general_params()
XAI_ADD_PARAMS    = get_xai_add_params()
ADDITIONAL_PARAMS = get_additional_params()

REVIEW_SITES      = get_review_sites()
SCAN_GENERAL      = get_scan_general()          # dict (user‑friendly keys)
APIFY_ACTORS      = get_apify_actors()          # mapping id strings
CLEAN_COLUMNS     = get_clean_columns()
JOBS              = get_jobs()
HOTEL_NAME        = get_selected_hotel_name()

# --- values for cloud calls -------------------------------------------------
TEMPERATURE        = GENERAL_PARAMS.get("temperature")
TOP_P              = GENERAL_PARAMS.get("top_p")
STREAM             = GENERAL_PARAMS.get("stream")
TOOLS              = GENERAL_PARAMS.get("tools")
TOOL_CHOICE        = GENERAL_PARAMS.get("tool_choice")
MAX_OUTPUT_TOKENS  = GENERAL_PARAMS.get("max_output_tokens")
STORE              = GENERAL_PARAMS.get("store")

# --- values for local / additional -----------------------------------------
TOP_K             = ADDITIONAL_PARAMS.get("top_k")
MAX_TOKENS        = ADDITIONAL_PARAMS.get("max_tokens")
N_CTX             = ADDITIONAL_PARAMS.get("n_ctx")
PRESENCE_PENALTY  = ADDITIONAL_PARAMS.get("presence_penalty")
FREQUENCY_PENALTY = ADDITIONAL_PARAMS.get("frequency_penalty")
