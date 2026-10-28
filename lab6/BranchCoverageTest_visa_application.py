"""Branch and boundary checks, including the compound nationality condition."""
import pytest

from visa_application import application_status, documents_complete, visa_fee


@pytest.mark.parametrize("visa_type,entries,speed,group,expected", [
    ("tourist", 0, "normal", "B", 0),
    ("tourist", 1, "normal", "B", 0),
    ("tourist", 2, "normal", "B", 40),
    ("tourist", 2, "express", "A", 0),
    ("tourist", 3, "express", "A", 100),
    ("business", 3, "normal", "B", 0),
    ("business", 4, "normal", "A", 0),
    ("business", 5, "normal", "A", 40),
    ("student", 2, "normal", "A", 0),
    ("student", 3, "normal", "A", 40),
    ("tourist", 6, "normal", "B", 200),
    ("tourist", 7, "normal", "B", 360),
    ("tourist", 6, "express", "B", 500),
    ("tourist", 7, "express", "B", 780),
])
def test_fee_branches(visa_type, entries, speed, group, expected):
    assert visa_fee(visa_type, entries, speed, group) == expected


@pytest.mark.parametrize("visa_type,entries,message", [
    ("invalid", 1, "unknown visa type"),
    ("tourist", -1, "invalid entries"),
])
def test_invalid_inputs(visa_type, entries, message):
    with pytest.raises(ValueError, match=message):
        visa_fee(visa_type, entries, "normal", "B")


@pytest.mark.parametrize("forms,photos,renewal,expected", [
    (0, 0, True, False), (1, 0, True, True), (2, 0, True, True),
    (3, 1, False, False), (2, 2, False, False), (3, 2, False, True),
    (4, 3, False, True), (0, 0, False, False),
])
def test_document_boundaries(forms, photos, renewal, expected):
    assert documents_complete(forms, photos, renewal) is expected


@pytest.mark.parametrize("express,peak,cutoff", [
    (True, False, 10), (True, True, 25),
    (False, False, 30), (False, True, 45),
])
@pytest.mark.parametrize("offset,expected", [
    (1, "open"), (0, "open"), (-1, "closing"),
    (-15, "closing"), (-16, "closed"),
])
def test_status_boundaries(express, peak, cutoff, offset, expected):
    assert application_status(cutoff + offset, express, peak) == expected
