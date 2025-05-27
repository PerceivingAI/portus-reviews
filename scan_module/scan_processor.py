# scan_module/scan_processor.py

"""
Invokes an Apify actor with prepared input and downloads the resulting
dataset as XLSX.
"""

from __future__ import annotations
from pathlib import Path
import time
import requests
from apify_client import ApifyClient
from apify_client._errors import ApifyApiError


def run_scanner(
    api_key: str,
    actor_id: str,
    url: str,
    actor_input: dict,
    archive_path: Path,
) -> None:
    payload = {
        "startUrls": [{"url": url}],
        **actor_input,
    }

    client = ApifyClient(api_key)

    retry_delays = [1, 3, 7]
    for attempt, delay in enumerate(retry_delays, start=1):
        try:
            run = client.actor(actor_id).call(run_input=payload)
            dataset_id = run.get("defaultDatasetId")
            if not dataset_id:
                raise RuntimeError("❌ Actor run returned no defaultDatasetId")
            break
        except ApifyApiError as e:
            #print(f"❌ Attempt {attempt}: Actor run failed – {e}")
            if attempt == len(retry_delays):
                raise
            time.sleep(delay)

    download_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?format=xlsx"
    headers = {"Authorization": f"Bearer {api_key}"}

    #print(f"💾 Downloading results to: {archive_path}")
    for attempt, delay in enumerate(retry_delays, start=1):
        try:
            resp = requests.get(download_url, headers=headers, timeout=120)
            resp.raise_for_status()
            break
        except Exception as e:
            #print(f"❌ Attempt {attempt}: Download failed – {e}")
            if attempt == len(retry_delays):
                raise
            time.sleep(delay)

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_bytes(resp.content)
    #print("✅ Scan complete:", archive_path)
