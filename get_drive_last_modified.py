from googleapiclient.discovery import build
from google.oauth2 import service_account
import yaml

# Load thông tin credentials từ service-account.json
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SERVICE_ACCOUNT_FILE = 'service_account.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# id dỉve cua Docs
PARENT_FOLDER_ID = "1TjIygC_EermjfPRFDxsyw3qa3sOqMA3L" 

def get_subfolders(parent_folder_id):
    """ Lấy danh sách folder con trong thư mục cha """
    query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def update_folders_yaml():
    """ Cập nhật danh sách folder vào folders.yml """
    folders = get_subfolders(PARENT_FOLDER_ID)

    folder_data = {"subjects": {folder['name']: folder['id'] for folder in folders}}

    with open("folders.yml", "w", encoding="utf-8") as file:
        yaml.dump(folder_data, file, default_flow_style=False, allow_unicode=True)

    print("✅ Đã cập nhật file folders.yml!")

if __name__ == "__main__":
    update_folders_yaml()
