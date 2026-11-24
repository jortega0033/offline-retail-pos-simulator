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

1. **Refresh the queue.** `gh issue list --label status:blocked --state open`. For each, read its blockers (`gh issue view`, and the epic's dependency table). If every blocker is closed, replace `status:blocked` with `status:ready`. Also check parents: a `tracking` parent whose sub-issues are all closed is closed with a comment. A ticket with no sub-issues is never closed by this step. Do nothing else to the labels of other tickets.
2. **Pick.** Work happens on leaf tickets only. A ticket labelled `tracking`, or with open sub-issues, is a container and is never picked. With an issue number: use it, but stop and say why if it is not a descendant of epic #1, is `needs-decision`, is `status:in-progress`, or has an open blocker; if it is a `tracking` parent, refuse it and list its open sub-issues. Without a number: take the first `status:ready` leaf ticket in the epic's order (the order of the parents in the epic's table, then the order of the sub-issues inside each parent) that is neither `status:in-progress` nor `needs-decision`. If none, report the queue (what is blocked by what) and stop.
3. **Claim.** Add `status:in-progress` to the issue.
4. **Branch.** Create a branch `<issue-number>-<short-slug>` from the latest `origin/main` in a fresh worktree (`git worktree add`). Work only there. Never touch the default branch or the owner's checkout.
5. **Implement.** Run the `implement-ticket` playbook for that issue, delegating to the project roles at the steps it names. Open owner decisions on the ticket are settled with the ticket's stated default; where it states none, take the conservative option and say so in the issue. A decision that blocks the ticket: stop, comment on the issue, say so.
6. **Gates and draft.** Local checks, Code Reviewer, Reality Checker. Add the line to `CHANGELOG.md` before the draft is opened, as playbook step 10 says (documentation only, so the gates stay valid). Before calling the reviewers, write the diff and the local evidence to the ticket worktree's `.claude/state/review/` (`git diff --stat origin/main...HEAD`, `git diff origin/main...HEAD`, the check outputs) and name those files in the request, because they have no shell. The pull request of the last open sub-issue of a parent says `Closes #<sub-issue>` and `Closes #<parent>`. Then `gh pr create --draft` (the gate hook blocks it unless both gates ran after the last code edit).
7. **CI, without polling.** After `git push`, bind the pull request to the session when the app offers it, and end the turn with the line "Draft pull request #N is waiting for CI". Do not loop, sleep or watch. When the session is woken (a CI event, or the owner says "continue"), read `gh pr checks <number>` once. Red: compare with the latest run on `main`, fix, re-run local checks and both gates, push, end the turn again. Still running: end the turn again with the same line. Green is a condition for step 8 that you check yourself; Reality Checker does not judge it.
8. **Ready.** With CI green and both gates passed on the current diff, run `gh pr ready <number>`, then comment on the issue with the pull request link and the CI run link. List acceptance steps that need a person under "Owner checks" in the pull request. Remove nothing else; the owner merges and the issue closes with the merge.
9. **Stop.** Report the pull request, the CI run, anything not verified, and the next ticket that is now unblocked. Do not start it.
