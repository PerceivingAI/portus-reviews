# portus_config_module\config_mapper.py

from __future__ import annotations
from typing import Any, Dict

from portus_config_module.config_manager import reload_config, get_scan_general, get_actor_extras

# --------------------------------------------------------------------------- #
#  Mapping tables
# --------------------------------------------------------------------------- #
GENERAL_MAP: Dict[str, Dict[str, str | None]] = {
    "review_number": {
        "tripadvisor": "maxItemsPerQuery",
        "google":      "maxReviews",
        "booking":     "maxReviewsPerHotel",
        "expedia":     "maxReviewsPerHotel",
    },
    "sort_by": {
        "tripadvisor": None,
        "google":      "reviewsSort",
        "booking":     "sortReviewsBy",
        "expedia":     "sortBy",
    },
    "cutoff_date": {
        "tripadvisor": "lastReviewDate",
        "google":      "reviewsStartDate",
        "booking":     "cutoffDate",
        "expedia":     "minDate",
    },
    "review_ratings": {
        "tripadvisor": "reviewRatings",
        "booking":     "reviewScores",
    },
    "review_languages": {
        "tripadvisor": "reviewsLanguages",
    },
    "proxyEnabled": {
        "tripadvisor": "proxyConfiguration",
        "booking":     "proxyConfiguration",
    },
}

EXTRA_SECTIONS = {
    "tripadvisor": get_actor_extras("tripadvisor"),
    "google":      get_actor_extras("google"),
    "booking":     get_actor_extras("booking"),
    "expedia":     get_actor_extras("expedia"),
}

# --------------------------------------------------------------------------- #
#  Value translators
# --------------------------------------------------------------------------- #
def _translate_tripadvisor(user_key: str, value):
    if user_key == "review_ratings" and value == ["ALL"]:
        return ["ALL_REVIEW_RATINGS"]
    if user_key == "review_languages" and value == ["ALL"]:
        return ["ALL_REVIEW_LANGUAGES"]
    return value

def _translate_booking(user_key: str, value):
    if user_key == "sort_by":
        return {
            "newest": "f_recent_desc",
            "oldest": "f_recent_asc",
            "high_score": "f_score_desc",
            "low_score": "f_score_asc",
            "relevance": "f_relevance",
        }.get(value, value)
    return value

def _translate_expedia(user_key: str, value):
    if user_key == "sort_by":
        return {
            "newest": "Most recent",
            "relevance": "Most relevant",
            "high_score": "Highest guest rating",
            "low_score": "Lowest guest rating",
        }.get(value, value)
    return value

# --------------------------------------------------------------------------- #
#  Public builder
# --------------------------------------------------------------------------- #
def build_actor_input(actor: str) -> Dict[str, Any]:
    if actor not in ("tripadvisor", "google", "booking", "expedia"):
        raise ValueError(f"Unknown actor key: {actor}")

    reload_config()  # ✅ Force fresh config every time
    general = get_scan_general().copy()  # ✅ Pull updated value
    actor_payload: Dict[str, Any] = {}

    proxy_flag = general.pop("proxyEnabled", False)

    for user_key, value in general.items():
        target_name = GENERAL_MAP.get(user_key, {}).get(actor)
        if not target_name:
            continue

        if actor == "tripadvisor":
            value = _translate_tripadvisor(user_key, value)
        elif actor == "booking":
            value = _translate_booking(user_key, value)
        elif actor == "expedia":
            value = _translate_expedia(user_key, value)

        actor_payload[target_name] = value

    if proxy_flag and actor in ("tripadvisor", "booking"):
        actor_payload["proxyConfiguration"] = {"useApifyProxy": True}

    actor_payload.update(EXTRA_SECTIONS[actor])
    return actor_payload
