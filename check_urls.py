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
    for root, _, files in os.walk(folder_path):  # Duyệt qua toàn bộ các thư mục và file con
        for file in files:  # Duyệt qua từng file
            if file.endswith(".md"):  # Chỉ xử lý các file có đuôi .md (Markdown)
                # Tính đường dẫn tương đối từ thư mục gốc
                relative_path = os.path.relpath(root, folder_path)
                if relative_path == ".":  # Nếu ở thư mục gốc, bỏ dấu "." vidu: svuit.org/mmtt/docs/./Templates -> svuit.org/mmtt/docs/Templates
                    relative_path = ""
                # Chuyển đổi đường dẫn file thành đường dẫn URL
                url_path = os.path.join(relative_path, file).replace("\\", "/")  # Đảm bảo dấu gạch chéo phù hợp
                url = f"{base_url}/{url_path}".replace(".md", ".html")  # Chuyển đổi đuôi .md thành .html
                urls.append(url)  # Thêm URL vào danh sách
    return urls  # Trả về danh sách URL

# Hàm trích xuất các liên kết từ nội dung file Markdown
def extract_urls_from_markdown(file_path):
    links = []  # Danh sách để lưu các liên kết
    link_pattern = r"\[.*?\]\((.*?)\)"  # Regular Expression để tìm các liên kết Markdown
    try:
        # Mở file với mã hóa UTF-8
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()  # Đọc toàn bộ nội dung file
            matches = re.findall(link_pattern, content)  # Tìm tất cả các liên kết
            for match in matches:  # Duyệt qua từng liên kết tìm được
                if not match.startswith("http://") and not match.startswith("https://"):  
                    # Nếu liên kết không phải là URL tuyệt đối (http/https), chuyển đổi thành tuyệt đối
                    match = urljoin(base_url, match)
                links.append(match)  # Thêm liên kết vào danh sách
    except Exception as e:  # Bắt lỗi nếu có vấn đề khi đọc file
        print(f"Error reading {file_path}: {e}")  # In ra lỗi
    return links  # Trả về danh sách liên kết

# Lấy URL từ thư mục
folder_urls = get_urls_from_folder(folder_path, base_url)

# Khởi tạo danh sách để lưu các liên kết từ nội dung Markdown
markdown_links = []

# Duyệt qua thư mục để xử lý từng file Markdown
for root, _, files in os.walk(folder_path):  # Duyệt qua tất cả các file trong thư mục
    for file in files:
        if file.endswith(".md"):  # Chỉ xử lý các file Markdown
            file_path = os.path.join(root, file)  # Đường dẫn đầy đủ đến file
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
print("Bắt đầu kiểm tra các URL...")
total_count = len(all_urls)
checked_count = 0

for url in all_urls:
    is_available, status = check_url(url)
    checked_count += 1
    
    # Hiển thị tiến trình kiểm tra
    if checked_count % 10 == 0 or checked_count == total_count:
        print(f"Đã kiểm tra: {checked_count}/{total_count} URLs", end="\r")
    
    if not is_available:
        broken_urls.append((url, status))

# In tổng kết
print("\n\n--- Tổng kết ---")
print(f"Tổng số URL kiểm tra: {total_count}")
print(f"Số URL lỗi: {len(broken_urls)}")

# In danh sách các URL lỗi
if broken_urls:
    print("\nDanh sách các URL lỗi:")
    for url, status in broken_urls:
        print(f"{url} - Trạng thái/Lỗi: {status}")
    
    # Lưu danh sách URL lỗi vào file
    with open("broken_urls.txt", "w", encoding="utf-8") as f:
        f.write("URL,Trạng thái/Lỗi\n")
        for url, status in broken_urls:
            f.write(f"{url},{status}\n")
    print("\nĐã lưu danh sách URL lỗi vào file 'broken_urls.txt'")
else:
    print("\nKhông tìm thấy URL nào bị lỗi.")