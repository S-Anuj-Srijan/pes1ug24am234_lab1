from hypothesis import given, strategies as st
from visa_application import parse_application, processing_average, payable_fee

@given(st.text() | st.none())
def test_parse_application_no_crash(s):

@given(st.text() | st.none())
def test_processing_average_no_crash(s):

@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
