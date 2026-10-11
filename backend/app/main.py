
import logging
from .schemas import EnrollmentCreate
from fastapi import FastAPI, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Response
from .database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CourseHub API",
    description="API thuc hanh Buoi 3 - Co so du lieu Web va he thong thong tin",
    version="0.3.0",
)


@app.get("/")
def home():
    return {"message": "CourseHub API dang hoat dong"}


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("Khong ket noi duoc co so du lieu")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Khong ket noi duoc co so du lieu",
        )

    return {"status": "ok", "database": "connected"}


@app.get("/courses")
def list_courses(
    q: str | None = Query(default=None, min_length=1),
) -> list[dict[str, object]]:
    sql = """
        SELECT code, name, credits
        FROM courses
    """
    parameters: dict[str, object] = {}

    if q is not None:
        keyword = q.strip().lower()

        if not keyword:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tu khoa tim kiem khong duoc rong",
            )

        sql += """
            WHERE LOWER(code) LIKE :keyword
               OR LOWER(name) LIKE :keyword
        """
        parameters["keyword"] = f"%{keyword}%"

    sql += " ORDER BY code"

    with engine.connect() as connection:
        rows = connection.execute(
            text(sql), parameters
        ).mappings().all()

    return [dict(row) for row in rows]


@app.get("/courses/{course_code}")
def get_course(course_code: str) -> dict[str, object]:
    sql = """
        SELECT code, name, credits
        FROM courses
        WHERE LOWER(code) = LOWER(:course_code)
    """

    with engine.connect() as connection:
        row = connection.execute(
            text(sql),
            {"course_code": course_code},
        ).mappings().first()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khong tim thay mon hoc",
        )

    return dict(row)


@app.get("/sections")
def list_sections() -> list[dict[str, object]]:
    sql = """
        SELECT
            id,
            course_code,
            semester_code,
            lecturer_id,
            capacity
        FROM class_sections
        ORDER BY id
    """

    with engine.connect() as connection:
        rows = connection.execute(
            text(sql)
        ).mappings().all()

    return [dict(row) for row in rows]

@app.get("/students/{student_id}/enrollments")
def get_student_enrollments(
    student_id: str,
) -> list[dict[str, object]]:
    sql = """
        SELECT
            e.student_id,
            e.class_section_id,
            e.registered_at,
            cs.course_code,
            c.name AS course_name,
            cs.semester_code
        FROM enrollments AS e
        JOIN class_sections AS cs
            ON e.class_section_id = cs.id
        JOIN courses AS c
            ON cs.course_code = c.code
        WHERE e.student_id = :student_id
        ORDER BY e.registered_at, e.class_section_id
    """

    with engine.connect() as connection:
        rows = connection.execute(
            text(sql),
            {"student_id": student_id},
        ).mappings().all()

    return [dict(row) for row in rows]

@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate) -> dict[str, object]:
    sql = """
        INSERT INTO enrollments (student_id, class_section_id)
        VALUES (:student_id, :class_section_id)
        RETURNING student_id, class_section_id, registered_at
    """

    try:
        with engine.begin() as connection:
            row = connection.execute(
                text(sql),
                {
                    "student_id": enrollment.student_id,
                    "class_section_id": enrollment.class_section_id,
                },
            ).mappings().one()

        return dict(row)

    except SQLAlchemyError as exc:
        logger.exception("Khong the dang ky hoc phan")

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Dang ky that bai: sinh vien hoac lop hoc phan khong hop le, hoac da dang ky",
        ) from exc

@app.delete(
    "/enrollments/{student_id}/{class_section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_enrollment(
    student_id: str,
    class_section_id: str,
) -> Response:
    sql = """
        DELETE FROM enrollments
        WHERE student_id = :student_id
          AND class_section_id = :class_section_id
    """

    with engine.begin() as connection:
        result = connection.execute(
            text(sql),
            {
                "student_id": student_id,
                "class_section_id": class_section_id,
            },
        )

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khong tim thay dang ky can huy",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)