# Study Vault UIT

## :memo: Giới thiệu

SVUIT là kho tài liệu trực tuyến, giúp các bạn sinh viên có thể tiếp cận trước tài liệu học tập cũng như tham khảo đồ án từ sinh viên khoá trước.

Repository này dành cho:

- Ban quản trị dự án(Administrator)
- Thành viên đóng góp(Contributor)

Nếu bạn muốn chia sẻ tài liệu học tập với chúng mình, bạn có thể:

- Liên hệ chúng mình thông qua địa chỉ email **studyvault.uit@gmail.com** và đính kèm tệp tài liệu của bạn.
- Tạo một **Issue** trên [repo GitHub](https://github.com/SVUIT/mmtt) và đính kèm đường dẫn của bạn.

Rất hoan nghênh sự đóng góp xây dựng của các bạn. :relaxed:

## :clap: Thành viên
<a href="https://github.com/SVUIT/mmtt/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=SVUIT/mmtt" />
</a>

## :anchor: Bắt đầu làm việc

1. Clone repository

```console
git clone https://github.com/SVUIT/mmtt.git
```

2. Tạo branch mới

```console
git branch <branch-name>
```
**Lưu ý:** Format tên branch `TenHo`

3. Chuyển sang branch vừa tạo và làm việc trên branch đấy

```console
git checkout <branch-name>
```

## :clipboard: Cấu trúc file Markdown

```markdown
---
layout: default
title: Mã môn học - Tên môn học
parent: Folder chứa môn học
---

# Mã môn học - Tên môn học

## Tài liệu môn học

[Folder Drive](link-tài-liệu){:target="_blank"}

## Mô tả môn học

### Hệ số điểm

| QT   | TH  | GK  | CK  |
|------|-----|-----|-----|
| <center>-</center>| <center>-</center>| <center>-</center> | <center>-</center> |

### Lý thuyết

Mô tả các chương, những thông tin liên quan ở phần lý thuyết...

### Thực hành

Mô tả các bài lab thực hành, hình thức thực hành (HT1/HT2)...

### Đồ án

Mô tả các nội dung về đồ án: số thành viên, đề tài...

### Hình thức thi

Mô tả hình thức thi giữa kỳ, cuối kỳ: thời gian, cấu trúc đề(tự luận/trắc nghiệm...), hình thức thi(tập trung/tại lớp...)

## Thông tin khác

Những thông tin hữu ích khác
```

## :floppy_disk: Cấu trúc Database

```
.
└── Docs/
    └── Mã môn - Tên môn/
        └── Khoá/
            ├── 1. Lý thuyết
            ├── 2. Thực hành
            ├── 3. Đồ án
            ├── 4. Ôn thi
            └── 5. Tài liệu tham khảo
```

## :computer: Chạy web ở Local

Từ từ sẽ có