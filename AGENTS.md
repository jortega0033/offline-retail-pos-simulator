# AGENTS.md

The full repository instructions are in [CLAUDE.md](CLAUDE.md). This file repeats only what an agent needs before it reads that.

## State

Scaffold only: the package skeleton, `python -m unittest` and `python -m retail_pos --help|--version` are real. There is no product behaviour; the other commands in `CLAUDE.md` are planned and introduced by the tickets named there.

## Test commands (real)

```
python -m unittest
```

Python 3.12, standard library only. `pyproject.toml` pins `requires-python` and has no dependencies. There is no lint step or build step. Do not add pip or npm dependencies.

## Run (planned: introduced by ticket #2)

```
python -m retail_pos --role store --data-dir <scratch-dir> --port <port> --store-id <one of A to H> [--head-office-url http://127.0.0.1:<port>]
python -m retail_pos --role head-office --data-dir <scratch-dir> --port <port>
```

Store IDs are fixed to A to H (A and B are used in the first epic). `--head-office-url` is optional and loopback only. Both bind loopback only. Use a scratch data directory outside the repository.

## Ticket work

To implement a GitHub issue, follow the steps in [.claude/skills/implement-ticket/SKILL.md](.claude/skills/implement-ticket/SKILL.md) and the section "Agent roles" in [CLAUDE.md](CLAUDE.md). The role files in `.claude/agents/` each start with a section "In this repository" that holds the project rules for that role. An agent that cannot delegate to those roles does the before-coding, while-coding and specialist steps itself and says so in the pull request. The review gate and the acceptance gate still apply to every ticket, but the agent that wrote the change cannot pass them: do not push or open the pull request. Stop, report that the gates could not run, and leave the run for the owner. The order is: local checks, both gates, draft pull request, CI, then ready only on green CI.

## Delivery

Only the owner starts ticket work, with `/next-ticket`. A review gate hook blocks `gh pr create` and `gh pr ready` until both gate roles ran after the last code edit. Only the owner merges and releases. UI work follows [docs/ui-quality.md](docs/ui-quality.md); owner decisions are in [docs/owner-decisions.md](docs/owner-decisions.md). Details: "Delivery workflow" in [CLAUDE.md](CLAUDE.md).

## Loop conventions

- The loop runs at L1: report-only, started by hand. It proposes; it does not label, comment, close, edit source, push or merge.
- No scheduler and no loop workflow is installed. Do not add one without the owner's approval.
- See [LOOP.md](LOOP.md) for the manual command and the human gates.
