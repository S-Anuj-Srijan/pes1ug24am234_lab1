# Lab 6: Code and Branch Coverage

**S Anuj Srijan — PES1UG24AM234**

Assigned repository: [Visa Application](https://github.com/SETAPESU26/L6_L7_52_visa_application/tree/main/Lab%206),
upstream commit `3321c388ecb5a18edc0ec409f74e509a001f2620`.

[visa_application.py](visa_application.py) retains the assigned implementation.
[baseline/test_visa_application.py](baseline/test_visa_application.py) preserves
the two starter tests. No branches are excluded or removed to improve coverage.

## Test submissions

| File | Purpose | Cases |
|---|---|---:|
| [CodeCoverageTest_visa_application.py](CodeCoverageTest_visa_application.py) | Execute every statement, including validation errors and all status returns | 11 |
| [BranchCoverageTest_visa_application.py](BranchCoverageTest_visa_application.py) | Exercise decisions, boundary values and nationality combinations | 44 |

The branch suite covers zero/included/extra entries, all three visa types,
group A's exception for students, normal and express rates, five versus six
extra entries, both invalid-input errors, renewal and new-document thresholds,
and all combinations of express processing and peak season. Deadline tests
check the cutoff, the day before it, the closing boundary and the day before
closure. Expected fees are explicit values, independent of the implementation.

## Reproduce the measurements

From the repository root:

```powershell
python -m pip install -r requirements-labs.txt
python scripts/verify_labs.py --lab 6
```

The script measures the baseline and each submission independently. Reports
include only `visa_application.py`, so executing test code cannot inflate the
application coverage. It saves text and JSON reports under `reports/` and
requires at least 90% line coverage and 90% of branch exits for the final suite.
Coverage percentages must be read from these measured reports, not inferred
from the number of passing tests.

## Measured results (24 November 2026)

| Suite | Lines executed | Branch exits taken |
|---|---:|---:|
| Starter tests | 14/37 (37.84%) | 6/26 (23.08%) |
| Code coverage tests | 37/37 (100%) | 25/26 (96.15%, separate branch measurement) |
| Branch coverage tests | 37/37 (100%) | 26/26 (100%) |

The branch-mode `Cover` column combines statements and branches. Its 32%
baseline and 98% code-suite values are not branch-only percentages.
The final branch suite has no missing statements or branch exits.

Saved output screenshots: [code](screenshots/code_coverage.png) and
[branch](screenshots/branch_coverage.png). These are explicitly labelled browser
report screenshots of real recorded stdout/stderr, **not native terminal captures**.
The native terminal window was unavailable to the capture tool. For the handout's
strict terminal-screenshot format, run `./scripts/show_evidence.ps1 coverage`
from the repository root and capture the displayed output. Alternatively,
run these commands from `lab6`:

```powershell
python -m coverage run --source=visa_application -m pytest CodeCoverageTest_visa_application.py -q
python -m coverage report -m
python -m coverage run --branch --source=visa_application -m pytest BranchCoverageTest_visa_application.py -q
python -m coverage report -m
```

Native terminal captures can replace the report screenshots in `screenshots/`.
Raw text, JSON coverage data and command metadata are available in `reports/`.

## Analysis

Line coverage records executed statements. Branch coverage records the exits
taken from decisions. The line suite intentionally does not cover the false
exit of the nested express condition for more than five extra entries; the
branch suite adds that normal-processing case. This demonstrates why executing
every statement does not establish complete branch coverage.

Function coverage asks whether each function was invoked. Path coverage asks
which combinations of decisions were followed and is stronger than branch
coverage. Neither full statement nor full branch coverage proves that all
requirements or all input types have been tested. These tests document the
assigned implementation, including its use of the normal rate for any speed
other than `express`; they are not real-world visa policy advice.
