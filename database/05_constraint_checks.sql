
--Loi trung khoa chinh
INSERT INTO enrollments (student_id, class_section_id)
VALUES ('22000001', 'WEB-01');

--Loi khoa ngoai: sinh vien khong ton tai
INSERT INTO enrollments (student_id, class_section_id)
VALUES ('22999999', 'WEB-01');

--Loi CHECK: suc chua phai lon hon 0
UPDATE class_sections
SET capacity = 0
WHERE id = 'WEB-01';

--Loi NOT NULL: so tin chi khong duoc NULL
UPDATE courses
SET credits = NULL
WHERE code = 'INT2204';

--Loi UNIQUE: email bi trung
UPDATE students
SET email = 'anh@example.com'
WHERE id = '22000002';

--Loi CHECK: ten khong duoc rong hoac chi co khoang trang
UPDATE students
SET name = ' '
WHERE id = '22000004';

--Kiem tra so luot dang ky
SELECT COUNT(*) AS total_enrollments
FROM enrollments;