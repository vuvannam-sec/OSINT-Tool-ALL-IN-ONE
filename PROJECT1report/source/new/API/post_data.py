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


def convert_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%m/%d/%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        print("Định dạng ngày không hợp lệ! Vui lòng nhập theo định dạng mm/dd/yyyy (ví dụ: 01/15/2023).")
        return None


def get_profile_posts(profile_id, start_date=None, end_date=None):
    url = f"{BASE_URL}/profile/posts"
    params = {"profile_id": profile_id}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return requests.get(url, headers=get_headers(), params=params)


def get_comments(post_id):
    url = f"{BASE_URL}/comments"
    params = {"post_id": post_id}
    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()


def get_nested_comments(comment_id):
    url = f"{BASE_URL}/comments/nested"
    params = {"comment_id": comment_id}
    response = requests.get(url, headers=get_headers(), params=params)
    return response.json()


def print_post_details(post_data):
    print("=== Danh sách bài post ===")
    for post in post_data.get("results", []):
        post_id = post.get("post_id", "Không có ID")
        text = post.get("message", "Không có nội dung")
        reactions_count = post.get("reactions_count", 0)
        reactions = post.get("reactions", {})
        comments_count = post.get("comments_count", 0)
        timestamp = post.get("timestamp", 0)
        post_date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S") if timestamp else "Không có ngày"

        print(f"\nPost ID: {post_id}")
        print(f"Ngày đăng: {post_date}")
        print(f"Nội dung: {text}")
        print(f"Số lượng tương tác: {reactions_count}")
        print(f"Chi tiết tương tác: {reactions}")
        print(f"Số lượng comment: {comments_count}")

        comments_data = get_comments(post_id)
        print("\n--- Comment ---")
        for comment in comments_data.get("data", []):
            comment_id = comment.get("id")
            comment_text = comment.get("text", "Không có nội dung")
            comment_reactions = comment.get("reactions", {}).get("total", 0)
            print(f"Comment ID: {comment_id}")
            print(f"Nội dung: {comment_text}")
            print(f"Số lượng tương tác: {comment_reactions}")

            nested_comments_data = get_nested_comments(comment_id)
            print("   --- Nested Comment ---")
            for nested_comment in nested_comments_data.get("data", []):
                nested_comment_id = nested_comment.get("id")
                nested_comment_text = nested_comment.get("text", "Không có nội dung")
                nested_comment_reactions = nested_comment.get("reactions", {}).get("total", 0)
                print(f"   Nested Comment ID: {nested_comment_id}")
                print(f"   Nội dung: {nested_comment_text}")
                print(f"   Số lượng tương tác: {nested_comment_reactions}")


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
    profile_id = input("Nhập Profile/Page ID: ").strip()
    start_date_input = input("Nhập ngày bắt đầu (mm/dd/yyyy, để trống nếu không cần): ").strip()
    end_date_input = input("Nhập ngày kết thúc (mm/dd/yyyy, để trống nếu không cần): ").strip()

    start_date = convert_date(start_date_input) if start_date_input else None
    end_date = convert_date(end_date_input) if end_date_input else None

    if (start_date_input and start_date is None) or (end_date_input and end_date is None):
        print("Dừng chương trình do lỗi định dạng ngày!")
    else:
        print(f"Profile/Page ID: {profile_id}")
        if start_date:
            print(f"Ngày bắt đầu: {start_date}")
        if end_date:
            print(f"Ngày kết thúc: {end_date}")

        response = get_profile_posts(profile_id, start_date, end_date)
        print(f"API Status Code: {response.status_code}")

        post_data = response.json()
        if "results" in post_data:
            save_data(post_data, "post_data", "post_data")
            print_post_details(post_data)
        else:
            print("Không thể lấy danh sách bài post. Kiểm tra lại profile_id, ngày nhập, hoặc API response.")
