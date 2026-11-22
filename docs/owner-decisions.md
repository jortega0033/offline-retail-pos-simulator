# Owner decisions

A dated record of the decisions the owner made for this repository, so the rules do not depend on anyone's memory of a conversation. Every entry is dated 2026-11-22. Changing any entry needs the owner; an agent that finds a decision blocking a ticket stops and says so.

| # | Decision | Implemented in |
|---|---|---|
| 1 | The instructions, tooling and playbook live on the default branch (`main`). | The whole `.claude/` tree, `CLAUDE.md`, `AGENTS.md`, `.github/`, `docs/` |
| 2 | Persona agents run automatically during ticket work and carry instructions tailored to this project. | [`.claude/agents/`](../.claude/agents/) (section "In this repository" in each role), [`.claude/skills/implement-ticket/SKILL.md`](../.claude/skills/implement-ticket/SKILL.md), [`.claude/agency-agents/README.md`](../.claude/agency-agents/README.md) |
| 3 | Every open ticket is about app implementation; tooling is installed, not ticketed. | Epic [#1](https://github.com/jortega0033/offline-retail-pos-simulator/issues/1) and tickets #2 to #9 |
| 4 | Agents may take a ticket up to a ready pull request. Only the owner merges and releases. | [`CLAUDE.md`](../CLAUDE.md) "Git workflow", [`.claude/settings.json`](../.claude/settings.json) deny rules, [`RELEASING.md`](RELEASING.md) |
| 5 | No scheduler. Ticket work starts only on the owner's go signal (`/next-ticket`), because the repository is used to train AI models. | [`.claude/skills/next-ticket/SKILL.md`](../.claude/skills/next-ticket/SKILL.md) (`disable-model-invocation: true`), [`LOOP.md`](../LOOP.md) |
| 6 | A review gate hook blocks opening or readying a pull request until the gate roles (Code Reviewer, Reality Checker) have run after the last code edit. | [`.claude/hooks/role_gate.py`](../.claude/hooks/role_gate.py), hooks in [`.claude/settings.json`](../.claude/settings.json). `ROLE_GATE=off` switches it off for a session. |
| 7 | Loop Engineering stays at L1, report-only and unscheduled. | [`LOOP.md`](../LOOP.md), [`loop-constraints.md`](../loop-constraints.md) |
| 8 | Continuous integration runs on Linux and Windows; the default branch requires a pull request and green checks. | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml); branch protection is set on GitHub by the owner's orchestration after the merge |
| 9 | Documented commands are allowed; force pushes, pushes to the default branch, merges, releases and reads of secrets are denied; edits to CI, agent configuration and Loop files ask first. | [`.claude/settings.json`](../.claude/settings.json) |
| 10 | Open decisions on tickets are settled with the ticket's stated default. Settled this way, with the default and the issues that use it, in the table below. | Issues #2 to #9 |
| 11 | Rust (where present) is verified in CI only. Not applicable: this repository has no Rust. | None |
| 12 | The ten UI rules in [`ui-quality.md`](ui-quality.md) are binding, and the `ui-ux-pro-max` and `unslop` skills are installed in the repository and used for UI work and for copy. | [`ui-quality.md`](ui-quality.md), [`.claude/skills/ui-ux-pro-max/`](../.claude/skills/ui-ux-pro-max/), [`.claude/skills/unslop/`](../.claude/skills/unslop/) |

## Decisions settled with the ticket default (entry 10)

Each ticket applies the default if the owner has not answered. A decision the owner changes afterwards needs an issue comment on the ticket named.

| ID | Decision | Default | Used by |
|---|---|---|---|
| D1 | Package and module names | `retail_pos`, layout in `docs/architecture.md` | #2 |
| D2 | Event digest | SHA-256 of the canonical JSON (UTF-8, sorted keys, no insignificant whitespace) of the normalized fields without the digest | #3, #4 |
| D3 | Event envelope v1 fields | `version`, `store_id`, `sequence`, `event_id`, `shift_id`, `type`, `amount`, `lines`, `tenders`, `original_sale_id`, `digest` | #3, #4 |
| D4 | Currency | EUR with two decimals, one constant shown on screens and receipts | #2 |
| D5 | Fixed store IDs | A to H; only A and B are exercised in this epic | #2, #4 |
| D6 | Synthetic catalog | notebook 199, pen 249, eraser 150, in a fixture module | #2 |
| D7 | Sync trigger and backoff | background worker plus a manual send; 1 s doubling to a 30 s cap | #5 |
| D8 | Limits | body 64 KiB; quantity 1 to 999; at most 50 lines; price at most 1,000,000 minor units | #2, #3 |
| D10 | Test-only fault switch | `RETAIL_POS_TEST_HARNESS=1` plus a checkpoint name in the environment, read once at start | #3, #7, #8 |
| D11 | Meaning of "zero external requests" | static scan for absolute URLs, CSP `default-src 'self'` on every static response, manual network log | #7 |
| D12 | Resource measurement | wall time, SQLite file sizes, peak memory of owned processes where the OS allows | #7 |
| D13 | Licence | left unselected; no LICENSE file is added (owner decision, not ticketed) | none |
| D14 | Platforms | Windows and Linux, Python 3.12 and 3.13 | CI |
| D15 | Receipt and transaction IDs | generated UUID4 plus the store sequence number | #2 |
| D16 | Refund eligibility | same store, refund recorded in the current open shift, original may be from an earlier shift | #6 |
| D17 | Cash tender | every tender share is virtual cash; all signed events count toward expected cash | #6 |
| D18 | Shift rules | one open shift per store; opening cash entered at open; a closed shift is final | #2, #6 |
| D19 | Conflict handling | a conflict pauses the store; no resume action in this epic | #4, #5 |
