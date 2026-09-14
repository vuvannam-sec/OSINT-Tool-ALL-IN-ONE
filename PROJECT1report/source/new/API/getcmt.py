import json
from datetime import datetime
from pathlib import Path

import requests

from _rapidapi import BASE_URL, get_headers

REQUEST_TIMEOUT = 30


def get_comments(post_id=None, cursor=None):
    """Return comments for a Facebook post or continue from a pagination cursor."""
    if not post_id and not cursor:
        raise ValueError("post_id or cursor is required")

    params = {}
    if post_id:
        params["post_id"] = post_id
    if cursor:
        params["cursor"] = cursor

    return requests.get(
        f"{BASE_URL}/post/comments",
        headers=get_headers(),
        params=params,
        timeout=REQUEST_TIMEOUT,
    )


def print_comment_details(comment_data):
    print("=== Danh sách comment ===")
    for comment in comment_data.get("results", []):
        author = comment.get("author", {})
        print(f"\nComment ID: {comment.get('legacy_comment_id', 'Không có ID')}")
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
    print("=== Tool Lấy Comment ===")
    choice = input("Lấy comment bằng (1) Post ID hoặc (2) Cursor? Nhập 1 hoặc 2: ").strip()

    if choice == "1":
        value = input("Nhập Post ID: ").strip()
        response = get_comments(post_id=value)
    elif choice == "2":
        value = input("Nhập Cursor: ").strip()
        response = get_comments(cursor=value)
    else:
        raise ValueError("Lựa chọn không hợp lệ")

    response.raise_for_status()
    comment_data = response.json()
    save_data(comment_data, "cmt", "cmt")
    print_comment_details(comment_data)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, requests.RequestException) as exc:
        raise SystemExit(f"Lỗi: {exc}") from exc
