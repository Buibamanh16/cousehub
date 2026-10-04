
-- BUOC 1: Bat dau giao dich
BEGIN;

-- BUOC 2: Them dang ky tam thoi
INSERT INTO enrollments (student_id, class_section_id)
VALUES ('22000004', 'WEB-01');

-- BUOC 3: Kiem tra view trong giao dich
SELECT class_id, capacity, enrolled, remaining
FROM v_section_summary
WHERE class_id = 'WEB-01';

-- BUOC 4: Huy thay doi trong giao dich
ROLLBACK;

-- BUOC 5: Kiem tra lai sau rollback
SELECT class_id, capacity, enrolled, remaining
FROM v_section_summary
WHERE class_id = 'WEB-01';