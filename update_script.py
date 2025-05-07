def process_folder(service, folder, md_file_path):
    folder_id = folder["id"]

    # Lấy file trong thư mục con
    query = f"'{folder_id}' in parents and trashed = false"
    files = service.files().list(q=query, fields="files(id, name, modifiedTime)").execute().get("files", [])

    # Xác định ngày cập nhật mới nhất
    latest_date = "Không có dữ liệu"
    if files:
        latest_date = max(parser.isoparse(f["modifiedTime"]) for f in files).strftime("%d-%m-%Y")

    # Đọc nội dung Markdown gốc
    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.readlines()

    # Cập nhật ngày
    new_content = update_date_in_md(md_content, latest_date)

    # Chỉ ghi lại file nếu có thay đổi
    if md_content != new_content:
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.writelines(new_content)
        print(f"✓ Cập nhật {md_file_path} với ngày cập nhật: {latest_date}")
    else:
        print(f"✓ Không thay đổi gì ở {md_file_path}, bỏ qua ghi file.")
