import json
import os
from datetime import datetime

import requests

API_HOST = "facebook-scraper3.p.rapidapi.com"
BASE_URL = "https://facebook-scraper3.p.rapidapi.com"


def get_headers():
    """Build request headers without storing credentials in source control."""
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        raise RuntimeError(
            "RAPIDAPI_KEY is not set. Configure it as an environment variable before running this tool."
        )
    return {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": API_HOST,
    }


def get_comments(post_id=None, cursor=None):
    url = f"{BASE_URL}/post/comments"
    params = {}
    if post_id:
        params["post_id"] = post_id
    if cursor:
        params["cursor"] = cursor
    return requests.get(url, headers=get_headers(), params=params)


def print_comment_details(comment_data):
    print("=== Danh sách comment ===")
    for comment in comment_data.get("results", []):
        comment_id = comment.get("legacy_comment_id", "Không có ID")
        comment_text = comment.get("message", "Không có nội dung")
        reactions_count = comment.get("reactions_count", "0")
        author = comment.get("author", {})
        author_name = author.get("name", "Không có tác giả")
        print(f"\nComment ID: {comment_id}")
        print(f"Tác giả: {author_name}")
        print(f"Nội dung: {comment_text}")
        print(f"Số lượng tương tác: {reactions_count}")


def save_data(data, subfolder, tool_name):
    base_dir = os.path.join(os.path.dirname(__file__), "data", subfolder)
    os.makedirs(base_dir, exist_ok=True)
    now = datetime.now()
    time_str = now.strftime("%Hh_%M_%d_%m_%Y")
    filename = f"{tool_name}_{time_str}.json"
    file_path = os.path.join(base_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Đã lưu dữ liệu vào {file_path}")


if __name__ == "__main__":
    print("=== Tool Lấy Comment ===")
    choice = input("Bạn muốn lấy comment bằng (1) Post ID hay (2) Cursor? Nhập 1 hoặc 2: ").strip()

    if choice == "1":
        post_id = input("Nhập Post ID: ").strip()
        response = get_comments(post_id=post_id)
    elif choice == "2":
        cursor = input("Nhập Cursor: ").strip()
        response = get_comments(cursor=cursor)
    else:
        print("Lựa chọn không hợp lệ! Dừng chương trình.")
        raise SystemExit(1)

    print(f"API Status Code: {response.status_code}")
    comment_data = response.json()
    if "results" in comment_data:
        save_data(comment_data, "cmt", "cmt")
        print_comment_details(comment_data)
    else:
        print("Không thể lấy danh sách comment. Kiểm tra lại post_id, cursor, hoặc API response.")
