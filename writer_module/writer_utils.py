# writer_module\writer_utils.py

from datetime import datetime
import re

SITE_PREFIX_MAP = {
    "tripadvisor": "TA",
    "google": "GO",
    "booking": "BK",
    "expedia": "EX"
}

def get_site_prefix(site: str) -> str:
    if site not in SITE_PREFIX_MAP:
        raise ValueError(f"Unknown site: {site}")
    return SITE_PREFIX_MAP[site]

def sanitize_and_truncate(name: str, max_len: int = 10) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', name.replace(" ", ""))
    return cleaned[:max_len]

def get_site_folder(site: str, hotel_name: str) -> str:
    prefix = get_site_prefix(site)
    hotel_tag = sanitize_and_truncate(hotel_name)
    return f"{prefix}_{hotel_tag}_Data"

def get_hotel_root_folder(hotel_name: str) -> str:
    return f"PS_{hotel_name}"

def generate_filenames(site: str, timestamp: str, hotel_name: str) -> dict:
    prefix = get_site_prefix(site)
    hotel_tag = sanitize_and_truncate(hotel_name)
    return {
        "archive_filename": f"{prefix}_Full_{hotel_tag}_{timestamp}.xlsx",
        "clean_filename":   f"{prefix}_Clean_{hotel_tag}_{timestamp}.xlsx",
        "archive_folder":   f"{prefix}_Archive"
    }
