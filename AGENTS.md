# AGENTS.md

Working protocol for AI agents and humans in this repository.
This file is short on purpose: it defines the *how*. The *what* lives in [docs/PLAN.md](docs/PLAN.md).

## On startup — every session, every machine, no exceptions

1. `git pull --rebase`
2. Read `docs/PLAN.md` in full (goal, current state, task ownership).
3. Read the last ~50 lines of `docs/DISCUSSION.md` (recent decisions and handoffs).
4. Skim `git log --oneline -20` (what actually changed recently).

Only then start working. Recent entries and commits tell you what your teammates and other agents are doing.

## Coordination model

- **One task, one owner.** Owners are named in `docs/PLAN.md` (human name or agent handle).
- **Claim** = set the owner in PLAN.md + append a claim entry to DISCUSSION.md + commit.
- **Complete** = mark the task done in PLAN.md + update "Current state" + append a completion entry (what changed, why, what's left) + commit.
- **Do not touch** files that are the primary target of someone else's active task. If you must, coordinate in DISCUSSION.md first.
- **Small, frequent commits to `main`.** Every commit leaves the repo in a consistent state. The commit log is a first-class communication channel: write it like someone else will read it 10 minutes from now.
- **Stale work is re-claimable.** If an owner went quiet and a task blocks progress, note it in DISCUSSION.md, then re-claim it.

## Identity

Use one stable, short handle everywhere (DISCUSSION.md, PLAN.md owners, commit body):

- Humans: your name.
- Agents: pick a handle (e.g. `agent-forge`) and keep it for the day.
- Note it in the commit body: `Agent: agent-forge` (or `By: yourname`).

## Commit style

- Imperative subject, ≤ 70 chars: `add login endpoint`, `fix: crash on empty config`
- Body (optional, encouraged): what + why, and which task it addresses: `Task: T4`

## Keeping the coordination files healthy

- **PLAN.md** is the source of truth: when reality drifts from it, fix it in the same commit as the change. Keep "Current state" to 3 short lines.
- **DISCUSSION.md** is append-only: new entries at the bottom, never rewrite or delete old ones.
- Both files must stay readable in under 2 minutes. When DISCUSSION.md grows long, distill durable decisions into PLAN.md ("Decisions") and move the old section to `docs/archive/`.

## Hard rules

- No force-pushes to `main`.
- No secrets in the repo (`.env` stays ignored).
- When in doubt, don't guess silently — write the question in DISCUSSION.md.
