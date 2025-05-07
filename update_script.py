import os
import datetime
from dateutil import parser
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Cấu hình
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
SERVICE_ACCOUNT_FILE = "drive-api-project-452000-10d4b5dc6bcc.json"
FOLDER_ID = "1TjIygC_EermjfPRFDxsyw3qa3sOqMA3L"
BASE_MD_FOLDER = "docs"

def validate_config():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"Không tìm thấy file {SERVICE_ACCOUNT_FILE}")
    if not os.path.exists(BASE_MD_FOLDER):
        raise FileNotFoundError(f"Không tìm thấy thư mục {BASE_MD_FOLDER}")

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)

def get_subfolders(service):
    query = f"'{FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    return service.files().list(q=query, fields="files(id, name)").execute().get("files", [])

def get_md_files():
    """Quét toàn bộ thư mục `docs/` đệ quy để lấy danh sách file Markdown."""
    md_files = {}
    for root, _, files in os.walk(BASE_MD_FOLDER):
        for file in files:
            if file.endswith(".md"):
                key = file.split(".")[0].lower()  # Lấy tên file không có đuôi .md
                md_files[key] = os.path.join(root, file)  # Lưu đường dẫn đầy đủ
    return md_files

def update_date_in_md(md_content, latest_date):
    """Xoá tất cả dòng ngày cập nhật cũ và chèn mới ngay trước '## Tài liệu môn học'"""
    new_content = []
    inserted = False
    for line in md_content:
        if line.strip().startswith("*Ngày cập nhật"):
            continue  # Xoá dòng ngày cập nhật cũ
        if not inserted and line.strip() == "## Tài liệu môn học":
            new_content.append(f"*Ngày cập nhật của folder Google Drive: {latest_date}*\n")
            inserted = True
        new_content.append(line)
    return new_content

def process_folder(service, folder, md_file_path):
    folder_id = folder["id"]

    # Lấy file trong thư mục con
    query = f"'{folder_id}' in parents and trashed = false"
    files = service.files().list(q=query, fields="files(id, name, modifiedTime)").execute().get("files", [])

    # Xác định ngày cập nhật mới nhất
    latest_date = "Không có dữ liệu"
    if files:
        latest_date = max(parser.isoparse(f["modifiedTime"]) for f in files).strftime("%d-%m-%Y")

    # Đọc nội dung Markdown
    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.readlines()

    # Cập nhật ngày
    md_content = update_date_in_md(md_content, latest_date)

    # So sánh trước khi ghi
    if old_content != md_content:
        with open(md_file_path, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(new_content)
        print(f"✓ Cập nhật {md_file_path} với ngày cập nhật: {latest_date}")
    else:
        print(f"✓ Không thay đổi gì ở {md_file_path}, bỏ qua ghi file.")

    # Ghi lại file
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.writelines(md_content)

    print(f"✓ Cập nhật {md_file_path} với ngày cập nhật: {latest_date}")

def main():
    print("🔍 Đang bắt đầu cập nhật...")
    validate_config()

    service = get_drive_service()
    subfolders = get_subfolders(service)
    md_files = get_md_files()

    for folder in subfolders:
        prefix = folder["name"].split(" ")[0].lower()
        if prefix not in md_files:
            print(f"⚠️ Bỏ qua {folder['name']} (không có Markdown tương ứng).")
            continue
        process_folder(service, folder, md_files[prefix])

    print("✅ Hoàn tất cập nhật tất cả các file Markdown!")

if __name__ == "__main__":
    main()
