#!/usr/bin/env python3
"""Small regression check for exported friends-data path parsing."""

import os
import re

SAMPLE_FILE = "friends_data_111704062025\\data_0_example.user.json"
SAMPLE_OUTPUT = f"""Bắt đầu quá trình khởi tạo...
Bắt đầu chương trình chính...
Bước 1: Tìm kiếm thư mục friends_data_*
...
💾 Đã lưu dữ liệu thành công vào
{SAMPLE_FILE}
Chương trình đã hoàn thành!"""


def main():
    print("=== TEST REGEX PATTERN ===")
    patterns = [
        r"Đã lưu dữ liệu thành công vào (.+\.json)",
        r"Đã lưu dữ liệu thành công vào\s+(.+\.json)",
        r"💾 Đã lưu dữ liệu thành công vào\s+(.+\.json)",
        r"💾 Đã lưu dữ liệu thành công vào\s*\n*(.+\.json)",
    ]

    for index, pattern in enumerate(patterns, 1):
        match = re.search(pattern, SAMPLE_OUTPUT)
        status = f"MATCH: '{match.group(1)}'" if match else "NO MATCH"
        print(f"Pattern {index}: {status}")

    file_path = SAMPLE_FILE
    if file_path.startswith("friends_data_"):
        processed_path = os.path.join("crawl", "metaspy", file_path)
    elif "\\" in file_path and file_path.split("\\")[0].startswith("friends_data_"):
        processed_path = os.path.join("crawl", "metaspy", file_path)
    else:
        processed_path = file_path

    normalized_path = processed_path.replace("\\", os.sep)
    print(f"Processed path: {normalized_path}")


if __name__ == "__main__":
    main()
