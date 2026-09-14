#!/usr/bin/env python3
"""Manual integration checks for the backend export flow.

A live crawl is opt-in: set OSINT_TEST_USERNAME locally. No real account
identifier is stored in the repository.
"""

import json
import os
import re

import requests

BASE_URL = "http://localhost:5000"


def test_live_export_flow():
    username = os.getenv("OSINT_TEST_USERNAME")
    if not username:
        print("Skipping live crawl: OSINT_TEST_USERNAME is not set.")
        return None

    crawl_url = f"{BASE_URL}/crawl-friend-list"
    payload = {
        "username": username,
        "layers": "0",
        "friends_per_layer": "1",
        "confirm": "y",
    }

    response = requests.post(crawl_url, json=payload, timeout=60)
    if response.status_code != 200:
        print(f"Live crawl failed: HTTP {response.status_code}")
        return False

    result = response.json()
    stdout = result.get("stdout", "")
    file_match = re.search(r"Dữ liệu đã được lưu tại: (.+\.json)", stdout)
    if not file_match:
        file_match = re.search(r"Đã lưu dữ liệu thành công vào\s+(.+\.json)", stdout)
    if not file_match:
        print("Could not find an exported JSON path in crawler output.")
        return False

    file_path = file_match.group(1).strip()
    check_url = f"{BASE_URL}/download-file"

    head_response = requests.head(check_url, params={"path": file_path}, timeout=10)
    if head_response.status_code != 200:
        print(f"Exported file is not available: HTTP {head_response.status_code}")
        return False

    download_response = requests.get(check_url, params={"path": file_path}, timeout=10)
    if download_response.status_code != 200:
        print(f"Download failed: HTTP {download_response.status_code}")
        return False

    try:
        exported = download_response.json()
    except json.JSONDecodeError:
        print("Downloaded export is not valid JSON.")
        return False

    print(f"Live export flow: PASS ({len(download_response.content)} bytes)")
    print(f"Export keys: {', '.join(list(exported.keys())[:5])}")
    return True


def test_existing_files():
    response = requests.get(f"{BASE_URL}/list-friends-data", timeout=10)
    if response.status_code != 200:
        print(f"Could not list existing exports: HTTP {response.status_code}")
        return False

    friends_data = response.json().get("data", {})
    for directory, files in friends_data.items():
        if not files:
            continue

        file_path = f"{directory}\\{files[0]}"
        download_response = requests.get(
            f"{BASE_URL}/download-file",
            params={"path": file_path},
            timeout=10,
        )
        if download_response.status_code == 200:
            print(f"Existing export download: PASS ({len(download_response.content)} bytes)")
            return True

    print("No downloadable existing export found.")
    return False


def main():
    print("Backend export flow checks")
    try:
        existing_ok = test_existing_files()
        live_result = test_live_export_flow()
    except requests.RequestException as exc:
        print(f"Backend request failed: {exc}")
        raise SystemExit(1) from exc

    if live_result is None:
        success = existing_ok
    else:
        success = existing_ok or live_result

    raise SystemExit(0 if success else 1)


if __name__ == "__main__":
    main()
