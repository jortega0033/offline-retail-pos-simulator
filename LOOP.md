# Loop Configuration: Issue Triage

Scaffolded with `npx --yes @cobusgreyling/loop@0.2.0 init . --pattern issue-triage --tool claude` ([Loop Engineering](https://github.com/cobusgreyling/loop-engineering), MIT). The generated `.grok/` and `.codex/` variants were removed; this repository uses the Claude Code files only. The scaffold generated no workflow file, and none was added.

## Active Loops

| Pattern | Cadence | Status | Command |
|---------|---------|--------|---------|
| Issue Triage | Manual, on request | L1 report-only | `/issue-triage` in a Claude Code session at the repository root |

## Operating level: L1 report-only

- The loop reads open issues with `gh issue list` and `gh issue view` and rewrites `issue-triage-state.md`. That file and `loop-run-log.md` are the only files it may change.
- It never applies labels, comments, closes or edits issues, edits source or tests, commits, pushes, opens pull requests or merges.
- No scheduler is configured. Do not wrap the skill in `/loop`, a cron entry, a scheduled task or a GitHub workflow. The "2h" cadence in the generated skill text describes the upstream pattern, not this repository.
- `loop doctor` prints its own readiness score. That score describes the scaffold, not the operating level. The operating level here stays L1 until the owner changes this file.

## Ticket work is not a loop run

Implementing a ticket is not part of this loop. The owner starts it with `/next-ticket`, and it is governed by `CLAUDE.md` ("Delivery workflow"), the `implement-ticket` playbook, the review gate hook, CI and branch protection. The loop stays at L1: report-only and unscheduled.

## Next manual triage run

From the repository root, in a new Claude Code session:

```text
/loop-constraints
/issue-triage
```

Headless equivalent:

```text
claude -p "Run the loop-constraints skill, then the issue-triage skill in L1 report-only mode. Update issue-triage-state.md and append one entry to loop-run-log.md. Make no GitHub writes and change no other file."
```

Review the diff of `issue-triage-state.md` afterwards. Committing it is a human decision.

## Recorded health check (2026-11-22)

Run once from the repository root with `@cobusgreyling/loop@0.2.0` after the scaffold was installed. `doctor .`: Ready 100/100 L3, Status HEALTHY, exit 0 (its note: could not parse the loop-sync output; its next actions ask for `docs/safety.md`, templates and MCP notes, which this repository covers in `loop-constraints.md`, `.github/` and `CLAUDE.md`). `status .`: pattern issue-triage, state "not yet run", no runs in `loop-run-log.md`, exit 0. The score describes the scaffold. The operating level of this repository stays L1.

## Health checks

```text
npx --yes @cobusgreyling/loop@0.2.0 doctor .
npx --yes @cobusgreyling/loop@0.2.0 status .
```

Doctor exit codes: 0 healthy, 1 warnings, 2 blocked. Both commands fetch the package from npm, so they need a network connection. The product itself never does.

## Human Gates

- Priority assignment (P0, P1): human only.
- Anything touching the money rules (discount, largest-remainder allocation, tender split, refund negation, cash-up), the versioned event contract and its digest, the SQLite schema or its constraints, the request-ID idempotency and sequence allocation, the outbox and ledger acknowledgement rules, the loopback Host and Origin checks, the body-size bound, or how receipt text reaches the page: always escalate.
- Anything that would add a dependency, a build step, an external request or a non-loopback listener: always escalate. The product is offline and standard-library only by design ([docs/PRD.md](docs/PRD.md), "Runtime and interface").
- Duplicate closure: human confirms.
- Stale issue closure: human confirms.
- Any change to this file, `loop-budget.md` or `loop-constraints.md`: human only.

## Verifier

`.claude/agents/loop-verifier.md` is the checker for a later maker/checker level. It is limited to `Read, Grep, Glob`, so it cannot run the tests itself and must answer `ESCALATE_HUMAN` when a verdict depends on a test run. It has no role at L1 because the loop proposes no changes.
