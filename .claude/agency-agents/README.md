# Agency Agents roles used in this repository

The Markdown files in `.claude/agents/` whose names start with `engineering-`, `security-` or `testing-` are copies of role definitions from Agency Agents. They are project-local Claude Code subagents. The file `loop-verifier.md` in the same folder is not from Agency Agents; it belongs to the Loop Engineering setup described in [`LOOP.md`](../../LOOP.md).

## Source and licence

- Upstream: https://github.com/msitarzewski/agency-agents
- Pinned revision: `8ae6164602c95ca78828b148b9052460ee426885` (upstream `main`, committed 2026-11-09)
- Licence: MIT, "Copyright (c) 2025 AgentLand Contributors". The upstream licence text at the pinned revision is kept unchanged in [`LICENSE`](LICENSE) next to this file (SHA-256 `9a45258434d5cedf0af73c9ad4771373701225038d246c49219026c33677f66f`). It covers only the copied role files, not the rest of this repository.
- Fetched with `gh api -H "Accept: application/vnd.github.raw" "repos/msitarzewski/agency-agents/contents/<path>?ref=<revision>"`.

## Installed roles

"Upstream SHA-256" is the hash of the file as fetched at the pinned revision. Reviewer roles have one added frontmatter line, `tools: Read, Grep, Glob`, so they cannot edit files or run commands. Nothing else in any file was changed at the time of copying.

| File in `.claude/agents/` | `name:` | Upstream path | Upstream SHA-256 | Local change |
|---|---|---|---|---|
| `engineering-code-reviewer.md` | Code Reviewer | `engineering/engineering-code-reviewer.md` | `7509fcc3ea1dda46511b2801996305bf3d4a125576f9655ff0b63df25602f446` | added `tools: Read, Grep, Glob` |
| `testing-reality-checker.md` | Reality Checker | `testing/testing-reality-checker.md` | `6d32fcdb114233e13902ec6372d50293b120e85d490b5e81d372c29808f988a1` | added `tools: Read, Grep, Glob` |
| `engineering-software-architect.md` | Software Architect | `engineering/engineering-software-architect.md` | `b85121691776147bacde26673e68fbbacd6a7f0816d1ca8e203c264d25ce1d30` | added `tools: Read, Grep, Glob` |
| `engineering-database-reliability-engineer.md` | Database Reliability Engineer | `engineering/engineering-database-reliability-engineer.md` | `0096dc3c1b31e33814c509fda43853cc77cef6252bb94da527b833be13b53a5a` | added `tools: Read, Grep, Glob` |
| `security-appsec-engineer.md` | Application Security Engineer | `security/security-appsec-engineer.md` | `a19f0bda46f4adca5737365dbc3c7ed93e9d93b71349536d92ff055dcf4e3b83` | added `tools: Read, Grep, Glob` |
| `testing-accessibility-auditor.md` | Accessibility Auditor | `testing/testing-accessibility-auditor.md` | `362935907af23839775b9c6162f38c0c5a740542ab4350cb5c5b5a0d9f9a4268` | added `tools: Read, Grep, Glob` |
| `testing-performance-benchmarker.md` | Performance Benchmarker | `testing/testing-performance-benchmarker.md` | `16a841f67392d084b773c6d9f05341d093e9017f3e116f6df0de59a5a3f59c34` | added `tools: Read, Grep, Glob` |
| `engineering-backend-architect.md` | Backend Architect | `engineering/engineering-backend-architect.md` | `ac717bde4848d7663fff8a3c7edc711fd119256de6a7ce38c036619372f42c99` | none |
| `engineering-frontend-developer.md` | Frontend Developer | `engineering/engineering-frontend-developer.md` | `1ae4cc10b2e0163bd3ed921ad54080b865cd02e591becd8919b64b73fab06dad` | none |
| `testing-api-tester.md` | API Tester | `testing/testing-api-tester.md` | `ab91de9188d48bd9c417282c33673a37b066215e90e08c0f1b270d036084e3bb` | none |
| `testing-test-automation-engineer.md` | Test Automation Engineer | `testing/testing-test-automation-engineer.md` | `4299d038e88387546d645ccbe767b1dfdb7de10da55eba1ab103149972cd2b9b` | none |

`loop-verifier.md` comes from the Loop Engineering scaffold (`@cobusgreyling/loop@0.2.0`, MIT); one line, `tools: Read, Grep, Glob`, was added.

## Why these roles

The repository plans two Python standard-library processes with SQLite, a keyboard-first native browser UI, an exactly-once delivery contract and a fault harness. Nothing is implemented yet, so the roles below describe the planned work.

| Role | Use in this repository |
|---|---|
| Software Architect (read-only) | Check a ticket against the module map and data ownership in [`docs/architecture.md`](../../docs/architecture.md) before code is written: the event contract, the store and head-office boundary, where money arithmetic lives. |
| Code Reviewer (read-only) | Review every diff for correctness, missed edge cases and broken rules (integer money, one transaction per write, frozen payloads, request guards, no outgoing request). Gate on every ticket. |
| Reality Checker (read-only) | Acceptance gate on every ticket: compare each criterion with the evidence actually produced. |
| Database Reliability Engineer (read-only) | Review the schema, constraints, transaction scope, rollback journal and `synchronous=FULL` profile, and the interruption and recovery cases. The product is built around crash-safe commits and restart recovery. |
| Application Security Engineer (read-only) | Review loopback Host and Origin checks, body bounds, parameterized SQL, receipt text rendered as text, and validation of events received by head office. |
| Accessibility Auditor (read-only) | Review keyboard operation, tab order, visible focus, labelled errors and the text summary of the register and operator screens. |
| Performance Benchmarker (read-only) | Review how the harness reports receipt latency, backlog catch-up and resource use (workload, environment, repeats, failures). It cannot run commands here; it judges recorded output. |
| Backend Architect | Implement work in the HTTP layer, store and head-office modules and persistence. |
| Frontend Developer | Implement the register, receipt print view, operator panel and cash-up screens in native HTML, CSS and JavaScript. |
| API Tester | Write the HTTP-level `unittest` cases for routes and error statuses. |
| Test Automation Engineer | Build the seeded fixtures, the controlled-exit harness and the evidence report. |

Most of these roles are written for larger stacks (frameworks, cloud services, Playwright, PostgreSQL, scanner pipelines). In this repository the rules in [`CLAUDE.md`](../../CLAUDE.md) win: Python standard library only, SQLite, native HTML, CSS and JavaScript, `unittest`, no pip or npm dependencies, no external requests.

Roles considered and left out: Codebase Onboarding Engineer (there is no code to trace yet; add it when the first ticket has merged), Database Optimizer (no performance-tuned queries are planned), UI Designer and UX Architect (the UI rules are checked by Code Reviewer and Accessibility Auditor), DevOps and tooling roles (no deployment exists).

## Local edits after copying

On 2026-11-22 one checklist line naming `docs/ui-quality.md` was added to the "In this repository" section of Code Reviewer, Frontend Developer and Accessibility Auditor. UI Designer and UX Architect are not installed here; the UI rules are checked by those three roles. The `ui-ux-pro-max` and `unslop` skills are installed under `.claude/skills/` and keep their own `PROVENANCE.md` files.

## Load check (2026-11-22)

Run from the repository root with `claude -p "List every project subagent in .claude/agents with its name and tools, say whether each starts with a section titled In this repository, and list the project skills." --model haiku` (Claude Code 2.1.323). Result: 12 project subagents. The 11 Agency Agents roles start with "In this repository"; `loop-verifier` does not (it is not an Agency Agents file). Tools: `Read, Grep, Glob` for Code Reviewer, Reality Checker, Software Architect, Database Reliability Engineer, Application Security Engineer, Accessibility Auditor, Performance Benchmarker and loop-verifier; no `tools:` line (full tools) for Backend Architect, Frontend Developer, Test Automation Engineer and API Tester. Project skills listed: implement-ticket, next-ticket, loop-budget, loop-constraints, loop-intake, issue-triage, ui-ux-pro-max, unslop. The run also printed that the `permissions.allow` entries of `.claude/settings.json` were ignored because the workspace (a worktree path) was not trusted yet; the owner's checkout needs the trust dialog accepted once.

## Name collision with user-level agents

A developer who has installed Agency Agents in `~/.claude/agents/` already has agents with the same `name:` values. Claude Code gives the project-level definition precedence, so inside this repository the copies here are used, including the read-only tool limits. The upstream names were kept on purpose so that the roles stay recognisable and can be compared with upstream.

A Claude Code session that was already running when these files were added keeps the definitions it loaded at start. Start a new session to pick up the project copies.

## Updating

Fetch the same paths at a newer revision, re-apply the `tools:` line to the seven reviewer roles, and update the revision and hashes in this file in the same commit.

## Local change: automatic delegation (2026-11-22)

One sentence beginning "Use proactively" was appended to the `description:` line of every Agency Agents role in `.claude/agents/` (not to `loop-verifier`). Claude Code uses that field to decide when to delegate, so the roles now run during ticket work without being named. A section headed "In this repository" was then inserted directly after the frontmatter of every Agency Agents role (not into `loop-verifier`), before the upstream text. It is project-specific text written for this repository, not upstream text: the stack and hard rules that bind the role, what it does here, its commands or the output it must be given, a checklist of this project's rules with their sources, the parts of the generic text that do not apply, and what it hands back. Because the repository has no code yet, the sections describe the planned modules and commands from `docs/TECHNICAL_SPEC.md` and `docs/architecture.md` and say so; they must be re-checked against the code as each ticket lands. Each ends with the sentence "This section and CLAUDE.md override the generic text below wherever they differ." The upstream text below it and the rest of the frontmatter are unchanged.

This supersedes any statement above that a role file is unmodified or that the `tools:` line is the only local change. To compare a role with the pinned upstream file, first remove the "Use proactively" sentence (in Backend Architect, Frontend Developer, API Tester, Performance Benchmarker and Reality Checker also the full stop that was added in front of it, because the upstream description has none), the section "In this repository" together with the blank line after it, and the `tools:` line where one was added. Checked on 2026-11-22: with these three removed, each of the eleven files has the upstream SHA-256 listed in the table above. After fetching a newer upstream revision (see "Updating"), put all three back and check each section against the code as it then is.

The steps at which each role runs are in `.claude/skills/implement-ticket/SKILL.md`.

Loading check: the `claude -p` listing of project agents was not run in this preparation stage. It remains to be done once from the repository root in a new session before the roles are called verified.
