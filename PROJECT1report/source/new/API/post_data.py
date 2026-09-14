import json
from datetime import datetime
from pathlib import Path

import requests

from _rapidapi import BASE_URL, get_headers

REQUEST_TIMEOUT = 30


def convert_date(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Ngày phải có định dạng mm/dd/yyyy") from exc


def get_profile_posts(profile_id, start_date=None, end_date=None):
    params = {"profile_id": profile_id}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    return requests.get(
        f"{BASE_URL}/profile/posts",
        headers=get_headers(),
        params=params,
        timeout=REQUEST_TIMEOUT,
    )


def get_comments(post_id):
    response = requests.get(
        f"{BASE_URL}/comments",
        headers=get_headers(),
        params={"post_id": post_id},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def get_nested_comments(comment_id):
    response = requests.get(
        f"{BASE_URL}/comments/nested",
        headers=get_headers(),
        params={"comment_id": comment_id},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def print_post_details(data):
    print("=== Danh sách bài post ===")
    for post in data.get("results", []):
        timestamp = post.get("timestamp", 0)
        post_date = (
            datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            if timestamp
            else "Không có ngày"
        )
        print(f"\nPost ID: {post.get('post_id', 'Không có ID')}")
        print(f"Ngày đăng: {post_date}")
        print(f"Nội dung: {post.get('message', 'Không có nội dung')}")
        print(f"Số lượng tương tác: {post.get('reactions_count', 0)}")
        print(f"Số lượng comment: {post.get('comments_count', 0)}")


def save_data(data, subfolder, tool_name):
    base_dir = Path(__file__).resolve().parent / "data" / subfolder
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Hh_%M_%d_%m_%Y")
    file_path = base_dir / f"{tool_name}_{timestamp}.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã lưu dữ liệu vào {file_path}")


def main():
    profile_id = input("Nhập Profile/Page ID: ").strip()
    if not profile_id:
        raise ValueError("Profile/Page ID là bắt buộc")

    start_input = input("Ngày bắt đầu (mm/dd/yyyy, có thể để trống): ").strip()
    end_input = input("Ngày kết thúc (mm/dd/yyyy, có thể để trống): ").strip()
    start_date = convert_date(start_input) if start_input else None
    end_date = convert_date(end_input) if end_input else None

    response = get_profile_posts(profile_id, start_date, end_date)
    response.raise_for_status()
    data = response.json()
    save_data(data, "post_data", "post_data")
    print_post_details(data)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, requests.RequestException) as exc:
        raise SystemExit(f"Lỗi: {exc}") from exc
