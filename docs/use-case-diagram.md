# UML Use-Case Diagram

The diagram models the two human stakeholders and Jira as a supporting external system. Solid arrows indicate actor participation; dotted labelled arrows indicate UML relationships.

```mermaid
flowchart LR
    DEV[Remote Developer]
    MGR[Engineering Manager]
    JIRA[Jira]

    subgraph SYS[Remote Team Time-Tracking & Project Approver]
      SYNC([Synchronize Jira Tasks])
      VIEW([View Assigned Jira Tasks])
      LOG([Log Time Entry])
      LIMIT([Validate Daily Hour Limit])
      SUBMIT([Submit Timesheet])
      VALIDATE([Validate Timesheet])
      REVIEW([Review Timesheet])
      APPROVE([Approve Timesheet])
      REJECT([Reject Timesheet])
      NOTIFY([Notify Developer])
      BUDGET([View Budget Burn Dashboard])
      ALERT([Send Budget Alert])
    end

    DEV --> VIEW
    DEV --> LOG
    DEV --> SUBMIT
    MGR --> REVIEW
    MGR --> APPROVE
    MGR --> REJECT
    MGR --> BUDGET
    JIRA --> SYNC

    VIEW -. "«include»" .-> SYNC
    LOG -. "«include»" .-> LIMIT
    SUBMIT -. "«include»" .-> VALIDATE
    APPROVE -. "«extend»" .-> REVIEW
    REJECT -. "«extend»" .-> REVIEW
    APPROVE -. "«include»" .-> NOTIFY
    REJECT -. "«include»" .-> NOTIFY
    ALERT -. "«extend» [threshold crossed]" .-> BUDGET
```

The equivalent editable PlantUML source is in [use-case-diagram.puml](use-case-diagram.puml).

## Relationship rationale

- `Log Time Entry` always invokes `Validate Daily Hour Limit`, so `«include»` is used.
- `Submit Timesheet` always invokes `Validate Timesheet`, so `«include»` is used.
- Approval and rejection are alternative outcomes available while reviewing a submitted timesheet, so each `«extend»`s `Review Timesheet`.
- `Send Budget Alert` occurs conditionally when a threshold is crossed, so it `«extend»`s `View Budget Burn Dashboard`.
