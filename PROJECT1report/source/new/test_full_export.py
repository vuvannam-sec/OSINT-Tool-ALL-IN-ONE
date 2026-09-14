#!/usr/bin/env python3
"""Regression check for parsing an exported friends-data path.

The fixture is synthetic. It intentionally avoids account identifiers collected
from real users so the repository can remain safe to publish.
"""

import re

SYNTHETIC_RESULT = {
    "module": "info-crawl",
    "timestamp": "2026-01-01T00:00:00Z",
    "data": {
        "friends_dir": "friends_data_example",
        "returncode": 0,
        "stderr": "",
        "stdout": """Bắt đầu quá trình khởi tạo...
Bắt đầu chương trình chính...
Bước 1: Tìm kiếm thư mục friends_data_*
Đã chọn: friends_data_example
✓ Đã hoàn thành crawl profile!
Bước 7: Lưu dữ liệu đã crawl

🌳 Bắt đầu cập nhật dữ liệu vào cây
✅ Đã cập nhật dữ liệu cho node: example.user
🔁 Cập nhật 1 node con
✅ Đã cập nhật dữ liệu cho node: example.friend
🔁 Cập nhật 0 node con

💾 Đã lưu dữ liệu thành công vào
friends_data_example\\data_0_example.user.json
Chương trình đã hoàn thành!""",
        "success": True,
    },
    "status": "success",
}


def extract_export_path(stdout: str):
    match = re.search(r"💾 Đã lưu dữ liệu thành công vào\s+(.+\.json)", stdout)
    return match.group(1).strip() if match else None


def main():
    stdout = SYNTHETIC_RESULT["data"]["stdout"]
    export_path = extract_export_path(stdout)

    assert export_path == "friends_data_example\\data_0_example.user.json"
    print(f"Export path parser: PASS ({export_path})")


if __name__ == "__main__":
    main()
