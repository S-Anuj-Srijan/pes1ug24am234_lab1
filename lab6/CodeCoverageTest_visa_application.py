"""Statement coverage tests for the assigned, unchanged application."""

import pytest

from visa_application import application_status, documents_complete, visa_fee


@pytest.mark.parametrize("visa_type,entries,speed,group,expected", [
    ("tourist", 1, "normal", "B", 0),
    ("tourist", 3, "normal", "A", 40),
    ("student", 8, "express", "A", 780),
])
def test_fee_statements(visa_type, entries, speed, group, expected):
    assert visa_fee(visa_type, entries, speed, group) == expected


@pytest.mark.parametrize("visa_type,entries,message", [
    ("unknown", 1, "unknown visa type"),
    ("tourist", -1, "invalid entries"),
])
def test_fee_errors(visa_type, entries, message):
    with pytest.raises(ValueError, match=message):
        visa_fee(visa_type, entries, "normal", "B")


@pytest.mark.parametrize("forms,photos,renewal,expected", [
    (1, 0, True, True),
    (3, 1, False, False),
    (3, 2, False, True),
])
def test_document_statements(forms, photos, renewal, expected):
    assert documents_complete(forms, photos, renewal) is expected


@pytest.mark.parametrize("days,express,peak,expected", [
    (25, True, True, "open"),
    (15, False, False, "closing"),
    (14, False, False, "closed"),
])
def test_status_statements(days, express, peak, expected):
    assert application_status(days, express, peak) == expected
