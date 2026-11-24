# Lab 7: Fuzz Testing - Visa Application

**S Anuj Srijan | PES1UG24AM234**

Reference: [assigned Lab 7 repository](https://github.com/SETAPESU26/L6_L7_52_visa_application/tree/5fff7c811cbd03f4611e80cac0ca7624c9ae30b8/Lab%207).
The original application and incomplete starter test are preserved in `baseline/`.

## Deliverables

- [Screenshot PDF and analysis](SE_Lab7_FuzzTesting_Deliverables.pdf)
- [Fixed application](visa_application.py)
- [Completed Hypothesis tests](test_processor.py)
- [Recorded output and commands](reports/)
- [Output screenshots](screenshots/)

The handout's `processor.py` is a generic example name. This submission retains
the assigned `visa_application.py` name and uses `test_processor.py` for tests.

## Results

On 24 November 2026, Hypothesis 6.170.17 found failures in **all three** original
functions. Minimized inputs include `None`, `''` and `b''`; the complete tracebacks
are in [before_fuzz.txt](reports/before_fuzz.txt). The exact same no-crash tests
pass against the fixed source. The full fixed suite has **33 passing tests**:
six property tests (up to 300 examples per property, deterministic generation)
and 27 explicit regression/size-limit cases.

| Function | Original problem | Fix |
|---|---|---|
| `parse_application` | Wrong types, missing/extra separators, invalid entry counts | Validate string and two nonempty fields; require nonnegative ASCII integer entries |
| `processing_average` | Empty input/tokens, wrong types and invalid day values | Validate a nonempty CSV of nonnegative integers before averaging |
| `payable_fee` | Invalid floats, negative values, NaN/infinity and overflow | Validate two finite nonnegative numbers and finite arithmetic result |

All functions return `None` for invalid input; the CLI displays `Invalid input`
and continues. Text is limited to 10,000 characters and integer tokens to 100
digits. These are explicit defensive limits chosen for this exercise, not visa
policy. Valid inputs retain the starter's floor average, 18% fee uplift and
zero floor after discount. No broad exception handler hides unexpected defects.

Valid sample outputs: `tourist:2` -> `('Tourist', 2)`, `5,10,21` -> `12`,
and `6000|500` -> `6580.0`. Empty lines crash the original but are handled by the fix.

## Reproduce

From the repository root, with the virtual environment active:

```powershell
python -m pip install -r requirements-labs.txt
python scripts/verify_labs.py --lab 7
python -m pytest lab7/test_processor.py -q
```

The verifier expects exit code 1 for the original crash/fuzz demonstrations and
exit code 0 for the fixed runs. It records stdout, stderr, stdin, command,
working directory, target-selection environment and exit code separately.
Tests load their target by absolute path to avoid confusing Lab 6's same-named module.

## Screenshot format

The PDF contains browser screenshots of real saved command output, clearly
labelled as report views. They are **not native terminal captures**; the terminal
window was unavailable to the capture tool. Full tracebacks remain in the text
reports; the fuzz-failure screenshot is explicitly marked as an excerpt.
For native-terminal captures, run these from the root:

```powershell
./scripts/show_evidence.ps1 demo
./scripts/show_evidence.ps1 fuzz
```

To regenerate the report images and PDF, install `playwright`, `reportlab` and
`pillow` in the rendering Python environment, with Microsoft Edge installed,
then run `python scripts/build_evidence.py`.
