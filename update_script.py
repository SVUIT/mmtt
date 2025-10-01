import os
from dateutil import parser
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Config
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
SERVICE_ACCOUNT_FILE = "drive_api_key.json"
FOLDER_ID = "1TjIygC_EermjfPRFDxsyw3qa3sOqMA3L"
BASE_MD_FOLDER = "docs"

def validate_config():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"Khong tim thay file {SERVICE_ACCOUNT_FILE}")
    if not os.path.exists(BASE_MD_FOLDER):
        raise FileNotFoundError(f"Khong tim thay thu muc {BASE_MD_FOLDER}")

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

def get_subfolders(service):
    query = f"'{FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    return service.files().list(q=query, fields="files(id, name)").execute().get("files", [])

def get_md_files():
    """Scan BASE_MD_FOLDER de quy de lay file .md"""
    md_files = {}
    for root, _, files in os.walk(BASE_MD_FOLDER):
        for file in files:
            if file.endswith(".md"):
                key = file.split(".")[0].lower()
                md_files[key] = os.path.join(root, file)
    return md_files

def update_date_in_md(md_content, latest_date):
    """Xoa ngay cu, chen ngay moi truoc '## Tai lieu mon hoc'"""
    new_content = []
    inserted = False
    for line in md_content:
        if line.strip().startswith("*Ngay cap nhat"):
            continue
        if not inserted and line.strip() == "## Tai lieu mon hoc":
            new_content.append(f"*Ngay cap nhat cua folder Google Drive: {latest_date}*\n")
            inserted = True
        new_content.append(line)
    if not inserted:
        # neu khong tim thay tieu de, chen len dau file
        new_content = [f"*Ngay cap nhat cua folder Google Drive: {latest_date}*\n"] + new_content
    return new_content

def safe(s):
    """In ASCII an toan, tranh UnicodeEncodeError"""
    return ascii(s)

def process_folder(service, folder, md_file_path):
    folder_id = folder["id"]
    query = f"'{folder_id}' in parents and trashed = false"
    print(f"Query: {query}")
    files = service.files().list(
        q=query, fields="files(id, name, modifiedTime)"
    ).execute().get("files", [])
    print(f"So file: {len(files)}")

    latest_date = "Khong co du lieu"
    if files:
        latest_date = max(parser.isoparse(f["modifiedTime"]) for f in files).strftime("%d-%m-%Y")
    print(f"Ngay moi nhat: {latest_date}")

    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.readlines()
    print(f"So dong file goc: {len(md_content)}")

    md_content = update_date_in_md(md_content, latest_date)

    with open(md_file_path, "w", encoding="utf-8") as f:
        f.writelines(md_content)

    print(f"Cap nhat {md_file_path} voi ngay: {latest_date}")

def main():
    print("Bat dau cap nhat...")
    validate_config()

    service = get_drive_service()
    subfolders = get_subfolders(service)
    md_files = get_md_files()

    for folder in subfolders:
        prefix = folder["name"].split(" ")[0].lower()
        if prefix not in md_files:
            print(f"Bo qua {safe(folder['name'])} (khong co file .md tuong ung).")
            continue
        process_folder(service, folder, md_files[prefix])

    print("Hoan tat cap nhat tat ca file Markdown!")

if __name__ == "__main__":
    main()
