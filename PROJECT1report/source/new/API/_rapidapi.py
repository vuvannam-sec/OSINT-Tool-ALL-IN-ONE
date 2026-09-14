"""Shared RapidAPI configuration for the Facebook OSINT helpers."""

import os

API_HOST = os.getenv("RAPIDAPI_HOST", "facebook-scraper3.p.rapidapi.com").strip()
BASE_URL = f"https://{API_HOST}"


def get_headers() -> dict[str, str]:
    """Build request headers without storing credentials in source control."""
    api_key = os.getenv("RAPIDAPI_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "RAPIDAPI_KEY is not set. Export it in your shell before running this command."
        )

    return {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": API_HOST,
    }
