---
name: next-ticket
description: 'Take the next ready ticket of epic #1 up to a ready pull request. Started only by the owner; starting it is the go signal.'
disable-model-invocation: true
argument-hint: "[issue number]"
---

# Next ticket

The owner starts this with `/next-ticket` or `/next-ticket <issue number>`. Nothing else starts it: no scheduler, no loop, no other skill. One ticket per run. Never merge, never release, never start another run.

Epic: [#1](https://github.com/jortega0033/offline-retail-pos-simulator/issues/1). Its table is authoritative for order and dependencies. The playbook is [`.claude/skills/implement-ticket/SKILL.md`](../implement-ticket/SKILL.md); `CLAUDE.md` wins where they differ.

Labels: `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`.

## Steps

1. **Refresh the queue.** `gh issue list --label status:blocked --state open`. For each, read its blockers (`gh issue view`, and the epic's dependency table). If every blocker is closed, replace `status:blocked` with `status:ready`. Do nothing else to the labels of other tickets.
2. **Pick.** With an issue number: use it, but stop and say why if it is not a child of epic #1, is `needs-decision`, is `status:in-progress`, or has an open blocker. Without a number: take the first `status:ready` child of epic #1 in the epic's dependency order that is neither `status:in-progress` nor `needs-decision`. If none, report the queue (what is blocked by what) and stop.
3. **Claim.** Add `status:in-progress` to the issue.
4. **Branch.** Create a branch `<issue-number>-<short-slug>` from the latest `origin/main` in a fresh worktree (`git worktree add`). Work only there. Never touch the default branch or the owner's checkout.
5. **Implement.** Run the `implement-ticket` playbook for that issue, delegating to the project roles at the steps it names. Open owner decisions on the ticket are settled with the ticket's stated default; where it states none, take the conservative option and say so in the issue. A decision that blocks the ticket: stop, comment on the issue, say so.
6. **Gates and draft.** Local checks, Code Reviewer, Reality Checker, then `gh pr create --draft` (the gate hook blocks it unless both gates ran after the last code edit). Add a line to `CHANGELOG.md`.
7. **CI.** `gh pr checks <number> --watch` on the draft. If a check fails, compare it with the latest run on `main`, fix, re-run local checks and both gates, push. Green CI is a condition for step 8 that you check yourself; Reality Checker does not judge it.
8. **Ready.** With CI green and both gates passed on the current diff, run `gh pr ready <number>`, then comment on the issue with the pull request link and the CI run link. Remove nothing else; the owner merges and the issue closes with the merge.
9. **Stop.** Report the pull request, the CI run, anything not verified, and the next ticket that is now unblocked. Do not start it.
