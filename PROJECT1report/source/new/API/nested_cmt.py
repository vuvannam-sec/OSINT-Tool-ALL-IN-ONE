import json
from datetime import datetime
from pathlib import Path

import requests

from _rapidapi import BASE_URL, get_headers

REQUEST_TIMEOUT = 30


def get_nested_comments(post_id, comment_id, expansion_token):
    """Return replies to a Facebook comment."""
    params = {
        "post_id": post_id,
        "comment_id": comment_id,
        "expansion_token": expansion_token,
    }
    return requests.get(
        f"{BASE_URL}/post/comments_nested",
        headers=get_headers(),
        params=params,
        timeout=REQUEST_TIMEOUT,
    )


def print_nested_comment_details(data):
    print("=== Danh sách nested comment ===")
    for comment in data.get("results", []):
        author = comment.get("author", {})
        print(f"\nNested Comment ID: {comment.get('legacy_comment_id', 'Không có ID')}")
        print(f"Độ sâu (Depth): {comment.get('depth', 0)}")
        print(f"Tác giả: {author.get('name', 'Không có tác giả')}")
        print(f"Nội dung: {comment.get('message', 'Không có nội dung')}")
        print(f"Số lượng tương tác: {comment.get('reactions_count', 0)}")


def save_data(data, subfolder, tool_name):
    base_dir = Path(__file__).resolve().parent / "data" / subfolder
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Hh_%M_%d_%m_%Y")
    file_path = base_dir / f"{tool_name}_{timestamp}.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã lưu dữ liệu vào {file_path}")


def main():
    print("=== Tool Lấy Nested Comment ===")
    post_id = input("Nhập Post ID: ").strip()
    comment_id = input("Nhập Comment ID: ").strip()
    expansion_token = input("Nhập Expansion Token: ").strip()

    if not all((post_id, comment_id, expansion_token)):
        raise ValueError("Post ID, Comment ID và Expansion Token đều bắt buộc")

    response = get_nested_comments(post_id, comment_id, expansion_token)
    response.raise_for_status()
    data = response.json()
    save_data(data, "nested_cmt", "nested_cmt")
    print_nested_comment_details(data)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, requests.RequestException) as exc:
        raise SystemExit(f"Lỗi: {exc}") from exc
