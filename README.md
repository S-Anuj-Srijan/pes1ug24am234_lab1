# Remote Team Time-Tracking & Project Approver

Software Engineering Lab 1 - Problem Statement 46

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
