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
| Run a store | `python -m retail_pos --role store --data-dir <dir> --port <port> --store-id <A or B>` | planned: introduced by ticket #2 |
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
- Do not change `.claude/agents/`, `LOOP.md`, `loop-constraints.md` or `loop-budget.md` as part of a feature ticket.

## Evidence before a ticket is called done

Items 1 to 7 are recorded locally before the draft pull request is opened and both gates judge them. Item 8 follows once the draft is open. Paste real output into the pull request; never summarize a run you did not make.

1. The output tail of `python -m unittest` from a clean checkout, with the Python version and operating system, and the test count before and after the change.
2. For each acceptance criterion in the issue: the test that proves it, or the exact manual step and what was observed.
3. For money, allocation or digest code: the spec fixture values checked against paper arithmetic in the test itself ([docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md), "Deterministic fixture and verification").
4. For persistence or sync code: the interruption or duplicate-delivery case exercised, the raw rows read back after the restart, and the SQLite version and journal settings reported.
5. For a new or changed route: one request and response pair per success and per error status, from a server on an ephemeral port and a scratch data directory.
6. For a change under the static UI: a browser run on the loopback URL with the browser name and version, keyboard-only operation of the changed controls, and a console and network log with no errors and no external request. Browser checks are manual.
7. `git status` with no stray files, and confirmation that no dependency, external URL or non-loopback listener was added.
8. Green CI on the draft pull request, checked by the driver before `gh pr ready`; Reality Checker is not asked to confirm it.
9. Anything not verified, said plainly.

## Loop

Issue triage runs at L1: report-only, started by hand, no scheduler, no GitHub writes. See [LOOP.md](LOOP.md).
