
CREATE VIEW v_section_summary AS
SELECT cs.id AS class_id,
       cs.course_code,
       cs.capacity,
       COUNT(e.student_id) AS enrolled,
       cs.capacity - COUNT(e.student_id) AS remaining
FROM class_sections cs
LEFT JOIN enrollments e
    ON e.class_section_id = cs.id
GROUP BY cs.id, cs.course_code, cs.capacity;

-- Xem toan bo thong ke
SELECT *
FROM v_section_summary
ORDER BY class_id;

-- Chi xem cac lop con cho
SELECT class_id, course_code, remaining
FROM v_section_summary
WHERE remaining > 0
ORDER BY class_id;

-- Tim lop da het cho
SELECT class_id, course_code, enrolled
FROM v_section_summary
WHERE remaining = 0
ORDER BY class_id;