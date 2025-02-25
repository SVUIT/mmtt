from googleapiclient.discovery import build
from google.oauth2 import service_account
import yaml
import os
import json
import re  # 🟢 Thêm import này để xử lý chuẩn hóa tên

# Load thông tin credentials từ service-account.json
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SERVICE_ACCOUNT_JSON = os.getenv("GDRIVE_CREDENTIALS", "{}")  # Lấy từ GitHub Secrets
SERVICE_ACCOUNT_INFO = json.loads(SERVICE_ACCOUNT_JSON)  # Chuyển chuỗi JSON thành dict

creds = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

service = build('drive', 'v3', credentials=creds)

# 🟢 Thư mục chứa các file môn học (có thể có thư mục con)
MARKDOWN_FOLDER = "docs"
PARENT_FOLDER_ID = "1TjIygC_EermjfPRFDxsyw3qa3sOqMA3L"

def normalize_name(name):
    """Chuẩn hóa tên môn học: Chuyển về chữ thường và chỉ lấy mã môn (nếu có)."""
    name = name.strip().lower()
    match = re.match(r"([A-Za-z0-9]+)", name)  # Lấy phần mã môn (nếu có)
    return match.group(1) if match else name

def get_md_subjects():
    """ Lấy danh sách môn học từ docs/ (dựa vào tên file .md) """
    subjects = set()
    for root, _, files in os.walk(MARKDOWN_FOLDER):
        for file in files:
            if file.endswith(".md"):
                subject_name = os.path.splitext(file)[0]  # Lấy tên file, bỏ .md
                subjects.add(normalize_name(subject_name))  # 🟢 Chuẩn hóa tên trước khi lưu
    return subjects

def get_drive_folders(parent_folder_id):
    """ Lấy danh sách folder từ Google Drive """
    query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(
        q=query,
        fields="files(id, name, modifiedTime)",  
        supportsAllDrives=True
    ).execute()
    
    folders = results.get('files', [])
    return {normalize_name(folder['name']): {  # 🟢 Chuẩn hóa tên trước khi lưu
        "id": folder['id'], 
        "last_modified": folder.get('modifiedTime', "Không có thông tin")
    } for folder in folders}

def update_folders_yaml():
    """ Cập nhật danh sách môn học vào folders.yml dựa trên docs/ """
    md_subjects = get_md_subjects()  # Lấy danh sách môn học từ file .md
    drive_folders = get_drive_folders(PARENT_FOLDER_ID)  # Lấy danh sách từ Drive

    # 🟢 Lọc ra những môn học có trong docs nhưng vẫn giữ ID từ Drive
    folder_data = {"subjects": {}}
    for subject in md_subjects:
        if subject in drive_folders:
            folder_data["subjects"][subject] = drive_folders[subject]
        else:
            folder_data["subjects"][subject] = {"id": "Không có ID", "last_modified": "Không có thông tin"}

    # 🟢 Ghi vào YAML
    with open("folders.yml", "w", encoding="utf-8") as file:
        yaml.dump(folder_data, file, default_flow_style=False, allow_unicode=True)

    print("✅ Đã cập nhật file folders.yml!")

if __name__ == "__main__":
    update_folders_yaml()

