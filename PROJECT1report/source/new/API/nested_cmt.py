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


def get_nested_comments(post_id, comment_id, expansion_token):
    url = f"{BASE_URL}/post/comments_nested"
    params = {
        "post_id": post_id,
        "comment_id": comment_id,
        "expansion_token": expansion_token,
    }
    return requests.get(url, headers=get_headers(), params=params)


def print_nested_comment_details(nested_comment_data):
    print("=== Danh sách nested comment ===")
    for comment in nested_comment_data.get("results", []):
        comment_id = comment.get("legacy_comment_id", "Không có ID")
        comment_text = comment.get("message", "Không có nội dung")
        reactions_count = comment.get("reactions_count", "0")
        depth = comment.get("depth", 0)
        author = comment.get("author", {})
        author_name = author.get("name", "Không có tác giả")
        print(f"\nNested Comment ID: {comment_id}")
        print(f"Độ sâu (Depth): {depth}")
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
    print("=== Tool Lấy Nested Comment ===")

    post_id = input("Nhập Post ID: ").strip()
    if not post_id:
        print("Post ID là bắt buộc! Dừng chương trình.")
        raise SystemExit(1)

    comment_id = input("Nhập Comment ID: ").strip()
    if not comment_id:
        print("Comment ID là bắt buộc! Dừng chương trình.")
        raise SystemExit(1)

    expansion_token = input("Nhập Expansion Token: ").strip()
    if not expansion_token:
        print("Expansion Token là bắt buộc! Dừng chương trình.")
        raise SystemExit(1)

    response = get_nested_comments(post_id, comment_id, expansion_token)
    print(f"API Status Code: {response.status_code}")

    nested_comment_data = response.json()
    if "results" in nested_comment_data:
        save_data(nested_comment_data, "nested_cmt", "nested_cmt")
        print_nested_comment_details(nested_comment_data)
    else:
        print("Không thể lấy danh sách nested comment. Kiểm tra lại tham số hoặc API response.")
