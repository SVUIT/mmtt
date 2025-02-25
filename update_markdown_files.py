import yaml
import os
import re  # 🟢 Thêm thư viện để chuẩn hóa tên

FOLDERS_YML = "folders.yml"
MARKDOWN_FOLDER = "docs"  # Thư mục chứa các file .md của từng môn học

def normalize_name(name):
    """Chuẩn hóa tên môn học: Chuyển về chữ thường và chỉ lấy mã môn (nếu có)."""
    name = name.strip().lower()
    match = re.match(r"([A-Za-z0-9]+)", name)  # Lấy phần mã môn (nếu có)
    return match.group(1) if match else name

def get_md_files():
    """Duyệt qua thư mục docs/ và trả về mapping {chuẩn hóa tên: tên file đầy đủ}"""
    md_files = {}
    for root, _, files in os.walk(MARKDOWN_FOLDER):
        for file in files:
            if file.endswith(".md"):
                subject_name = os.path.splitext(file)[0]  # Bỏ phần mở rộng .md
                md_files[normalize_name(subject_name)] = os.path.join(root, file)  # Lưu đường dẫn đầy đủ
    return md_files

def update_markdown_files():
    # Đọc dữ liệu từ folders.yml
    with open(FOLDERS_YML, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    subjects = data.get("subjects", {})
    md_files = get_md_files()  # Lấy danh sách file .md trong docs/

    for subject, info in subjects.items():
        normalized_subject = normalize_name(subject)

        if normalized_subject in md_files:
            md_file_path = md_files[normalized_subject]

            with open(md_file_path, "r", encoding="utf-8") as md_file:
                lines = md_file.readlines()

            # Tìm và cập nhật ngày cập nhật
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                found = False
                for line in lines:
                    if line.startswith("**Ngày cập nhật**:"):
                        md_file.write(f"**Ngày cập nhật**: {info.get('last_modified', 'Không có dữ liệu')}\n")
                        found = True
                    else:
                        md_file.write(line)
                
                # Nếu file chưa có dòng ngày cập nhật, thêm vào đầu file
                if not found:
                    md_file.seek(0, 0)  # Quay lại đầu file để ghi nội dung mới
                    md_file.write(f"**Ngày cập nhật**: {info.get('last_modified', 'Không có dữ liệu')}\n\n")
                    md_file.writelines(lines)

            print(f"✅ Đã cập nhật {md_file_path}")
        else:
            print(f"⚠️ Không tìm thấy file .md cho môn học: {subject}")

if __name__ == "__main__":
    update_markdown_files()
