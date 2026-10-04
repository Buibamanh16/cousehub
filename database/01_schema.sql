
-- =========================================
-- FILE 01: TAO CAU TRUC DATABASE COURSEHUB
-- =========================================

CREATE TABLE students (
    id VARCHAR(8) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    major VARCHAR(20) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,

    CONSTRAINT ck_students_id
        CHECK (LENGTH(id) = 8),

    CONSTRAINT ck_students_name
        CHECK (TRIM(name) <> '')
);

CREATE TABLE courses (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    credits INTEGER NOT NULL,

    CONSTRAINT ck_courses_credits
        CHECK (credits BETWEEN 1 AND 6)
);

CREATE TABLE semesters (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,

    CONSTRAINT ck_semesters_dates
        CHECK (end_date >= start_date)
);

CREATE TABLE lecturers (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE class_sections (
    id VARCHAR(20) PRIMARY KEY,
    course_code VARCHAR(10) NOT NULL,
    semester_code VARCHAR(10) NOT NULL,
    lecturer_id VARCHAR(10) NOT NULL,
    capacity INTEGER NOT NULL,

    CONSTRAINT fk_sections_course
        FOREIGN KEY (course_code)
        REFERENCES courses(code),

    CONSTRAINT fk_sections_semester
        FOREIGN KEY (semester_code)
        REFERENCES semesters(code),

    CONSTRAINT fk_sections_lecturer
        FOREIGN KEY (lecturer_id)
        REFERENCES lecturers(id),

    CONSTRAINT ck_sections_capacity
        CHECK (capacity > 0)
);

CREATE TABLE enrollments (
    student_id VARCHAR(8) NOT NULL,
    class_section_id VARCHAR(20) NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_enrollments
        PRIMARY KEY (student_id, class_section_id),

    CONSTRAINT fk_enrollments_student
        FOREIGN KEY (student_id)
        REFERENCES students(id),

    CONSTRAINT fk_enrollments_section
        FOREIGN KEY (class_section_id)
        REFERENCES class_sections(id)
);
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
ORDER BY table_name;