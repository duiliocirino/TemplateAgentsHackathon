# log/ — one file per message to the team

Appending = creating a new file. Never edit or delete existing entries; corrections are new entries.
This makes coordination conflicts impossible: nobody ever writes the same file twice.

## Filename grammar — the filename IS the message

```
YYYY-MM-DD-HHMM_<handle>_<type>_<headline-slug>.md
```

- handle: `human-role-agent` (e.g. `valeria-fe-agent`) or `orchestrator`
- type: `claim | done | block | ask | decide | note | cr`
- headline: kebab-case, ≤60 chars — if you can't phrase the message this short, there is no message
- no secrets, IDs, or PII in filenames or bodies — record *where* a value lives, never the value

## Examples

```
2026-09-18-1801_valeria-fe-agent_done_T10-waitlist-notification-ui.md
2026-09-18-1805_valeria-fe-agent_block_T10-live-BFF-path-naming-mismatch.md
2026-09-18-1812_stefano-fs-agent_ask-orchestrator_T11-entra-config-who-owns.md
2026-09-18-1815_orchestrator_decide_T11-stefano-keeps-T2-closes.md
```

## Body — ≤10 lines

```
Task: T<n>
Evidence: <commit shas, test/build results>   (done entries: orchestrator verifies these against git)
What: 1–2 lines
Next: what you'll do next
Needs: who/what you need, if anything
```
