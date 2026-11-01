
import logging

from fastapi import FastAPI, HTTPException, Query, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .database import engine
from .schemas import EnrollmentCreate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="CourseHub API",
    version="0.4.0",
    description="API thuc hanh Buoi 4 - transaction, locking va hieu nang",
)


@app.get("/")
def home():
    return {"message": "CourseHub API dang hoat dong"}


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    except SQLAlchemyError as exc:
        logger.exception("Khong ket noi duoc co so du lieu")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Khong ket noi duoc co so du lieu",
        ) from exc

    return {
        "status": "ok",
        "database": "connected",
    }


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
            text(sql),
            parameters,
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
            class_id,
            capacity,
            enrolled,
            remaining
        FROM v_section_summary
        ORDER BY class_id
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


@app.post(
    "/enrollments",
    status_code=status.HTTP_201_CREATED,
)
def create_enrollment(
    enrollment: EnrollmentCreate,
) -> dict[str, object]:

    parameters = {
        "student_id": enrollment.student_id,
        "class_section_id": enrollment.class_section_id,
    }

    try:
        with engine.begin() as connection:

            # 1. Kiem tra sinh vien
            student = connection.execute(
                text("""
                    SELECT id
                    FROM students
                    WHERE id = :student_id
                """),
                {"student_id": enrollment.student_id},
            ).first()

            if student is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Khong tim thay sinh vien",
                )

            # 2. Khoa lop hoc phan
            section = connection.execute(
                text("""
                    SELECT id, capacity
                    FROM class_sections
                    WHERE id = :class_section_id
                    FOR UPDATE
                """),
                {
                    "class_section_id": enrollment.class_section_id,
                },
            ).mappings().first()

            if section is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Khong tim thay lop hoc phan",
                )

            # 3. Kiem tra dang ky trung
            duplicated = connection.execute(
                text("""
                    SELECT 1
                    FROM enrollments
                    WHERE student_id = :student_id
                      AND class_section_id = :class_section_id
                """),
                parameters,
            ).first()

            if duplicated is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Sinh vien da dang ky lop nay",
                )

            # 4. Kiem tra suc chua
            enrolled = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM enrollments
                    WHERE class_section_id = :class_section_id
                """),
                {
                    "class_section_id": enrollment.class_section_id,
                },
            ).scalar_one()

            if enrolled >= section["capacity"]:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Lop hoc phan da het cho",
                )

            # 5. Them dang ky
            row = connection.execute(
                text("""
                    INSERT INTO enrollments
                        (student_id, class_section_id)
                    VALUES
                        (:student_id, :class_section_id)
                    RETURNING
                        student_id,
                        class_section_id,
                        registered_at
                """),
                parameters,
            ).mappings().one()

            # 6. Ghi lich su dang ky
            connection.execute(
                text("""
                    INSERT INTO enrollment_events
                        (
                            student_id,
                            class_section_id,
                            event_type,
                            source,
                            dataset
                        )
                    VALUES
                        (
                            :student_id,
                            :class_section_id,
                            'CREATED',
                            'api',
                            'demo'
                        )
                """),
                parameters,
            )

        return dict(row)

    except HTTPException:
        raise

    except SQLAlchemyError as exc:
        logger.exception("Khong the dang ky hoc phan")

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Dang ky that bai do xung dot du lieu",
        ) from exc


@app.delete(
    "/enrollments/{student_id}/{class_section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_enrollment(
    student_id: str,
    class_section_id: str,
) -> Response:

    parameters = {
        "student_id": student_id,
        "class_section_id": class_section_id,
    }

    try:
        with engine.begin() as connection:

            # 1. Khoa lop hoc phan
            section = connection.execute(
                text("""
                    SELECT id
                    FROM class_sections
                    WHERE id = :class_section_id
                    FOR UPDATE
                """),
                {
                    "class_section_id": class_section_id,
                },
            ).first()

            if section is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Khong tim thay lop hoc phan",
                )

            # 2. Xoa dang ky
            deleted = connection.execute(
                text("""
                    DELETE FROM enrollments
                    WHERE student_id = :student_id
                      AND class_section_id = :class_section_id
                    RETURNING student_id
                """),
                parameters,
            ).first()

            if deleted is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Khong tim thay dang ky can huy",
                )

            # 3. Ghi lich su huy dang ky
            connection.execute(
                text("""
                    INSERT INTO enrollment_events
                        (
                            student_id,
                            class_section_id,
                            event_type,
                            source,
                            dataset
                        )
                    VALUES
                        (
                            :student_id,
                            :class_section_id,
                            'CANCELLED',
                            'api',
                            'demo'
                        )
                """),
                parameters,
            )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
        )

    except HTTPException:
        raise

    except SQLAlchemyError as exc:
        logger.exception("Khong the huy dang ky hoc phan")

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Huy dang ky that bai do xung dot du lieu",
        ) from exc
