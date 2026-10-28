# Lab 5: Static Code Analysis

**S Anuj Srijan — PES1UG24AM234**

Assigned repository: [Course Enrollment System](https://github.com/SETAPESU26/L5_52_course_enrollment_system).
The original source is preserved under `baseline/`; the cleaned submission is
[course_enrollment_system.py](course_enrollment_system.py).

## Deliverables

- [Issue table and verification](issues.md)
- [Reflection answers](reflection.md)
- [Before reports](reports/before/)
- [After reports](reports/after/)
- [Regression tests](test_course_enrollment_system.py)

Three local commits separate Bandit security fixes, Pylint quality fixes and
Flake8 formatting fixes. See `git log --oneline -- lab5`.

## Run

From the repository root:

```powershell
python -m pip install -r requirements-labs.txt
python lab5/course_enrollment_system.py
python -m pytest lab5 -q
python scripts/verify_labs.py --lab 5
```

The verification script runs all three tools against both versions and saves
stdout, stderr and exit status separately. It does not execute the unsafe
baseline. The final security report requires Bandit to be installed.
