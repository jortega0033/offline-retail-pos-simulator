## Ticket

Closes #

## What changed

<!-- What the change does and why, in plain sentences. -->

## Evidence

<!-- Each command you ran and its result. Paste real output; never summarize a run you did not make. -->

| Command | Result |
|---|---|
| `python -m unittest` | |

## Agent roles run

<!-- Role, what it was asked, verdict. Also list any step done without a role and why. -->

| Role | Asked | Verdict |
|---|---|---|
| Code Reviewer | | |
| Reality Checker | | |

## Risks and rollback

<!-- What could break, and how to undo this change. -->

## Checklist

- [ ] Local checks passed before the draft pull request was opened
- [ ] Code Reviewer and Reality Checker ran on the current diff
- [ ] No dependency, external URL, build step or non-loopback listener added
- [ ] No data directory, SQLite file or `.env*` committed
- [ ] `CHANGELOG.md` has a line for this change
- [ ] Copy and docs went through the `unslop` skill; UI changes checked against `docs/ui-quality.md`
