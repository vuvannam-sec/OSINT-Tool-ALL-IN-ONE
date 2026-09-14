import json
from datetime import datetime
from pathlib import Path

import requests

from _rapidapi import BASE_URL, get_headers

REQUEST_TIMEOUT = 30


def create_profile_url(value):
    value = value.strip()
    if not value:
        raise ValueError("Username hoặc UID là bắt buộc")
    return f"https://www.facebook.com/{value}/"


def get_profile_details(profile_url):
    return requests.get(
        f"{BASE_URL}/profile/details_url",
        headers=get_headers(),
        params={"url": profile_url},
        timeout=REQUEST_TIMEOUT,
    )


def print_profile_details(data):
    print("=== Thông tin profile ===")
    profile = data.get("profile", {})

    if profile.get("type") == "private_profile":
        print("Profile này là private, không có thông tin chi tiết để hiển thị.")
        return

    fields = (
        ("Tên", profile.get("name", "Không có tên")),
        ("Profile ID", profile.get("profile_id", "Không có ID")),
        ("URL", profile.get("url", "Không có URL")),
        ("Ảnh đại diện", profile.get("image", "Không có ảnh đại diện")),
        ("Giới thiệu", profile.get("intro", "Không có giới thiệu")),
        ("Ảnh bìa", profile.get("cover_image", "Không có ảnh bìa")),
        ("Giới tính", profile.get("gender", "Không xác định")),
    )
    for label, value in fields:
        print(f"{label}: {value}")

    about = profile.get("about", {})
    print("\nThông tin bổ sung:")
    if isinstance(about, dict):
        values = about.values()
    elif isinstance(about, list):
        values = about
    else:
        values = []

    found = False
    for item in values:
        if isinstance(item, dict):
            text = item.get("text")
        else:
            text = item
        if text:
            found = True
            print(f"- {text}")
    if not found:
        print("- Không có thông tin bổ sung.")


def save_data(data, subfolder, tool_name):
    base_dir = Path(__file__).resolve().parent / "data" / subfolder
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Hh_%M_%d_%m_%Y")
    file_path = base_dir / f"{tool_name}_{timestamp}.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã lưu dữ liệu vào {file_path}")


def main():
    print("=== Tool Lấy Thông Tin Profile ===")
    profile_url = create_profile_url(input("Nhập Username hoặc UID: "))
    response = get_profile_details(profile_url)
    response.raise_for_status()
    data = response.json()
    save_data(data, "profile_details", "profile_details")
    print_profile_details(data)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, requests.RequestException) as exc:
        raise SystemExit(f"Lỗi: {exc}") from exc
