# Buổi 6 - Docker, Testing, CI

## Môi trường

- OS: Windows
- Docker version: 29.2.1 (Docker Desktop)
- Python / Node version: Python 3.12 / Node 22

## Kết quả local

- pytest backend/tests -q: 2 passed
- npm test: 8 passed
- npm run build: Thành công (tạo thư mục dist/)
- docker compose up --build: Backend healthy, Frontend chạy tại cổng 8080

## Một luồng tích hợp đã kiểm tra

- Request: Đăng ký lớp WEB-01 cho sinh viên 22000004 qua http://127.0.0.1:8080/api/enrollments
- HTTP status: 201 Created (và 204 No Content khi hủy đăng ký)
- SQL xác nhận: Bảng enrollments và view v_section_summary cập nhật đúng số lượng và hoàn tác về trạng thái ban đầu

## Debug / AI

- Lỗi gặp phải:
  1. Docker daemon chưa khởi động (`failed to connect to the docker API`) -> Mở Docker Desktop chờ Engine running.
  2. Thiếu `frontend/Dockerfile` khi chạy Compose -> Tạo bổ sung file multi-stage build.
  3. `pytest` báo `ModuleNotFoundError: No module named 'backend'` -> Thêm `__init__.py` vào `backend/` và `backend/tests/`.
- Bằng chứng đã xem: Output terminal `docker info`, log build Compose và traceback của `pytest`.
- Nếu dùng AI: AI hỗ trợ giải thích cấu hình `.env.docker.example`, cách gỡ lỗi daemon/import package và đã tự chạy lệnh xác minh trên máy local.

## Pull Request / CI

- PR: (Điền link PR sau khi tạo ở Bước 4)
- Reviewer: (Tên thành viên review)
- CI run: (Điền trạng thái pass/fail sau khi push)
