"""Extract post records from a public REST API."""

import logging

import requests

logger = logging.getLogger(__name__)


def extract_posts(api_url: str, timeout: int = 20) -> list[dict]:
    """Fetch posts from the configured API and return decoded JSON records."""
    logger.info("Extracting records from %s", api_url)
    response = requests.get(api_url, timeout=timeout)
    response.raise_for_status()

    records = response.json()
    if not isinstance(records, list):
        raise ValueError("Expected the API response to be a JSON array.")

    logger.info("Extracted %d records", len(records))
    return records
