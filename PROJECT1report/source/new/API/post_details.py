import json
from datetime import datetime
from pathlib import Path

import requests

from _rapidapi import BASE_URL, get_headers

REQUEST_TIMEOUT = 30


def extract_post_info(value):
    """Accept either a Facebook post URL or a post identifier."""
    value = value.strip()
    if not value:
        raise ValueError("Post ID hoặc URL là bắt buộc")
    return {"post_url": value} if "facebook.com" in value else {"post_id": value}


def get_post_details(params):
    return requests.get(
        f"{BASE_URL}/post",
        headers=get_headers(),
        params=params,
        timeout=REQUEST_TIMEOUT,
    )


def print_post_details(data):
    print("=== Thông tin bài post ===")
    post = data.get("results", {})
    author = post.get("author", {})
    fields = (
        ("Post ID", post.get("post_id", "Không có ID")),
        ("Loại bài", post.get("type", "Không xác định")),
        ("URL", post.get("url", "Không có URL")),
        ("Nội dung", post.get("message", "Không có nội dung")),
        ("Thời gian đăng", post.get("timestamp", "Không có thời gian")),
        ("Số lượng comment", post.get("comments_count", 0)),
        ("Số lượng tương tác", post.get("reactions_count", 0)),
        ("Chi tiết tương tác", post.get("reactions", {})),
        ("Số lượng chia sẻ", post.get("reshare_count", 0)),
        ("Tác giả", author.get("name", "Không có tác giả")),
        ("Link ảnh", post.get("image", "Không có ảnh")),
    )
    for label, value in fields:
        print(f"{label}: {value}")


def save_data(data, subfolder, tool_name):
    base_dir = Path(__file__).resolve().parent / "data" / subfolder
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Hh_%M_%d_%m_%Y")
    file_path = base_dir / f"{tool_name}_{timestamp}.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã lưu dữ liệu vào {file_path}")


def main():
    print("=== Tool Lấy Thông Tin Bài Post ===")
    params = extract_post_info(input("Nhập Post ID hoặc URL bài viết: "))
    response = get_post_details(params)
    response.raise_for_status()
    data = response.json()
    save_data(data, "post_details", "post_details")
    print_post_details(data)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, requests.RequestException) as exc:
        raise SystemExit(f"Lỗi: {exc}") from exc
