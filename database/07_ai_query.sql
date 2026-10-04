

SELECT cs.id,
       COUNT(*) AS enrolled
FROM class_sections cs
LEFT JOIN enrollments e
    ON e.class_section_id = cs.id
WHERE cs.id = 'WEB-02'
GROUP BY cs.id;

-- TRUY VAN DUNG
-- COUNT(e.student_id) khong dem gia tri NULL.
-- WEB-02 phai co enrolled = 0.
SELECT cs.id,
       COUNT(e.student_id) AS enrolled
FROM class_sections cs
LEFT JOIN enrollments e
    ON e.class_section_id = cs.id
WHERE cs.id = 'WEB-02'
GROUP BY cs.id;