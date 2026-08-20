# Use-Case Flow Specification

| Field | Specification |
|---|---|
| Use-case ID and name | UC-05 - Submit Timesheet for Approval |
| Scope | Remote Team Time-Tracking & Project Approver |
| Level | User goal |
| Primary actor | Remote Developer |
| Supporting actor | Engineering Manager |
| Trigger | The developer chooses **Submit for Approval** for a weekly draft timesheet. |

## Preconditions

1. The developer is authenticated and authorized for the project.
2. A draft timesheet exists for the selected work week.
3. A responsible engineering manager is assigned to the project.

## Postconditions

**Success guarantee:** The timesheet has status **Submitted**; its entries are locked against developer editing; the manager, submission timestamp, and audit event are recorded; and the manager is notified.

**Minimal guarantee:** If submission fails, the timesheet remains **Draft**, no entries are locked, and no approval request is created.

## Main Success Scenario

1. The developer opens the draft timesheet for the selected week.
2. The system displays all entries, the daily and weekly totals, and the assigned manager.
3. The developer selects **Submit for Approval**.
4. The system validates that every entry has a work date, positive duration, work note, and active Jira ticket, and that no daily total exceeds 24 hours.
5. The system asks the developer to confirm the weekly total and submission.
6. The developer confirms.
7. The system atomically changes the status from **Draft** to **Submitted** and locks its entries.
8. The system records the developer, manager, and submission timestamp in the audit history.
9. The system sends the approval request to the assigned engineering manager.
10. The system shows the developer a submission confirmation and the **Submitted** status.

## Alternate Flow A1 - Validation fails

At step 4, one or more entries are invalid:

1. The system does not create an approval request and keeps the timesheet in **Draft**.
2. The system identifies each invalid entry and explains the correction required (for example, missing work note, inactive Jira ticket, or daily total above 24 hours).
3. The developer corrects the entries.
4. The use case resumes at step 3 of the Main Success Scenario.

## Business rules

- BR-01: A developer's total logged duration must not exceed 24 hours in a calendar day in the project's configured time zone.
- BR-02: Only **Draft** or **Rejected** timesheets may be edited by a developer.
- BR-03: A submitted timesheet must be routed to the manager responsible for that project at submission time.

## Related requirements

FR-001, FR-002, FR-003, NFR-001, and NFR-002.
