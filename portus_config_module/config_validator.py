# portus_config_module/config_validator.py

import sys
import os
from pathlib import Path
from typing import Any, Dict

import ruamel.yaml
from dotenv import load_dotenv
from portus_config_module.config_defaults import (
    reset_config_defaults,
    DEFAULT_CONFIG_CONTENT,
    CONFIG_FILENAME,
    CONFIG_PATH,
    ENV_PATH
)
from portus_config_module.config_utils import candidate_dirs
from portus_config_module.config_utils import find_config_path

yaml = ruamel.yaml.YAML()

def _recursive_validate(default: Dict[str, Any], actual: Dict[str, Any], path: str = ""):
    """
    Ensure that every key in `default` exists in `actual` at the same structure.
    Raises ValueError listing missing keys.
    """
    missing = []
    for key, def_val in default.items():
        if key not in actual:
            missing.append(f"{path}/{key}" if path else key)
        elif isinstance(def_val, dict):
            try:
                _recursive_validate(def_val, actual[key], f"{path}/{key}" if path else key)
            except ValueError as e:
                missing.extend(e.args[0])
    if missing:
        raise ValueError(missing)


def validate_or_create():
    cfg_path = find_config_path(CONFIG_FILENAME)
    if cfg_path is None:
        cfg_path = CONFIG_PATH
        reset_config_defaults(cfg_path)
        created = True
    else:
        created = False

    try:
        cfg = yaml.load(cfg_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to read config: {e}")
        sys.exit(1)

    if not created:
        try:
            default = yaml.load(DEFAULT_CONFIG_CONTENT)
            _recursive_validate(default, cfg)
        except ValueError as missing_keys:
            print("❌ Config structure invalid; missing keys:")
            for k in missing_keys.args[0]:
                print(f"   • {k}")
            sys.exit(1)

    mode = cfg["mode"]["default_mode"]

    if mode == "api":
        if ENV_PATH:
            load_dotenv(ENV_PATH, override=True)
        else:
            print("❌ .env not found; please create one or run with --reset-env to generate a placeholder.")
            sys.exit(1)

        prov = cfg["mode"]["api"]["default_provider"]
        env_var = {
            "openai": "OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "xai":   "XAI_API_KEY"
        }.get(prov)
        if not env_var:
            print(f"❌ Unknown provider: {prov}")
            sys.exit(1)