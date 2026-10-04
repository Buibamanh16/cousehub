student = [
    {
        "id": "24001722",
        "name": "Nguyen Son Tung",
        "major": "KHDL"
    },
    {
        "id": "24001668",
        "name": "Cao Trung Hieu",
        "major": "KHDL"
    },
]

courses = [
    {
        "code": "INT2204",
        "name": "Co so du lieu web",
        "capacity": 3,
        "enrolled": 2
    },
    {
        "code": "INT2205",
        "name": "Khai pha du lieu",
        "capacity": 2,
        "enrolled": 2
    },
]

enrollments = [
    {
        "student_id": "24001722",
        "course_code": "INT2204"
    }
]


for course in courses:
    remaining = course["capacity"] - course["enrolled"]
    print(course["code"], "- con", remaining, "cho")


def find_course(course_code):
    for course in courses:
        if course["code"] == course_code:
            return course
    return None


print(find_course("INT2204"))


def can_enroll(student_id, course_code):
    course = find_course(course_code)

    if course is None:
        return False, "Hoc phan khong ton tai"

    if course["enrolled"] >= course["capacity"]:
        return False, "Lop da du so luong"

    duplicated = any(
        item["student_id"] == student_id
        and item["course_code"] == course_code
        for item in enrollments
    )

    if duplicated:
        return False, "Sinh vien da dang ky hoc phan nay"

    return True, "Co the dang ky"


print(can_enroll("24001668", "INT2204"))


try:
    limit = int(input("Nhap so luong hoc phan muon hien thi: "))
    print(courses[:limit])
except ValueError:
    print("So luong phai la so nguyen")


def enroll_student(student_id, course_code):

    student_exists = any(
        s["id"] == student_id
        for s in student
    )

    if not student_exists:
        return False, "Sinh vien khong ton tai"

    course = find_course(course_code)

    if course is None:
        return False, "Hoc phan khong ton tai"

    duplicated = any(
        item["student_id"] == student_id
        and item["course_code"] == course_code
        for item in enrollments
    )

    if duplicated:
        return False, "Sinh vien da dang ky hoc phan nay"

    if course["enrolled"] >= course["capacity"]:
        return False, "Lop da du so luong"

    enrollments.append({
        "student_id": student_id,
        "course_code": course_code
    })

    course["enrolled"] += 1

    return True, "Dang ky thanh cong"


print("1. Dang ky thanh cong:")
print(enroll_student("24001668", "INT2204"))

print("2. Dang ky trung:")
print(enroll_student("24001722", "INT2204"))

print("3. Lop da day:")
print(enroll_student("24001722", "INT2205"))

print("4. Hoc phan khong ton tai:")
print(enroll_student("24001668", "INT9999"))

print("5. Sinh vien khong ton tai:")
print(enroll_student("99999999", "INT2204"))


def search_courses(keyword):
    normalized = keyword.strip().lower()
    results = []

    for course in courses:
        code = course["code"].lower()
        name = course["name"].lower()

        if normalized in code or normalized in name:
            results.append(course)

    return results


print(search_courses("web"))
