# portus_config_module/config_utils.py

import sys
import os
from pathlib import Path

def candidate_dirs():
    """Search order: CWD → script folder → frozen-exec temp dir."""
    yield Path.cwd()
    yield Path(sys.argv[0]).resolve().parent
    if getattr(sys, "frozen", False):
        yield Path(getattr(sys, "_MEIPASS", ""))
        
def find_config_path(filename: str) -> Path | None:
    for d in candidate_dirs():
        path = d / filename
        if path.is_file():
            return path
    return None

def find_env_path() -> Path | None:
    for d in candidate_dirs():
        env_file = d / ".env"
        if env_file.is_file():
            return env_file
    return None

def normalize_path(path: str) -> Path:
    """
    Normalize a user-provided path string:
    - Strip surrounding quotes
    - Expand ~ to user home
    - Return an absolute resolved Path object
    """
    cleaned = path.strip('"').strip("'")
    expanded = os.path.expanduser(cleaned)
    return Path(expanded).resolve()