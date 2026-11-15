# CourseHub - Buoi 4

## 1. Transaction và Concurrency

- Migration 001: `enrollment_events`.
- Demo class: `RACE-01`, capacity = 1.
- POST `/enrollments`: sử dụng `SELECT ... FOR UPDATE`.
- Concurrency test:
  - Student `22000002`: HTTP 201.
  - Student `22000004`: HTTP 409.
  - Kết quả: chỉ có một request đăng ký thành công.
  - `enrolled = 1`, `remaining = 0`.

## 2. Performance và Index

- Performance data: 100000 rows, dataset = `performance`.
- Index: `idx_enrollment_events_dataset_student_time`.

### Trước khi tạo Index

- Scan type: Seq Scan.
- Rows Removed by Filter: 99184.
- Buffers: 1137.
- Execution Time: 8.638 ms.

### Sau khi tạo Index

- Scan type: Index Scan.
- Buffers: 53 (50 hit, 3 read).
- Execution Time: 0.269 ms.

### Nhận xét

Sau khi tạo Composite Index trên ba cột `dataset`, `student_id`, `occurred_at DESC`, PostgreSQL chuyển từ Seq Scan sang Index Scan.

Thời gian thực thi giảm từ 8.638 ms xuống 0.269 ms, nhanh hơn khoảng 32.1 lần trong lần đo này.

## 3. Kết luận

- Đã áp dụng row locking để tránh race condition khi đăng ký học phần.
- Việc tạo và hủy đăng ký cùng ghi audit event trong một transaction.
- Đã kiểm thử hai request đồng thời.
- Đã tạo 100000 dòng dữ liệu hiệu năng và so sánh truy vấn trước/sau Index.

Không commit backend/.env.
