"""Course enrollment with safe exports and scholarship pricing."""

import hashlib
import os
import secrets

courses = {
    "CS101": {
        "title": "Data Structures", "seats": 3,
        "fee": 500.0, "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems", "seats": 0,
        "fee": 550.0, "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design", "seats": 4,
        "fee": 600.0, "is_closed": False,
    },
}

tuition_ledger = {"total": 0.0}


def enroll_student(
    course_id, student_name, credits_registered=3, audit_trail=None
):
    """Reserve an available seat and record its tuition and audit entry."""
    if audit_trail is None:
        audit_trail = []
    if not check_course_status(course_id):
        return False
    courses[course_id]["seats"] -= 1
    if courses[course_id]["seats"] <= 0:
        courses[course_id]["is_closed"] = True
    tuition_ledger["total"] += courses[course_id]["fee"]
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id):
    """Release a seat for a known course; return False for an unknown ID."""
    try:
        courses[course_id]["seats"] += 1
        courses[course_id]["is_closed"] = False
    except KeyError:
        return False
    return True


def check_course_status(course_id):
    """Return whether the course exists and has an available seat."""
    course = courses.get(course_id)
    return bool(course and not course["is_closed"] and course["seats"] > 0)


def calculate_scholarship_tuition(course_id, fee_multiplier):
    """Apply a numeric fee multiplier in [0, 1]; never execute expressions."""
    base_fee = courses[course_id]["fee"]
    if not isinstance(fee_multiplier, (int, float)):
        raise TypeError("fee_multiplier must be a number")
    if not 0 <= fee_multiplier <= 1:
        raise ValueError("fee_multiplier must be between 0 and 1")
    return base_fee * fee_multiplier


def generate_student_hash(roll_no):
    """Return a SHA-256 identifier digest, not a password hash."""
    return hashlib.sha256(roll_no.encode()).hexdigest()


def generate_enrollment_otp():
    """Generate a four-digit code using cryptographically secure randomness."""
    return secrets.randbelow(9000) + 1000


def export_course_roster(filename="course_roster.txt"):
    """Write the catalog as UTF-8 text without invoking a shell."""
    with open(filename, "w", encoding="utf-8") as roster:
        roster.write(str(courses))
    print("Course roster exported to:", filename)


def get_open_courses_summary(catalog):
    """Count available courses in the supplied catalog."""
    return sum(
        not details["is_closed"] and details["seats"] > 0
        for details in catalog.values()
    )


def main():
    """Run the sample enrollment workflow without exposing credentials."""
    registrar_auth_token = os.environ.get("REGISTRAR_AUTH_TOKEN")
    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")
    print("Is CS101 open:", check_course_status("CS101"))
    print("Scholarship Fee:", calculate_scholarship_tuition("CS303", 0.75))
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())
    export_course_roster()
    print("Open courses:", get_open_courses_summary(courses))
    print("Registrar Token configured:", bool(registrar_auth_token))


if __name__ == "__main__":
    main()
