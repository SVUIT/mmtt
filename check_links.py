import os
import re
import requests
from urllib.parse import urljoin

# Thư mục chứa file markdown
folder_path = "./docs"
# URL gốc của website
base_url = "https://svuit.org/mmtt/docs"
# GitHub repo details
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")  # Lấy repo từ GitHub Actions
GITHUB_TOKEN = os.getenv("ISSUE_API")  # Token để tạo issue

# Header giả lập trình duyệt để tránh bị chặn
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_urls_from_folder(folder_path, base_url):
    """Lấy danh sách URL từ các file markdown trong thư mục."""
    urls = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                relative_path = os.path.relpath(root, folder_path).replace("\\", "/")
                url_path = os.path.join(relative_path, file).replace("\\", "/")
                url = f"{base_url}/{url_path}".replace(".md", ".html")
                urls.append(url)
    return urls

def extract_urls_from_markdown(file_path, base_url):
    """Trích xuất tất cả các URL từ file Markdown, giữ đúng phần anchor (#)."""
    links = []
    link_pattern = r"\[.*?\]\((.*?)\)"
    
    # Lấy URL gốc của file markdown hiện tại
    relative_path = os.path.relpath(file_path, folder_path).replace("\\", "/")
    base_file_url = f"{base_url}/{relative_path}".replace(".md", ".html")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            matches = re.findall(link_pattern, content)
            for match in matches:
                if match.startswith(("http://", "https://")):
                    full_url = match  # URL tuyệt đối
                elif match.startswith("#"):
                    full_url = base_file_url + match  # Link anchor trong file
                elif match.startswith("/"):
                    full_url = urljoin(base_url, match)  # Link tuyệt đối theo trang gốc
                else:
                    full_url = urljoin(base_file_url, match)  # Link tương đối

                links.append(full_url)
    except Exception as e:
        print(f"⚠️ Lỗi khi đọc {file_path}: {e}")
    return links

def check_url(url):
    """Kiểm tra xem URL có hoạt động không."""
    try:
        response = requests.head(url, timeout=10, headers=HEADERS, allow_redirects=True)
        if 404 <= response.status_code <= 500:
            return False, response.status_code
        return True, response.status_code
    except requests.RequestException as e:
        return False, str(e)

def create_github_issue(broken_urls):
    """Tạo issue trên GitHub với danh sách broken links."""
    print(f"GITHUB_REPOSITORY: {os.getenv('GITHUB_REPOSITORY')}")
    print(f"ISSUE_API: {'Đã tìm thấy' if os.getenv('ISSUE_API') else 'Không tìm thấy'}")

    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("⚠️ Không tìm thấy GITHUB_TOKEN hoặc GITHUB_REPOSITORY. Bỏ qua việc tạo issue.")
        return

    issue_title = "🚨 Broken Links Detected!"
    issue_body = "Danh sách các liên kết bị lỗi được phát hiện:\n\n"
    for error in broken_urls:
        issue_body += f"- {error}\n"

    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": issue_title,
        "body": issue_body,
        "labels": ["broken-links"]
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("✅ Issue đã được tạo thành công!")
    else:
        print(f"❌ Lỗi khi tạo issue: {response.status_code} - {response.text}")

if __name__ == '__main__':
    print("🔍 Đang thu thập danh sách URL từ thư mục...")

    folder_urls = get_urls_from_folder(folder_path, base_url)
    markdown_links = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                markdown_links.extend(extract_urls_from_markdown(file_path, base_url))

    all_urls = list(set(folder_urls + markdown_links))

    broken_urls = []
    total_count = len(all_urls)
    checked_count = 0

    print(f"🔗 Tổng số URL cần kiểm tra: {total_count}")

    for url in all_urls:
        checked_count += 1
        print(f"({checked_count}/{total_count}) Kiểm tra: {url} ...", end=" ")
        is_available, status = check_url(url)
        if not is_available:
            print(f"❌ LỖI ({status})")
            broken_urls.append(f"{url} ➝ Lỗi: {status}")
        else:
            print(f"✅ Hoạt động ({status})")

    if broken_urls:
        create_github_issue(broken_urls)
    else:
        print("\n🎉 Tất cả URL đều hợp lệ!")
