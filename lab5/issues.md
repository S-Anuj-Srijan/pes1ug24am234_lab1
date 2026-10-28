# Lab 5 issue report

S Anuj Srijan | PES1UG24AM234 | Course Enrollment System

Line numbers below refer to the preserved `baseline/course_enrollment_system.py`.
Pylint and Flake8 findings were measured locally. Bandit rule IDs below identify
the relevant checks; the Bandit run must confirm the final security results.

| Issue | Type / tool | Original line(s) | Description | Fix approach |
|---|---|---|---|---|
| Shell injection | High / Bandit B605 | 63 | A filename is concatenated into an operating-system command. | Print the message directly; never start a shell. |
| Weak digest | High / Bandit B324 | 52 | MD5 is unsuitable for security-sensitive hashing. | Use SHA-256 for identifier digests. This is not a password-storage function. |
| Arbitrary evaluation | Medium / Bandit B307, Pylint W0123 | 47 | A scholarship expression can execute Python code. | Replace expression strings with a numeric fee multiplier between 0 and 1. |
| Shared audit list | Bug / Pylint W0102 | 15 | The mutable default persists across calls. | Default to `None` and initialize a fresh list. Caller-supplied lists are retained. |
| Swallowed exceptions | Bandit B110, Pylint W0702 | 28-32 | Bare `except: pass` hides failures. | Catch `KeyError` specifically and return `False` for an unknown course. |
| Predictable OTP | Bandit B311 | 56 | `random.randint` is not a cryptographic random generator. | Use `secrets.randbelow(9000) + 1000`. |
| Embedded credential | Bandit B105; manual output review | 75, 84 | A sample registrar token is hardcoded and printed. | Read an environment variable and print only whether it is configured. |
| Resource management | Pylint R1732 / W1514 | 60-62 | File closure is manual and encoding implicit. | Use a context manager and explicit UTF-8 encoding. |
| Naming and unused values | Pylint C0103 / W0611 / W0612 / W0621 | 4, 12, 15-68 | Camel-case functions, unused variables and shadowed names obscure intent. | Use snake_case, remove unused values, and name the supplied catalog separately. |
| Redundant conditional | Pylint C0121 / R1703 / R1705 | 37-42 | Equality comparison with None and redundant boolean branches. | Return a boolean availability check including the seat count. |
| Long lines | Flake8 E501 | 7-9, 23, 79 | Long literals and calls exceed the style limit. | Wrap catalog entries, function signatures and audit text. |
| Import side effects | Manual review | 87 | Importing the module runs the demonstration and writes a file. | Add a `__main__` guard. |

## Verification and interface changes

- Pylint baseline: **4.17/10**; cleaned source: **10.00/10**.
- Final Flake8 scan: **no findings**, using its default 79-character limit.
- Security regression tests check expression rejection, literal export filenames,
  secret redaction, secure OTP bounds and the SHA-256 result.
- Enrollment tests check capacity, unknown/closed courses, audit entries and tuition.
- Functions now use snake_case. Scholarship calls pass `0.75`, rather than
  `"base_fee * 0.75"`. The example still yields **450.0** for CS303.
- Accumulated tuition is exposed as `tuition_ledger["total"]`.

The preserved original contains intentionally unsafe examples and is only used
as input to static analysis. The fixed module is the runnable submission.
This teaching program does not maintain individual enrollment records, enforce
authenticated access or model refunds. Its drop operation releases one seat for
a known course, as in the starter program. Static-analysis success does not
establish production readiness.
