"""Regression checks for security fixes and enrollment behavior."""
import copy
import hashlib

import pytest

import course_enrollment_system as app


@pytest.fixture(autouse=True)
def reset_state(monkeypatch):
    monkeypatch.setattr(app, "courses", copy.deepcopy(app.courses))
    monkeypatch.setattr(app, "tuition_ledger", {"total": 0.0})


def test_enrollment_capacity_and_audit():
    audit = []
    for name in ("A", "B", "C"):
        assert app.enroll_student("CS101", name, audit_trail=audit)
    assert not app.enroll_student("CS101", "D")
    assert app.courses["CS101"]["seats"] == 0
    assert app.tuition_ledger["total"] == 1500
    assert len(audit) == 3
    assert not app.check_course_status("CS101")


def test_unknown_and_closed_courses():
    assert not app.enroll_student("missing", "A")
    assert not app.enroll_student("CS202", "A")
    assert not app.drop_course("missing")
    assert app.drop_course("CS202")
    assert app.check_course_status("CS202")
    assert app.get_open_courses_summary(app.courses) == 3


def test_zero_seats_cannot_be_enrolled_even_if_flag_is_open():
    app.courses["CS101"]["seats"] = 0
    assert not app.enroll_student("CS101", "A")


def test_default_audit_is_not_shared():
    assert app.enroll_student.__defaults__ == (3, None)
    assert app.enroll_student("CS101", "A")
    audit = []
    assert app.enroll_student("CS101", "B", audit_trail=audit)
    assert len(audit) == 1
    assert "student B" in audit[0]


@pytest.mark.parametrize("multiplier,expected", [(0, 0), (0.75, 450), (1, 600)])
def test_scholarship(multiplier, expected):
    assert app.calculate_scholarship_tuition("CS303", multiplier) == expected


@pytest.mark.parametrize("multiplier", [-0.01, 1.01, float("nan"), float("inf")])
def test_invalid_multiplier(multiplier):
    with pytest.raises(ValueError):
        app.calculate_scholarship_tuition("CS303", multiplier)


def test_expression_is_rejected(tmp_path):
    marker = tmp_path / "executed"
    expression = f"__import__('pathlib').Path({str(marker)!r}).touch()"
    with pytest.raises(TypeError):
        app.calculate_scholarship_tuition("CS303", expression)
    assert not marker.exists()


def test_hash_and_otp_bounds(monkeypatch):
    assert app.generate_student_hash("roll") == hashlib.sha256(b"roll").hexdigest()
    monkeypatch.setattr(app.secrets, "randbelow", lambda limit: 0)
    assert app.generate_enrollment_otp() == 1000
    monkeypatch.setattr(app.secrets, "randbelow", lambda limit: limit - 1)
    assert app.generate_enrollment_otp() == 9999


def test_export_literal_filename(tmp_path):
    filename = tmp_path / "roster & echo injected.txt"
    app.export_course_roster(filename)
    assert "CS101" in filename.read_text(encoding="utf-8")


def test_main_does_not_print_token(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("REGISTRAR_AUTH_TOKEN", "test-private-value")
    app.main()
    output = capsys.readouterr().out
    assert "test-private-value" not in output
    assert "Scholarship Fee: 450.0" in output
    assert "Registrar Token configured: True" in output
