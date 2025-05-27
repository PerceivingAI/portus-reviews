# scan_module/scan_manager.py
"""
Coordinates the “scan” phase for every active review site:
  1. Builds the list of active sites (enabled + URL present).
  2. For each site: validate URL, build actor input, run Apify scanner.
  3. Optionally triggers clean‑up and reply generation.
"""

from __future__ import annotations
import os
from pathlib import Path

from portus_config_module.config_manager import (
    reload_config,
    get_review_sites,
    get_selected_hotel_urls,
    get_writer_output_folder,
    get_apify_actors,
    get_jobs,
    get_clean_columns,
    get_provider_name,
)

from portus_config_module.config_mapper import build_actor_input
from scan_module.scan_validator import validate_url
from scan_module.scan_processor import run_scanner
from writer_module.writer_main import prepare_writer_paths
from clean_module.clean_columns import clean_columns
from reply_module.reply_manager import handle_reply_generation


# --------------------------------------------------------------------------- #
def _active_sites() -> list[str]:
    """Enabled sites that also have a URL for the selected hotel."""
    review_sites = get_review_sites()
    urls = get_selected_hotel_urls()
    return [
        site for site, enabled in review_sites.items()
        if enabled and urls.get(site)
    ]


# --------------------------------------------------------------------------- #
def run_scan() -> None:
    reload_config()
    jobs = get_jobs()
    if not jobs.get("scan", False):
        print("🔍 Scan job is disabled, skipping.")
        return

    sites = _active_sites()
    if not sites:
        print("❌ No active review sites configured, skipping scan.")
        return

    api_key = os.getenv("APIFY_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("APIFY_API_KEY not found in environment.")

    hotel_urls = get_selected_hotel_urls()
    output_root: Path = get_writer_output_folder()

    for site in sites:
        # 1) Validate URL
        raw_url = hotel_urls.get(site, "")
        try:
            url = validate_url(site, raw_url)
        except Exception as exc:
            print(f"❌ URL validation failed for '{site}': {exc}")
            continue

        # 2) Actor ID & mapped params
        actor_id = get_apify_actors()[f"actor_{site}"]
        actor_payload = build_actor_input(site)

        # 3) Prepare writer paths
        paths = prepare_writer_paths(output_root, site)
        archive_path: Path = paths["archive_path"]
        clean_path: Path = paths["clean_path"]

        # 4) Run the scanner
        try:
            run_scanner(
                api_key=api_key,
                actor_id=actor_id,
                url=url,
                actor_input=actor_payload,
                archive_path=archive_path,
            )
        except Exception as exc:
            print(f"❌ Scan failed for '{site}': {exc}")
            continue

        # 5) Clean phase
        if get_jobs().get("clean", False):
            keep_cols = get_clean_columns().get(site, [])
            clean_columns(
                site=site,
                columns_to_keep=keep_cols,
                source_file=archive_path,
                target_file=clean_path,
            )

        # 6) Reply generation phase
        if get_jobs().get("reply", False):
            handle_reply_generation(
                provider=get_provider_name(),
                active_sites=[site],
                clean_file_path=clean_path,
            )
