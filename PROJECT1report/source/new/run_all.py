import json
import os
from pathlib import Path
import subprocess
import sys
import webbrowser

BASE_DIR = Path(__file__).resolve().parent


def choose_item(items, prompt="Chọn số: "):
    if not items:
        return None

    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")

    try:
        choice = int(input(prompt).strip())
    except ValueError:
        print("Lựa chọn phải là một số.")
        return None

    if not 1 <= choice <= len(items):
        print("Lựa chọn ngoài phạm vi.")
        return None

    return items[choice - 1]


def run_process(command, cwd=None):
    """Run a child process without invoking a shell."""
    working_dir = str(cwd) if cwd else None
    try:
        result = subprocess.run(command, cwd=working_dir, check=False)
    except FileNotFoundError as exc:
        print(f"Không thể chạy lệnh: {exc}")
        return 127
    return result.returncode


def run_account_friend_layer():
    username = input("Nhập uid hoặc username: ").strip()
    if not username:
        print("Không được để trống uid/username!")
        return

    metaspy_dir = BASE_DIR / "crawl" / "metaspy"
    run_process(
        [sys.executable, "main.py", "friend-layer-crawler", username],
        cwd=metaspy_dir,
    )


def run_crawl_profile_data():
    metaspy_dir = BASE_DIR / "crawl" / "metaspy"
    run_process(
        [sys.executable, "-m", "src.facebook.account.crawl_profile_data"],
        cwd=metaspy_dir,
    )


def run_api_scripts():
    api_dir = BASE_DIR / "API"
    scripts = sorted(path.name for path in api_dir.glob("*.py") if path.name != "__init__.py")
    if not scripts:
        print("Không tìm thấy script API nào.")
        return

    print("Chọn script API để chạy:")
    script = choose_item(scripts)
    if not script:
        return

    run_process([sys.executable, script], cwd=api_dir)


def run_network_html():
    metaspy_dir = BASE_DIR / "crawl" / "metaspy"
    dirs = sorted(path for path in metaspy_dir.glob("friends_data_*") if path.is_dir())
    if not dirs:
        print("Không tìm thấy thư mục friends_data_*")
        return

    print("Chọn thư mục dữ liệu:")
    selected_dir_name = choose_item([path.name for path in dirs])
    if not selected_dir_name:
        return

    data_dir = metaspy_dir / selected_dir_name
    files = sorted(path for path in data_dir.glob("*.json") if path.is_file())
    if not files:
        print("Không có file JSON trong thư mục này!")
        return

    print("Chọn file JSON:")
    selected_file_name = choose_item([path.name for path in files])
    if not selected_file_name:
        return

    json_path = data_dir / selected_file_name
    try:
        with json_path.open("r", encoding="utf-8") as handle:
            raw_data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Không thể đọc dữ liệu JSON: {exc}")
        return

    tree_data = raw_data.get("tree_data", raw_data) if isinstance(raw_data, dict) else raw_data
    if not isinstance(tree_data, dict):
        print("Định dạng dữ liệu không hợp lệ: tree_data phải là object JSON.")
        return

    normalized_data = {
        "root_user": tree_data.get("id", ""),
        "max_layers": raw_data.get("max_layers", 2) if isinstance(raw_data, dict) else 2,
        "friends_per_layer": raw_data.get("friends_per_layer", 3) if isinstance(raw_data, dict) else 3,
        "crawled_at": raw_data.get("crawled_at", "") if isinstance(raw_data, dict) else "",
        "total_accounts": raw_data.get("total_accounts", 0) if isinstance(raw_data, dict) else 0,
        "tree_data": tree_data,
    }

    output_path = BASE_DIR / "data.js"
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("const jsonData = ")
        json.dump(normalized_data, handle, ensure_ascii=False, indent=2)
        handle.write(";")

    print(f"Đã tạo dữ liệu trực quan hóa từ {json_path}")
    webbrowser.open((BASE_DIR / "network.html").as_uri())


def run_map_visualization():
    index_path = BASE_DIR / "map" / "index.html"
    if not index_path.exists():
        print(f"Không tìm thấy file: {index_path}")
        return

    print(f"Đang mở file: {index_path}")
    webbrowser.open(index_path.as_uri())


def run_checkin_crawler():
    crawler_dir = BASE_DIR / "CrawCheckin"
    package_json = crawler_dir / "package.json"
    if not package_json.exists():
        print(f"Không tìm thấy file: {package_json}")
        return

    run_process(["npm", "start"], cwd=crawler_dir)


def run_checkin_visualization():
    data_dir = BASE_DIR / "CrawCheckin" / "src" / "data"
    if not data_dir.exists():
        print(f"Không tìm thấy thư mục: {data_dir}")
        return

    files = sorted(path for path in data_dir.glob("*.json") if path.is_file())
    if not files:
        print("Không có file JSON trong thư mục này!")
        return

    print("Chọn file dữ liệu check-in để hiển thị:")
    selected_file_name = choose_item([path.name for path in files])
    if not selected_file_name:
        return

    json_path = data_dir / selected_file_name
    try:
        with json_path.open("r", encoding="utf-8") as handle:
            checkin_data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Không thể đọc dữ liệu JSON: {exc}")
        return

    output_path = BASE_DIR / "data_checkin.js"
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("const jsonData = ")
        json.dump(checkin_data, handle, ensure_ascii=False, indent=2)
        handle.write(";")

    print(f"Đã tạo dữ liệu trực quan hóa từ {json_path}")
    webbrowser.open((BASE_DIR / "checkin_routes.html").as_uri())


def main():
    actions = {
        "1": run_account_friend_layer,
        "2": run_crawl_profile_data,
        "3": run_api_scripts,
        "4": run_network_html,
        "5": run_map_visualization,
        "6": run_checkin_crawler,
        "7": run_checkin_visualization,
    }

    while True:
        print("\n==== OSINT TOOL ====")
        print("1. Crawl danh sách bạn bè")
        print("2. Crawl thông tin cá nhân từng người từ data")
        print("3. OSINT bằng API")
        print("4. Sinh sơ đồ mạng (network.html)")
        print("5. Thống kê tỉnh thành từ dữ liệu")
        print("6. Lấy thông tin di chuyển (check-in)")
        print("7. Thống kê lịch trình di chuyển")
        print("0. Thoát")

        try:
            choice = input("Chọn chức năng: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nĐang thoát tool...")
            return

        if choice == "0":
            print("Đang thoát tool...")
            return

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
