import os  
import re  
import requests
#from github import Github
from urllib.parse import urljoin

folder_path = "./docs"
base_url = "https://svuit.org/mmtt/docs"

# Hàm lấy URL từ các file trong thư mục
def get_urls_from_folder(folder_path, base_url):
    urls = []  # Danh sách để lưu các URL
    for root, _, files in os.walk(folder_path): 
        for file in files:  
            if file.endswith(".md"):  # Chỉ xử lý các file có đuôi .md (Markdown)
                relative_path = os.path.relpath(root, folder_path)
                if relative_path == ".": 
                    relative_path = ""
                # Chuyển đổi đường dẫn file thành đường dẫn URL
                url_path = os.path.join(relative_path, file).replace("\\", "/")  
                url = f"{base_url}/{url_path}".replace(".md", ".html")  
                urls.append(url)  
    return urls  # Trả về danh sách URL

# Hàm trích xuất các liên kết từ nội dung file Markdown
def extract_urls_from_markdown(file_path):
    links = [] 
    link_pattern = r"\[.*?\]\((.*?)\)"  # Regular Expression để tìm các liên kết Markdown
    try:
        # Mở file với mã hóa UTF-8
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read() 
            matches = re.findall(link_pattern, content) 
            for match in matches:  
                if not match.startswith("http://") and not match.startswith("https://"):  
                    match = urljoin(base_url, match)
                links.append(match) 
    except Exception as e:  # Bắt lỗi nếu có vấn đề khi đọc file
        print(f"Error reading {file_path}: {e}")  # In ra lỗi
    return links  # Trả về danh sách liên kết

# Lấy URL từ thư mục
folder_urls = get_urls_from_folder(folder_path, base_url)

# Khởi tạo danh sách để lưu các liên kết từ nội dung Markdown
markdown_links = []

# Duyệt qua thư mục để xử lý từng file Markdown
for root, _, files in os.walk(folder_path): 
    for file in files:
        if file.endswith(".md"):  # Chỉ xử lý các file Markdown
            file_path = os.path.join(root, file)  
            # Trích xuất các liên kết từ nội dung file và thêm vào danh sách
            markdown_links.extend(extract_urls_from_markdown(file_path))

# Hợp nhất danh sách URL từ các file trong thư mục và các liên kết Markdown, sau đó loại bỏ trùng lặp
all_urls = list(set(folder_urls + markdown_links))

# Danh sách để lưu các URL không khả dụng
broken_urls = []

# Đặt User-Agent để tránh bị chặn bởi một số trang web
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Hàm kiểm tra một URL có khả dụng không
def check_url(url):
    try:
        response = requests.head(url, timeout=10, headers=headers, allow_redirects=True)
        if response.status_code >= 400:  # Các mã lỗi HTTP từ 400 trở lên là lỗi
            return False, response.status_code
        return True, response.status_code
    except requests.RequestException as e:
        return False, str(e)

# Kiểm tra từng URL trong danh sách
total_count = len(all_urls)
checked_count = 0

for url in all_urls:
    is_available, status = check_url(url)
