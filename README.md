# TemplateAgentsHackathon

Team template for building with AI agents in parallel. Humans and agents share one repo, one plan, one log — no other infrastructure.

## The idea

A single agent gets its context from one conversation. Distributed agents (different laptops, different tools, parallel work) can't share conversations, so the shared context lives **in the repo**:

| File | Role |
|------|------|
| [`AGENTS.md`](AGENTS.md) | The protocol. Read automatically by agents (pi, Claude Code, Codex, …) on startup. |
| [`docs/PLAN.md`](docs/PLAN.md) | The plan: goal, current state, tasks, owners. |
| [`docs/DISCUSSION.md`](docs/DISCUSSION.md) | Append-only log: claims, decisions, handoffs. |

Git is the transport: **pull → read the three files → work → update the files → commit**.
The commit log is the feed of *what changed*; the docs are the feed of *why, and what's next*.

## Quickstart (per person / per agent)

1. `git clone` the repo (or `git pull --rebase`)
2. Read `AGENTS.md`, then `docs/PLAN.md`, then the tail of `docs/DISCUSSION.md`
3. Claim a task: set the owner in PLAN.md, log it in DISCUSSION.md, commit
4. Work in small, frequent commits to `main`
5. Complete: update PLAN.md ("Current state" + task), log it in DISCUSSION.md, commit

## Parallel agents on one machine

Give each agent its own worktree and a short-lived branch:

```bash
git worktree add -b agent-forge ../worktrees/agent-forge
# ... work and commit inside the worktree ...
git push origin agent-forge
git checkout main && git merge --ff-only agent-forge && git push
```

Across machines it's just clones of the same repo: pull often, push small commits.

## Rules of thumb

- One task, one owner — that's what prevents two agents from colliding.
- PLAN.md and DISCUSSION.md must stay readable in under 2 minutes; prune, don't grow.
- Real-time chat stays in Slack/Discord; the repo log is for durable things only.
- The design works at commit granularity (minutes), not seconds: coordinate before editing the same files.
