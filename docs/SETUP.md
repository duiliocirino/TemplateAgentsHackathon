# Competition toolchain preflight

This checklist reflects the organizers' setup notice for this competition. Complete it once per machine before the challenge. The challenge brief and starter repository remain the source of truth for application architecture and project-specific dependencies.

## Required for everyone

| Requirement | Install / verify |
|---|---|
| Git and access to the event's GitHub repository | `git --version`; confirm you can access the team repo |
| Visual Studio Code with GitHub Copilot active | `code --version`; sign in and confirm Copilot works in the VS Code profile you will use |
| .NET 10 SDK | Install the **SDK**, not only a runtime: [official .NET 10 downloads](https://dotnet.microsoft.com/download/dotnet/10.0). Verify with `dotnet --version` and confirm `dotnet --list-sdks` includes `10.0.x` |

Copilot sign-in and entitlement need a manual check in VS Code; the CLI version commands do not verify them.

## Required for the relevant role

| Role | Requirement | Install / verify |
|---|---|---|
| Frontend | Node.js LTS 22 (22.12 or newer) or Node 24, with npm | [Node.js downloads](https://nodejs.org/en/download); verify `node --version` and `npm --version` |
| Frontend | Angular CLI 21 | `npm install -g @angular/cli@21`; verify with `ng version` |
| Backend | Python 3.13 or newer | [Python downloads](https://www.python.org/downloads/); verify with `python --version` |
| Backend | `uv` package/environment manager | Follow the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/); verify with `uv --version` |

## Recommended, not blockers

- Docker Desktop with Docker Compose: verify with `docker --version` and `docker compose version`. If the project uses containers, also run `docker info` to confirm the engine is running.
- A SQLite GUI, such as the VS Code SQLite Viewer extension or [DB Browser for SQLite](https://sqlitebrowser.org/).
- An API client, such as Postman, REST Client, or Thunder Client.

Do not block work just because an optional recommendation is absent.

## Before task claims

Before the challenge, each person confirms all requirements marked “for everyone.” Before claiming role-specific work, confirm the tools required for that role. Report any missing mandatory item to the orchestrator as a `block`; resolve it before dependent work starts. Do not silently substitute a different required toolchain.

## Machine setup vs. clone setup

This checklist is machine-level preparation. After cloning this coordination repository, run `.\scripts\setup.ps1` on Windows or `./scripts/setup.sh` in Bash, once per clone. These scripts configure Git pull/rebase and rerere behavior only; they do not install or validate the tools above.
