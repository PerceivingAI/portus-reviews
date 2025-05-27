# portus_core_module/core_manager.py
"""
Main orchestration for the review‑app pipeline:
1. Validate & build URLs for each enabled site.
2. Call Apify actors (scan phase) with mapped parameters.
3. Clean resulting CSV/JSON if enabled.
4. Generate reply drafts if enabled.
5. Perform sentiment analysis and write report if enabled.
"""

from __future__ import annotations
import os
import sys
from pathlib import Path

# pull helpers dynamically (no frozen globals)
from portus_config_module import config_manager
from portus_config_module.config_manager import (
    reload_config,
    get_selected_hotel_name,
    get_selected_hotel_urls,
    get_writer_output_folder,
    get_review_sites,
    get_jobs,
    get_clean_columns,
    get_provider_name,
    get_apify_actors,
)

from portus_config_module.config_mapper import build_actor_input
from scan_module.scan_validator import validate_url
from scan_module.scan_processor import run_scanner
from writer_module.writer_main import prepare_writer_paths
from clean_module.clean_columns import clean_columns
from reply_module.reply_manager import handle_reply_generation
from portus_sa_module.sa_manager import handle_sentiment_analysis 


# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #
def _determine_active_sites(hotel_urls: dict) -> list[str]:
    reload_config()
    review_sites = get_review_sites()
    return [
        site for site, enabled in review_sites.items()
        if enabled and hotel_urls.get(site)
    ]


# --------------------------------------------------------------------------- #
#  Pipeline driver
# --------------------------------------------------------------------------- #
def run_app(log_gui: callable = lambda msg: None) -> Path:
    reload_config()

    # msg = "🔧 Operation mode: api"
    # print(msg)
    # log_gui(msg)

    api_key = os.getenv("APIFY_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("APIFY_API_KEY not found in environment variables")

    reload_config()
    hotel_name = get_selected_hotel_name()
    hotel_urls = get_selected_hotel_urls()
    output_root: Path = get_writer_output_folder()

    active_sites = _determine_active_sites(hotel_urls)
    if not active_sites:
        msg = "❌ No active review sites configured."
        print(msg)
        log_gui(msg)
        return output_root

    msg = f"🏨  Selected hotel: {hotel_name}"
    print(msg)
    log_gui(msg)

    for site in active_sites:
        msg = f"\n🌐 Processing site: {site}"
        print(msg)
        log_gui(msg)

        raw_url = hotel_urls.get(site, "")
        try:
            # msg = f"✅ Validated URL for '{site}': {raw_url}"
            # print(msg)
            # log_gui(msg)

            url = validate_url(site, raw_url)

            msg = f"🔗  Using URL: {url}"
            print(msg)
            log_gui(msg)
        except ValueError as exc:
            msg = f"❌ Invalid URL for {site}: {exc}"
            print(msg)
            log_gui(msg)
            continue

        paths = prepare_writer_paths(output_root, site)
        archive_path: Path = paths["archive_path"]
        clean_path:   Path = paths["clean_path"]

        reload_config()
        provider_name = get_provider_name()
        apify_actors  = get_apify_actors()
        jobs          = get_jobs()
        clean_cols    = get_clean_columns()
        scan_params   = build_actor_input(site)

        actor_id = apify_actors[f"actor_{site}"]

        msg = f"▶️ Running Apify actor: {actor_id}"
        print(msg)
        log_gui(msg)

        run_scanner(
            api_key=api_key,
            actor_id=actor_id,
            url=url,
            actor_input=scan_params,
            archive_path=archive_path,
        )

        msg = f"💾 Downloading results to: {archive_path}"
        print(msg)
        log_gui(msg)

        msg = f"✅ Scan complete: {archive_path}"
        print(msg)
        log_gui(msg)

        # 4) Clean phase
        if jobs.get("clean", True):
            msg = f"🧼  Cleaning data for {site}..."
            print(msg)
            log_gui(msg)

            keep_cols = clean_cols.get(site, [])
            clean_columns(
                site=site,
                columns_to_keep=keep_cols,
                source_file=archive_path,
                target_file=clean_path,
            )

        # 5) Reply generation
        if jobs.get("reply", True):
            msg = f"✍️  Generating replies for {site}..."
            print(msg)
            log_gui(msg)

            # msg = f"🧪 Provider: {provider_name}"
            # print(msg)
            # log_gui(msg)

            # msg = f"🧪 Active review sites: {[site]}"
            # print(msg)
            # log_gui(msg)

            msg = f"🧪 Clean file path: {clean_path}"
            print(msg)
            log_gui(msg)

            handle_reply_generation(
                provider=provider_name,
                active_sites=[site],
                clean_file_path=clean_path,
            )

            msg = f"✅ Reply generation complete."
            print(msg)
            log_gui(msg)

        # 6) Sentiment analysis
        if jobs.get("sa", True):
            msg = f"📊  Analyzing sentiment for {site}..."
            print(msg)
            log_gui(msg)

            handle_sentiment_analysis(
                site=site,
                clean_file_path=clean_path,
            )

            msg = "✅ SA done."
            print(msg)
            log_gui(msg)

    return output_root
