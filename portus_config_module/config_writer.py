# portus_config_module/config_writer.py

from dotenv import set_key
from pathlib import Path
import argparse
import sys
import ruamel.yaml

from portus_config_module.config_defaults import CONFIG_PATH, ENV_PATH
from portus_config_module.config_manager import load, save
from portus_config_module.config_utils import candidate_dirs

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True

def update_yaml_value(keys: list[str], new_value) -> None:
    """
    Update a deeply nested key in the YAML config file.
    `keys` is a list of keys that define the path to the value.
    Example: ["model_parameters", "xai_add_parameters"]
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        cfg = yaml.load(f)

    ref = cfg
    for k in keys[:-1]:
        if k not in ref or not isinstance(ref[k], dict):
            ref[k] = {}
        ref = ref[k]

    ref[keys[-1]] = new_value

    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.dump(cfg, f)

def update_env_value(key: str, value: str) -> None:
    """
    Update or create a key-value pair in the .env file.
    Uses the validated ENV_PATH.
    """
    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENV_PATH.touch(exist_ok=True)
    set_key(str(ENV_PATH), key, value.strip())
