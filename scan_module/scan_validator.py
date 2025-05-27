# scan_module/scan_validator.py
from urllib.parse import urlparse

SITE_DOMAINS = {
    "tripadvisor": "tripadvisor.com",
    "google": "google.com",
    "booking": "booking.com",
    "expedia": "expedia.com",
}


def validate_url(site: str, url: str) -> str:
    if not url or not url.lower().startswith(("http://", "https://")):
        raise ValueError("Invalid URL: must start with http:// or https://")

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    expected = SITE_DOMAINS.get(site)
    if not expected:
        raise ValueError(f"No domain configured for site '{site}'")
    if expected not in domain:
        raise ValueError(
            f"URL domain mismatch: expected '{expected}' for '{site}', got '{domain}'"
        )

    cleaned = url.strip()
    print(f"✅ Validated URL for '{site}': {cleaned}")
    return cleaned
