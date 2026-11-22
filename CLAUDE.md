# CLAUDE.md

Working instructions for this repository. Read this file first, then the documents it links to. It does not repeat them.

## What this is

A simulator of an offline retail point of sale for a fictional chain. A store process sells while head office is unreachable, keeps printable receipts, and later delivers every transaction to a separate head-office process exactly once. Full refunds and shift cash-up are part of the scope.

**State today: planning only.** The repository holds the README, the product plan and the technical specification. There is no application code, no test, no runnable command and no CI result. Every command in this file is planned; it is marked with the ticket that introduces it and must not be assumed to work until that ticket is merged. Do not claim a baseline that does not exist ([README.md](README.md), "Current status").

## Sources of truth

| Topic | Document |
|---|---|
| Product scope, finish line, fixture table, epic and ticket text | [docs/PRD.md](docs/PRD.md) |
| Runtime, money rules, persistence, reconciliation contract, verification fixtures | [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md) |
| Planned module map, data ownership and invariants (planned, not implemented) | [docs/architecture.md](docs/architecture.md) |
| Backlog | Epic issue #1 and its sub-issues on GitHub. The epic's table is authoritative for order, dependencies, parallel tracks and estimates. |
| Loop setup and its limits | [LOOP.md](LOOP.md), [loop-constraints.md](loop-constraints.md) |
| Project subagents, their origin and local changes | [.claude/agency-agents/README.md](.claude/agency-agents/README.md) |
| Owner decisions, dated, with where each is implemented | [docs/owner-decisions.md](docs/owner-decisions.md) |
| UI rules (ten, binding) | [docs/ui-quality.md](docs/ui-quality.md) |
| Ticket workflow and the step at which each agent role runs | [.claude/skills/implement-ticket/SKILL.md](.claude/skills/implement-ticket/SKILL.md), section "Agent roles" below |

The PRD and the technical specification state the same design twice; cite the technical specification. Once code exists, the code is the baseline when it disagrees with the plan, and [docs/architecture.md](docs/architecture.md) records the difference.

## Stack and hard rules

From [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md), "Runtime and interface". A change that breaks one needs the owner's approval first, not a pull request.

- Python 3.12, standard-library SQLite and HTTP, native HTML, CSS and JavaScript. No framework, no pip or npm dependency, no build step. The owner's machine has Python 3.13 as `python`; write code that also runs on 3.12.
- Two processes, a store and a head office, each on its own loopback port with its own SQLite database. They talk only over bounded loopback HTTP and never share a database file. The command line takes a role, a data directory, a port and a fictional store ID.
- Loopback only: no outgoing request to another host from the processes, the page or the tests. The page loads nothing from another host.
- Browser mutations check the loopback `Host` and a same-origin `Origin`. Request bodies are size-bounded. Writes are serialized within a process. SQL is parameterized. Receipt strings are rendered as text, never as HTML.
- Fixed set of simulated store IDs; unknown stores are rejected. Fixed currency, integer minor units everywhere.
- Fault controls act only on fixture links and on test subprocesses the harness started itself.
- Durability profile for tests: rollback journal, `synchronous=FULL`, foreign keys enabled on every connection. Reports name the filesystem, journal settings and SQLite version, and claim durability only for the process-interruption cases actually exercised.
- Synthetic data only: no real payments, personal data, tax, inventory reservation, loyalty, price distribution or partial refunds.
- Tests use temporary directories and ephemeral ports, no fixed port, no network, no dependence on wall-clock timing for a pass. Generated IDs and databases are new on every run.

## Commands (all planned)

Nothing below runs yet. Each is introduced by the ticket named. On the owner's Windows machine Python is `python` (`python3` on Linux).

| Purpose | Command | Status |
|---|---|---|
| Run all tests | `python -m unittest` | planned: introduced by ticket #2 |
| Run a store | `python -m retail_pos --role store --data-dir <dir> --port <port> --store-id <one of A to H> [--head-office-url http://127.0.0.1:<port>]` | planned: introduced by ticket #2 (`--head-office-url` is optional there and drives the manual send; ticket #5 adds the delivery worker). Store IDs are fixed to A to H; this epic uses A and B. |
| Run head office | `python -m retail_pos --role head-office --data-dir <dir> --port <port>` | planned: introduced by ticket #2, completed by ticket #4 |
| Repeatable offline-sale demo from a clean directory | `python -m retail_pos.demo` | planned: introduced by ticket #2 |
| Two-store evidence report with controlled exits | `python -m retail_pos.evidence` | planned: introduced by ticket #7 |

Module and flag names are the plan's defaults ([docs/architecture.md](docs/architecture.md)); the ticket that introduces a command confirms or corrects them here in the same pull request. Never run a server against the repository directory: use a scratch data directory and delete it afterwards. Database files (`*.sqlite*`, `*.db`) are ignored by Git. On Windows, stop a background server by process id, then confirm the port is free.

## Architecture boundaries (planned)

The full map is in [docs/architecture.md](docs/architecture.md). The short form:

- Store process: HTTP layer, checkout, shifts and refunds, outbox, sync client, static register UI. Head-office process: HTTP layer, ingest, ledger, cursor, reports. Shared pure code only: money arithmetic, the versioned event contract and its digest.
- The store never reads head-office tables and head office never reads store tables. The event envelope is the only contract between them.
- Money arithmetic lives in one pure module with no I/O; the HTTP layer never computes amounts.
- The storage layer is the only code that touches `sqlite3`. Every write is one explicit transaction.

Rules that every change keeps (each is stated in [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md)):

- Look up the request ID before checking shift state. The same canonical input returns the same receipt, even after shift close; changed input conflicts before anything is written.
- For a new request, one transaction validates the open shift, allocates the next sequence, appends the event, stores the receipt snapshot and queues the outbox payload. Commit before the receipt is shown.
- Sent payloads are frozen: every retry sends the same saved bytes.
- Head office appends a ledger row and advances the cursor in one transaction. Exact duplicates return the original acknowledgement; a gap reports the next expected sequence; changed content under an existing identity is a conflict and pauses that store.
- A store marks an outbox row confirmed only after the acknowledgement matches store ID, sequence, event ID and digest.
- One full refund per original sale, enforced by a unique origin reference; the refund negates amounts and tender shares exactly and the original receipt stays unchanged.

## Git workflow

- Default branch `main`. One branch per ticket, named `<issue-number>-<short-slug>`, and a pull request to `main` that names the issue (`Part of #1`, `Closes #n`). Small commits with imperative subjects and a type prefix (`feat:`, `fix:`, `test:`, `docs:`, `chore:`).
- Only the owner merges and releases. Do not push to `main`, do not merge your own pull request, do not force-push.
- Order for every ticket: local checks, Code Reviewer, Reality Checker, a draft pull request, CI on that draft, then ready only when CI is green.
- Never commit a data directory, a SQLite file or `.env*`.
- In a ticket, do not change `.claude/agents/`, `.claude/skills/`, `.claude/hooks/`, `.claude/settings.json`, `.claude/agency-agents/`, `LOOP.md`, `loop-constraints.md` or `loop-budget.md`, by any means including shell commands.

## Evidence before a ticket is called done

Items 1 to 7 are what the agent can record locally before the draft pull request is opened, and both gates judge them. Steps the ticket marks manual and that need a person (browser name and version, keyboard-only run, devtools storage, network log) are done by the agent as far as it can, with scripted evidence, and the rest is listed under "Owner checks" in the pull request; the gates judge the scripted evidence and the Owner checks list, not a browser record. Item 8 follows once the draft is open. Paste real output into the pull request; never summarize a run you did not make.

1. The output tail of `python -m unittest` from a clean checkout, with the Python version and operating system, and the test count before and after the change.
2. For each acceptance criterion in the issue: the test that proves it, or, for a step the ticket marks manual, the scripted evidence the agent could produce plus the remaining step listed under "Owner checks".
3. For money, allocation or digest code: the spec fixture values checked against paper arithmetic in the test itself ([docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md), "Deterministic fixture and verification").
4. For persistence or sync code: the interruption or duplicate-delivery case exercised, the raw rows read back after the restart, and the SQLite version and journal settings reported.
5. For a new or changed route: one request and response pair per success and per error status, from a server on an ephemeral port and a scratch data directory.
6. For a change under the static UI: the evidence an agent can produce, namely tests, HTTP request and response pairs from a server on an ephemeral port, the static scan (no external URL, no non-loopback listener), the CSP header and the served HTML. Steps the ticket marks manual (browser name and version, keyboard-only operation of the changed controls, devtools storage, console and network log) go under "Owner checks" in the pull request; the agent never invents a browser record.
7. `git status` with no stray files, and confirmation that no dependency, external URL or non-loopback listener was added.
8. Green CI on the draft pull request, checked by the driver before `gh pr ready`; Reality Checker is not asked to confirm it.
9. Anything not verified, said plainly.

## Delivery workflow

How a ticket gets from the backlog to a pull request. Each item is defined in the file linked; this part only points at them.

- **Start:** only the owner starts ticket work, with `/next-ticket [issue number]` ([driver](.claude/skills/next-ticket/SKILL.md)). Starting it is the go signal; nothing is scheduled. One ticket per run. Only leaf tickets are picked, never a `tracking` parent; the pull request of a parent's last sub-issue also closes the parent.
- **Playbook:** [implement-ticket](.claude/skills/implement-ticket/SKILL.md), with the roles in "Agent roles" below.
- **Review gate hook:** [`.claude/hooks/role_gate.py`](.claude/hooks/role_gate.py) blocks `gh pr create` and `gh pr ready` until Code Reviewer and Reality Checker ran after the last code edit (documentation-only changes pass). The owner can switch it off for a session by starting Claude Code with `ROLE_GATE=off`. Its ledger is `claude-role-runs.jsonl` in the repository's common git dir (shared by the main checkout and all worktrees); the older `.claude/state/role-runs.jsonl`, which Git ignores, is still read.
- **Permissions:** [`.claude/settings.json`](.claude/settings.json). Documented commands are allowed; force pushes, pushes to `main`, `gh pr merge`, releases and reads of `.env` are denied; edits to `.github/`, agent configuration, hooks, skills, this file, `AGENTS.md` and the Loop files ask first, at any depth so ticket worktrees ask too. Acceptance steps that need a person are listed under "Owner checks" in the pull request.
- **CI:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs on Linux and Windows with Python 3.12 and 3.13. It must be green before a pull request is marked ready. The driver does not poll: after the push it ends the turn with "Draft pull request #N is waiting for CI" and reads `gh pr checks` once when woken. Until ticket #2 adds `retail_pos/`, the test step is skipped by a guard that enables itself once `retail_pos/__init__.py` exists; the gate self-test runs always. Deleting the guard line afterwards is optional cleanup that needs the owner (edits to `.github/` ask first).
- **Pull request:** [template](.github/pull_request_template.md). Ticket template: [implementation-ticket](.github/ISSUE_TEMPLATE/implementation-ticket.md).
- **Labels:** `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`.
- **Changelog:** every ticket pull request adds a line to [CHANGELOG.md](CHANGELOG.md).
- **UI and copy:** UI tickets follow [docs/ui-quality.md](docs/ui-quality.md) and start with the `ui-ux-pro-max` skill; copy, docs and pull request text go through the `unslop` skill.
- **Merge and release:** only the owner merges and releases ([docs/RELEASING.md](docs/RELEASING.md)). Decisions the owner made are in [docs/owner-decisions.md](docs/owner-decisions.md); an agent that finds one blocking a ticket stops and says so.

## Loop

Issue triage runs at L1: report-only, started by hand, no scheduler, no GitHub writes. See [LOOP.md](LOOP.md).

## Agent roles

Project subagents are in `.claude/agents/`: eleven Agency Agents roles and `loop-verifier`, which belongs to the Loop setup. Each Agency Agents role file starts with a section "In this repository", written for this project: the stack and hard rules that bind the role, the files it owns or reviews, its commands or the output it must be given, a checklist of this project's rules, the parts of the generic text that do not apply, and what it hands back. Nothing is implemented yet, so those sections describe planned modules and commands. That section and this file override the generic text below it. Sources, licence and local changes are in [.claude/agency-agents/README.md](.claude/agency-agents/README.md).

When asked to implement, continue or finish a GitHub issue, follow the playbook [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md). Claude Code loads it on its own for ticket work; `/implement-ticket <issue number>` starts it by hand. Delegate to the roles without waiting to be asked: each role's `description` ends with a "Use proactively ..." sentence, which is what makes Claude Code delegate. The playbook gives the exact trigger of each role.

| When | Roles | Access |
|---|---|---|
| Before coding | Software Architect (module boundary, data model, schema, event contract, route or dependency) | `Read, Grep, Glob` |
| While coding | Backend Architect (server, persistence), Frontend Developer (static UI), Test Automation Engineer (fixtures, harness, tests) | can edit |
| While coding | Database Reliability Engineer (schema, constraints, transactions, restart and interruption handling) | `Read, Grep, Glob` |
| After coding, when the trigger matches | Application Security Engineer (untrusted input, Host and Origin checks, event validation), Accessibility Auditor (UI, keyboard, focus), Performance Benchmarker (reported measurements) | `Read, Grep, Glob` |
| After coding, when the trigger matches | API Tester (new or changed route or status code) | can edit |
| Gate on every ticket | Code Reviewer on the full diff, until no material finding is left | `Read, Grep, Glob` |
| Acceptance gate on every ticket, after Code Reviewer | Reality Checker on each acceptance criterion and the recorded local evidence, and that CI is configured to run the checks (no CI result is needed) | `Read, Grep, Glob` |

- The two gates run on every ticket, whatever its size. A ticket is not called done before both have passed.
- Roles limited to `Read, Grep, Glob` cannot run commands. Before calling them, write the diff and the recorded check output to `.claude/state/review/` in the ticket worktree and name the files in the request.
- The session or role that wrote a change does not count as its reviewer.
- If a role is missing or cannot be delegated to, the session does the before-coding, while-coding and specialist steps itself and says so. It cannot pass the two gates on its own change: do not push or open the pull request. Stop, report that the gates could not run, and leave the run for the owner. A pull request is opened or marked ready only after both gates passed on the current diff.
- In the pull request description, list under "Agent roles run" each role that ran, what it was asked and its verdict, and any step done without a role.
