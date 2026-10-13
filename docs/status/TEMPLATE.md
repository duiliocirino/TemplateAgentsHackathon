# <handle> — owner-only file

Update this in the same push as your log entries. A fresh agent session on your machine reads it
first: it is your handoff, so "Handoff" must contain what a stranger needs (env quirks, gotchas,
where things live, what you tried that failed).

```
Working on: T<n> (since HH:MM)
Done:       T<n> (commit <sha>, <evidence: tests/build/contract>)
Blocked:    <what | on whom | since when>
Handoff:    <what a fresh session on this machine must know>
```
