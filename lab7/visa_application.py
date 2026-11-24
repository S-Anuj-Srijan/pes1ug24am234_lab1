"""Visa input parsers: invalid input returns None instead of crashing.

Text is limited to 10,000 characters. Entries and days are nonnegative
integers; fees and discounts are finite, nonnegative numbers. The starter's
floor-average and 18% fee uplift are retained.
"""

import math


def _parts(value, separator, count=None):
    if not isinstance(value, str) or not value or len(value) > 10000:
        return None
    parts = [part.strip() for part in value.split(separator)]
    if any(not part for part in parts):
        return None
    if count is not None and len(parts) != count:
        return None
    return parts


def _nonnegative_int(value):
    if len(value) > 100 or not value.isascii() or not value.isdecimal():
        return None
    return int(value)


def parse_application(text):
    """Parse a nonempty visa label and a nonnegative entry count."""
    parts = _parts(text, ':', 2)
    if parts is None:
        return None
    visa, raw_entries = parts
    entries = _nonnegative_int(raw_entries)
    if entries is None:
        return None
    return visa.title(), entries


def processing_average(days_csv):
    """Return the floor mean of a nonempty CSV of nonnegative days."""
    parts = _parts(days_csv, ',')
    if parts is None:
        return None
    values = [_nonnegative_int(part) for part in parts]
    if any(value is None for value in values):
        return None
    return sum(values) // len(values)


def payable_fee(text):
    """Return max(fee * 1.18 - discount, 0), or None for invalid input."""
    parts = _parts(text, '|', 2)
    if parts is None:
        return None
    try:
        fee, discount = map(float, parts)
    except (ValueError, OverflowError):
        return None
    if not all(math.isfinite(x) and x >= 0 for x in (fee, discount)):
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0.0)


def main():
    """Run the three prompts, reporting invalid input without a traceback."""
    prompts = (
        ('parse_application', 'Enter visa type:entries (e.g. tourist:2): ',
         'Visa Type and Entries:', parse_application),
        ('processing_average', 'Enter processing days as CSV (e.g. 5,10,21): ',
         'Average Processing Days:', processing_average),
        ('payable_fee', 'Enter fee|discount (e.g. 6000|500): ',
         'Payable Fee:', payable_fee),
    )
    for name, prompt, label, function in prompts:
        print(f'==== Running {name} ====')
        try:
            result = function(input(prompt))
        except EOFError:
            print('Input ended.')
            return
        print(label, 'Invalid input' if result is None else result)


if __name__ == '__main__':
    main()
