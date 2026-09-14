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


def extract_post_info(input_str):
    if "facebook.com" in input_str:
        return {"post_url": input_str}
    return {"post_id": input_str}


def get_post_details(params):
    url = f"{BASE_URL}/post"
    return requests.get(url, headers=get_headers(), params=params)


def print_post_details(post_data):
    print("=== Thông tin bài post ===")
    post = post_data.get("results", {})
    post_id = post.get("post_id", "Không có ID")
    post_type = post.get("type", "Không xác định")
    url = post.get("url", "Không có URL")
    message = post.get("message", "Không có nội dung")
    timestamp = post.get("timestamp", None)
    comments_count = post.get("comments_count", 0)
    reactions_count = post.get("reactions_count", 0)
    reshare_count = post.get("reshare_count", 0)
    reactions = post.get("reactions", {})
    author = post.get("author", {})
    author_name = author.get("name", "Không có tác giả")
    image = post.get("image", "Không có ảnh")

    print(f"Post ID: {post_id}")
    print(f"Loại bài: {post_type}")
    print(f"URL: {url}")
    print(f"Nội dung: {message}")
    print(f"Thời gian đăng: {timestamp if timestamp else 'Không có thời gian'}")
    print(f"Số lượng comment: {comments_count}")
    print(f"Số lượng tương tác: {reactions_count}")
    print(f"Chi tiết tương tác: {reactions}")
    print(f"Số lượng chia sẻ: {reshare_count}")
    print(f"Tác giả: {author_name}")
    print(f"Link ảnh: {image}")


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
    print("=== Tool Lấy Thông Tin Bài Post ===")

    input_str = input("Nhập Post ID hoặc URL bài viết: ").strip()
    if not input_str:
        print("Post ID hoặc URL là bắt buộc! Dừng chương trình.")
        raise SystemExit(1)

    params = extract_post_info(input_str)
    if "post_id" in params:
        print(f"Post ID: {params['post_id']}")
    else:
        print(f"Post URL: {params['post_url']}")

    response = get_post_details(params)
    print(f"API Status Code: {response.status_code}")

    post_data = response.json()
    if "results" in post_data:
        save_data(post_data, "post_details", "post_details")
        print_post_details(post_data)
    else:
        print("Không thể lấy thông tin bài post. Kiểm tra lại post_id hoặc URL, hoặc API response.")
