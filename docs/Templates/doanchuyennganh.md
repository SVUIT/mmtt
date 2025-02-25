**Ngày cập nhật**: Không có thông tin

---
layout: default
title: Đồ án chuyên ngành
parent: Templates
---

## Các mẫu Template

Mẫu template được dựng dựa trên [sonnh-uit/HCMUIT_thesistemplate](https://github.com/sonnh-uit/HCMUIT_thesistemplate/tree/master)

### Template LaTeX trên OverLeaf

[Truy cập](https://link.svuit.org/dacn-overleaf){: .btn .btn-primary }

### Source code template LaTeX

[Truy cập](https://github.com/SVUIT/report-templates/tree/main/specialized-project){: .btn .btn-primary }

## Hướng dẫn sử dụng Template đồ án môn học

### Cú pháp cơ bản

Đối với những bạn chưa sử dụng qua LaTeX hoặc ít sử dụng, có thể tham khảo link [Hướng dẫn trên OverLeaf](https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes) để biết sử dụng các cú pháp cơ bản nhé.

### Tổ chức file

```md
├── chapters
│   ├── front // Danh mục từ viết tắt và Lời cảm ơn
│   |    ├── glossaries.tex
│   |    ├── thanks.tex
│   ├── main // Nội dung chính
│   |    ├── chapter-1.tex
│   |    ├── chapter-2.tex
│   |    ├── conclusion.tex
│   |    ├── intro.tex
│   |    ├── summary.tex
├── graphics // Folder chứa hình ảnh
│   ├── chapter-1
│   |    ├──pic-1.png
│   ├── chapter-2
│   |    ├── pic-2.png
├── main.tex // File chính để tổng hợp nội dung từ các file khác
├── project.cls // Định nghĩa trang bìa và một số định dạng quan trọng như lề, khung trang.
├──ref.bib // Chứa các nguồn tài liệu tham khảo ở cuối báo cáo
```

### Overleaf bản xịn hơn

Bản free của OverLeaf sẽ có các hạn chế nhất định như chỉ được phép tối đa 2 người chỉnh sửa. Các bạn sinh viên khoa Mạng có thể sử dụng [latex.uitiot.vn](https://latex.uitiot.vn/project) (đăng nhập bằng mail trường) để được sử dụng các tính năng premium mà không tốn thêm phí, tuy nhiên sẽ hơi chậm khi compile.