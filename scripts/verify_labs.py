"""Run the lab tools and preserve actual output without fabricating results."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(args, cwd, destination, allowed=(0,)):
    """Save a tool's output and metadata, then enforce expected exit codes."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    result = subprocess.run(
        [sys.executable, *args], cwd=cwd, env=env,
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(result.stdout, encoding="utf-8")
    destination.with_suffix(".stderr.txt").write_text(
        result.stderr, encoding="utf-8"
    )
    destination.with_suffix(".command.json").write_text(json.dumps({
        "command": ["python", *args],
        "working_directory": str(cwd.relative_to(ROOT)) or ".",
        "exit_code": result.returncode,
    }, indent=2), encoding="utf-8")
    print(result.stdout, end="")
    if result.returncode not in allowed:
        raise RuntimeError(f"Command failed: {args}\n{result.stderr}")


def static_analysis():
    for stage, source in (
        ("before", "baseline/course_enrollment_system.py"),
        ("after", "course_enrollment_system.py"),
    ):
        cwd = ROOT / "lab5"
        output = cwd / "reports" / stage
        for tool, options in (
            ("pylint", ["--persistent=n"]),
            ("bandit", ["-r", "-f", "txt"]),
            ("flake8", []),
        ):
            run(["-m", tool, *options, source], cwd,
                output / f"{tool}_report.txt",
                allowed=tuple(range(32)) if stage == "before" else (0,))
    run(["-m", "pytest", "test_course_enrollment_system.py", "-q"],
        ROOT / "lab5", ROOT / "lab5/reports/tests.txt")


def coverage_analysis():
    cwd = ROOT / "lab6"
    for label, test, branch in (
        ("baseline_line", "baseline/test_visa_application.py", False),
        ("baseline_branch", "baseline/test_visa_application.py", True),
        ("code", "CodeCoverageTest_visa_application.py", False),
        ("code_with_branches", "CodeCoverageTest_visa_application.py", True),
        ("branch", "BranchCoverageTest_visa_application.py", True),
    ):
        output = cwd / "reports" / label
        args = ["-m", "coverage", "run", "--source=visa_application"]
        if branch:
            args.append("--branch")
        run([*args, "-m", "pytest", test, "-q"], cwd, output / "tests.txt")
        run(["-m", "coverage", "report", "-m"], cwd, output / "coverage.txt")
        run(["-m", "coverage", "json", "-o", str(output / "coverage.json")],
            cwd, output / "export.txt")
        totals = json.loads((output / "coverage.json").read_text())["totals"]
        if label in ("code", "branch"):
            line_ratio = totals["covered_lines"] / totals["num_statements"]
            if line_ratio < 0.9:
                raise RuntimeError(f"{label}: line coverage is below 90%")
        if label == "branch":
            branch_ratio = totals["covered_branches"] / totals["num_branches"]
            if branch_ratio < 0.9:
                raise RuntimeError("Branch coverage is below 90%")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lab", choices=("5", "6", "all"), default="all")
    args = parser.parse_args()
    dependencies = ["pytest"]
    if args.lab in ("5", "all"):
        dependencies += ["pylint", "bandit", "flake8"]
    if args.lab in ("6", "all"):
        dependencies.append("coverage")
    missing = [name for name in dependencies
               if importlib.util.find_spec(name) is None]
    if missing:
        parser.exit(2, "Missing dependencies: " + ", ".join(missing)
                    + "\nRun: python -m pip install -r requirements-labs.txt\n")
    if args.lab in ("5", "all"):
        static_analysis()
    if args.lab in ("6", "all"):
        coverage_analysis()


if __name__ == "__main__":
    main()
