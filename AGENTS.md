# AGENTS.md — multi-agent protocol (v2)

Protocol for humans + AI agents working in parallel on this repo, from any machine, any tool.
The *how* is here. The *what* lives in [docs/BOARD.md](docs/BOARD.md) and [docs/tasks/](docs/tasks/).

## Who you are — declare at session start

First message of every session: `I am <name>, <role>. Follow AGENTS.md.`
Your handle = `<name>-<role>-agent` (e.g. `vale-fe-agent`, `fabio-db-agent`). `git config user.name` tells you whose machine you are on — confirm it matches the declared name.
The orchestrator session boots differently: `You are the orchestrator. Follow docs/ORCHESTRATOR.md.`

## Startup ritual — every session, every machine, no exceptions

1. Run `scripts/sync` (pull --rebase --autostash + status + recent log headlines + recent commits).
2. Read `docs/BOARD.md` — the current state. Generated; never hand-edit it.
3. Read your `docs/status/<handle>.md` if it exists — your handoff from the last session.
4. Read the task files you own in `docs/tasks/`.

Then work. Do not read more than this unless a log headline tells you to. Context is a budget, not a dump.

## Write matrix — who may write what

| Artifact | Writers | Rule |
|---|---|---|
| `docs/log/<new file>` | anyone | create only, never edit or delete |
| `docs/status/<handle>.md` | that handle only | your memory + handoff |
| `docs/tasks/*` | orchestrator only | definitions frozen during the day |
| `docs/BOARD.md` | orchestrator only | cache, regenerated every ≤10 min |
| code | everyone | only inside your task's `Scope:` |

Never edit a file another handle owns. Need something changed there? Write a log entry instead.

## Log grammar — the filename IS the message

`docs/log/YYYY-MM-DD-HHMM_<handle>_<type>_<headline-slug>.md`
type ∈ `claim | done | block | ask | decide | note | cr`. Headline: kebab-case, ≤60 chars.
Body ≤10 lines: Task, Evidence (commits/tests), What, Next, Needs.
No secrets, IDs, or PII in filenames or bodies — record *where* a value lives, never the value.

## Git is your job — autonomously, no human prompting

- Run `scripts/sync` before starting and before every push.
- Commit + push each completed unit of work yourself, unprompted. Small and often.
- After each task unit: write your log entry (`done`/`block`) + update your status file, same push.
- Never force-push. Never edit old log files.

## Claims — self-service, optimistic

Want a task: write a `claim` log entry + update your status file, start immediately.
The orchestrator ratifies it on the board within ~10 min. First claim wins unless a `decide` entry says otherwise.

## Hard rules

- BOARD.md is the only shared status file and it is a cache — if it's stale or the orchestrator is down, restart the orchestrator (anyone: new session + "Follow docs/ORCHESTRATOR.md").
- Organizers WILL change requirements mid-event. Do not react ad hoc: the orchestrator runs the CR playbook in docs/ORCHESTRATOR.md.
- When in doubt, write an `ask` log entry instead of guessing silently.
