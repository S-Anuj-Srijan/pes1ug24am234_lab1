"""Run identical fuzz properties against the original or fixed module.

LAB7_TARGET=baseline selects the preserved original for failure evidence.
"""
import importlib.util
import math
import os
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

target = Path(__file__).parent
if os.environ.get('LAB7_TARGET') == 'baseline':
    target /= 'baseline'
spec = importlib.util.spec_from_file_location(
    'lab7_target', target / 'visa_application.py'
)
application = importlib.util.module_from_spec(spec)
spec.loader.exec_module(application)

settings.register_profile('lab7', max_examples=300, derandomize=True,
                          deadline=None, database=None)
settings.load_profile('lab7')

inputs = st.one_of(st.none(), st.text(), st.integers(), st.floats(),
                   st.binary(), st.lists(st.integers(), max_size=10),
                   st.dictionaries(st.text(max_size=10), st.integers(),
                                   max_size=5))


@given(inputs)
def test_parse_application_no_crash(value):
    result = application.parse_application(value)
    assert result is None or (
        isinstance(result, tuple) and len(result) == 2
        and isinstance(result[0], str) and bool(result[0].strip())
        and isinstance(result[1], int) and result[1] >= 0
    )


@given(inputs)
def test_processing_average_no_crash(value):
    result = application.processing_average(value)
    assert result is None or isinstance(result, int) and result >= 0


@given(inputs)
def test_payable_fee_no_crash(value):
    result = application.payable_fee(value)
    assert result is None or math.isfinite(result) and result >= 0


@given(st.sampled_from(['tourist', 'business', 'student']),
       st.integers(min_value=0, max_value=10**12))
def test_valid_application(visa, entries):
    assert application.parse_application(f' {visa} : {entries} ') == (
        visa.title(), entries
    )


@given(st.lists(st.integers(min_value=0, max_value=10**12),
                min_size=1, max_size=100))
def test_valid_processing_average(days):
    result = application.processing_average(','.join(map(str, days)))
    assert result == sum(days) // len(days)
    assert min(days) <= result <= max(days)


@given(st.integers(min_value=0, max_value=10**9),
       st.integers(min_value=0, max_value=10**9))
def test_valid_payable_fee(fee, discount):
    assert application.payable_fee(f'{fee}|{discount}') == pytest.approx(
        max(fee * 1.18 - discount, 0)
    )


@pytest.mark.parametrize('name,value', [
    ('parse_application', ''), ('parse_application', None),
    ('parse_application', 'tourist'), ('parse_application', 'a:1:2'),
    ('parse_application', ':2'), ('parse_application', 'tourist:-1'),
    ('parse_application', 'tourist:1.5'),
    ('parse_application', 'tourist:' + '9' * 5000),
    ('processing_average', ''), ('processing_average', None),
    ('processing_average', '1,,3'), ('processing_average', '-1,2'),
    ('processing_average', '1,hello'), ('processing_average', '1.5,2'),
    ('payable_fee', ''), ('payable_fee', None),
    ('payable_fee', '1|2|3'), ('payable_fee', 'nan|0'),
    ('payable_fee', 'inf|0'), ('payable_fee', '0|inf'),
    ('payable_fee', '-1|0'), ('payable_fee', '1|-1'),
    ('payable_fee', '1.79e308|0'), ('payable_fee', 'hello|0'),
])
def test_invalid_input_returns_none(name, value):
    assert getattr(application, name)(value) is None


@pytest.mark.parametrize('name', [
    'parse_application', 'processing_average', 'payable_fee'
])
def test_input_size_limit(name):
    assert getattr(application, name)('1' * 10001) is None
