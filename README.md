# TemplateAgentsHackathon — v2

Coordination template for a team of humans + AI agents working in parallel on one repo,
from different machines, under time pressure. Hackathon-tested, finals-tuned.

## The one-minute idea

Shared state has exactly one writer per file, so coordination conflicts are impossible **by construction**, not by discipline:

- anyone **creates new files** in `docs/log/` — the filename IS the message (`2026-09-18-1805_valeria-fe-agent_block_T10-BFF-path-mismatch.md`)
- each handle owns one file in `docs/status/` — its memory and session handoff
- the **orchestrator** alone writes `docs/BOARD.md` (current state, regenerated every ≤10 min) and `docs/tasks/` (the plan)
- git is the transport, and **agents run git themselves** — humans don't babysit commits

## Machine setup (before the event)

See [docs/SETUP.md](docs/SETUP.md) for the organizers' required toolchain, role-specific prerequisites, and verification commands. Complete it once per machine.

## Clone setup (once per clone)

```powershell
.\scripts\setup.ps1    # or: scripts/setup.sh
```

This configures Git behavior for this clone; it does not install or validate the machine toolchain.

## Day-one flow

1. Each person starts their agent session with: `I am <name>, <role>. Follow AGENTS.md.`
2. One person runs a dedicated orchestrator chat, open all day: `You are the orchestrator. Follow docs/ORCHESTRATOR.md.`
3. The orchestrator publishes task files in `docs/tasks/` from the brief; the team self-claims via log entries.
4. Agents work → commit+push → log entry → status update, autonomously.
5. The orchestrator refreshes the board every ≤10 min and runs the CR playbook when the organizers change requirements mid-event (they will).

## Files

| Path | What | Writer |
|---|---|---|
| `AGENTS.md` | the protocol, auto-read by every coding agent | — (frozen during the day) |
| `docs/ORCHESTRATOR.md` | orchestrator identity, refresh cycle, CR playbook, decision guardrails | — |
| `docs/SETUP.md` | organizer-required machine preflight and role-specific tools | — (freeze during event) |
| `docs/BOARD.md` | current state: working/done/blocked/next | orchestrator only |
| `docs/tasks/` | task definitions with scope + definition of done | orchestrator only |
| `docs/log/` | one file per message to the team (grammar in its README) | anyone, create-only |
| `docs/status/` | one file per handle: working/done/blocked/handoff | owner only |
| `scripts/sync` | pull --rebase --autostash + status + feed, one command | — |

## Why this design (learned the hard way, 18 Sep)

- One shared PLAN.md + DISCUSSION.md with 5 concurrent writers: 75% of commits touched them, 3 rounds of md-conflict cleanup, ~1/3 of all human prompts spent on coordination overhead.
- Humans prompting "commit and push please" 23 times = humans as the sync bottleneck. In v2, git is the agents' job.
- Re-reading the whole plan + log every turn ≈ 81k prompt tokens/turn. Headline-first files keep a full team sync under ~3k.
- The change request hit at 2/3 time and the orchestrator role was improvised at 21:51. In v2 it exists at minute 0, with a playbook.
