# T<n> — <short imperative name>

Written by the orchestrator at planning time. Definitions are frozen during the day;
state (Owner/Status) is maintained by the orchestrator when it ratifies claims/decisions.
Owners never edit these files — claim via a log entry.

```
Owner:  —            (orchestrator sets this on a ratified claim)
Status: open         (open | claimed | in-progress | done | blocked)
Scope:  <paths this task may write, e.g. apps/web/**>
Depends: <task ids, or none>
```

## Definition of done

- [ ] acceptance criteria, contract references, tests required — concrete enough that
      the orchestrator can verify "done" against git evidence without asking you
