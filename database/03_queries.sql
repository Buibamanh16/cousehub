-- Hiển thị danh sách học phần

SELECT code,name, credits
FROM courses
ORDER BY (code);
-- Tìm học phần theo một phần mã hoặc tên

SELECT code,name,credits
FROM courses
WHERE LOWER(code)LIKE'%web%' or LOWER(name)LIKE'%web%'
ORDER BY code;
-- Đếm số đăng kí và tính số chỗ còn lại của từng lớp

SELECT cs.id as class_id,
       cs.course_code,
       cs.capacity,
       COUNT(e.student_id) as enrolled,
       cs.capacity - COUNT(e.student_id) as remaining

FROM class_sections cs
LEFT JOIN enrollments e on e.class_section_id = cs.id
GROUP BY cs.id,cs.course_code,cs.capacity
ORDER BY cs.id;
-- Tìm sinh viên chưa đăng kí lớp nào

SELECT id,name,major
FROM students
WHERE NOT EXISTS(
    SELECT 1
    FROM enrollments e
    WHERE e.student_id = id
);
--Dùng CTE in ra lớp học và số sinh viên đã đki nếu chưa có sinh viên 
nào đăng kí thì không in

WITH section_counts AS (
SELECT cs.id AS class_id,
cs.capacity,
COUNT(e.student_id) AS enrolled
FROM class_sections AS cs
LEFT JOIN enrollments AS e ON e.class_section_id = cs.id
GROUP BY cs.id, cs.capacity
)
SELECT class_id, capacity, enrolled,
capacity - enrolled AS remaining
FROM section_counts
WHERE enrolled < capacity
ORDER BY class_id;
--Xếp hạng học phần theo số lượt đăng ký

WITH course_totals AS (
SELECT c.code, COUNT(e.student_id) AS total
FROM courses AS c
LEFT JOIN class_sections AS cs ON cs.course_code = c.code
LEFT JOIN enrollments AS e ON e.class_section_id = cs.id
GROUP BY c.code
)
SELECT code, total,
DENSE_RANK() OVER (ORDER BY total DESC) AS demand_rank
FROM course_totals
ORDER BY total DESC, code;
