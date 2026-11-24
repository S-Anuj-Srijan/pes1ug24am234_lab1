# Software Engineering Labs — PES1UG24AM234

**S Anuj Srijan | Labs 1–7**

## Lab index

| Lab | Topic / project | Deliverables |
|---|---|---|
| 1 | Requirements engineering — Remote Team Time-Tracking & Project Approver | [Consolidated report](LAB1_DELIVERABLE.md), [PDF](deliverble/LAB1_DELIVERABLE.pdf), [requirements and UML](docs/) |
| 2 | Agile planning in Jira — Remote Team Time Tracker | [Epics, stories, timeline, workflow evidence and retrospective](lab_2/SE_Lab2_Jira_Deliverables.pdf) |
| 3 | Component modelling and architecture — Self-Service Coffee Kiosk | [Component diagram and layered architecture justification](lab3/SE_Lab3_Deliverables.pdf) |
| 4 | LLM-assisted debugging — Skyscraper Stack | [Instructions and fixes](lab_4/README.md), [source](lab_4/main.py), [before/after videos](lab_4/submision/), [conversation](lab_4/conversation.txt) |
| 5 | Static analysis — Course Enrollment System | [Lab report and run instructions](lab5/README.md), [fixed source](lab5/course_enrollment_system.py), [issues](lab5/issues.md), [reflection](lab5/reflection.md) |
| 6 | Line and branch coverage — Visa Application | [Analysis and run instructions](lab6/README.md), [line tests](lab6/CodeCoverageTest_visa_application.py), [branch tests](lab6/BranchCoverageTest_visa_application.py) |
| 7 | Fuzz testing — Visa Application | [Report and instructions](lab7/README.md), [PDF](lab7/SE_Lab7_FuzzTesting_Deliverables.pdf), [fixed source](lab7/visa_application.py), [Hypothesis tests](lab7/test_processor.py) |

## Run Labs 5, 6 and 7

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-labs.txt
$env:PYTEST_DEBUG_TEMPROOT = "$PWD/.pytest_tmp"
New-Item -ItemType Directory -Force .pytest_tmp | Out-Null
python -m pytest -q
python scripts/verify_labs.py
```

The full test suite has **103 passing cases**. Lab 5's final Pylint score is
**10.00/10**; Flake8 and Bandit report no findings. Lab 6 measured **100% line
coverage and 100% branch coverage**. Lab 7 records three failing fuzz properties
on the original and **33 passing tests** after fixes. Reports and labelled
browser screenshots of recorded output are included. Native terminal captures
remain a format requirement for Lab 6; reproduction scripts are included.

## Lab 1 — Remote Team Time-Tracking & Project Approver

Problem Statement 46

This repository contains the requirements-engineering and UML use-case modelling deliverables for an engineering productivity platform that records developer effort against Jira tickets, monitors project budget burn, and supports managerial timesheet approval.

## Deliverables

- [Single consolidated submission document](LAB1_DELIVERABLE.md) - contains all four required deliverables
- [Complete requirements table](docs/requirements.md) - exactly five functional and two non-functional requirements
- [UML use-case diagram](docs/use-case-diagram.md) - rendered on GitHub, with PlantUML source provided for UML tooling
- [Use-case flow specification](docs/use-case-flow.md) - core use case: Submit Timesheet for Approval
- [Original problem statement](46_SE_Lab1_SE_Problem_Statements.pdf)

## System scope

The system boundary includes task synchronization, time-entry management, timesheet submission and approval, budget monitoring, and notifications. Jira is modelled as an external supporting system. Payroll, invoicing, project planning, and Jira issue creation are outside scope.

## Traceability summary

| Requirement | Use case(s) |
|---|---|
| FR-001 | View Assigned Jira Tasks, Synchronize Jira Tasks |
| FR-002 | Log Time Entry, Validate Daily Hour Limit |
| FR-003 | Submit Timesheet, Validate Timesheet |
| FR-004 | Review Timesheet, Approve Timesheet, Reject Timesheet, Notify Developer |
| FR-005 | View Budget Burn Dashboard, Send Budget Alert |
