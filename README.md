# Offline Retail POS Simulator

A planned offline project. Implementation has not started. The repository currently contains the product plan, technical specification and implementation backlog.

## Program goal

Build the distributed system behind a retail chain: thousands of stores that sell offline for days, a ledger that stays exact through any failure, stock, pricing and fraud decisions, and a simulator that tries to break all of it.

The program is planned ([#39](https://github.com/jortega0033/offline-retail-pos-simulator/issues/39)). Phase 1 is the current epic [#1](https://github.com/jortega0033/offline-retail-pos-simulator/issues/1) and the only phase with tickets.

**Score.** Simulated store-years under injected faults without a lost, doubled or unbalanced transaction.

| Phase | Content | Hours (rough) | Issue |
|---|---|---|---|
| 1 | The current epic and its tickets | 60 to 95 | [#1](https://github.com/jortega0033/offline-retail-pos-simulator/issues/1) |
| 2 | Exact ledger | 90 to 150 | [#40](https://github.com/jortega0033/offline-retail-pos-simulator/issues/40) |
| 3 | Distributed core | 170 to 300 | [#41](https://github.com/jortega0033/offline-retail-pos-simulator/issues/41) |
| 4 | Decisions | 120 to 200 | [#42](https://github.com/jortega0033/offline-retail-pos-simulator/issues/42) |
| 5 | Till and devices | 110 to 180 | [#43](https://github.com/jortega0033/offline-retail-pos-simulator/issues/43) |
| 6 | Scale and proof | 120 to 210 | [#44](https://github.com/jortega0033/offline-retail-pos-simulator/issues/44) |

About 670 to 1140 engineer hours in total: rough estimates, not measurements. The numbers in the score and the finish lines are targets until a run shows them. Only phase 1 has tickets to work; the sub-issues of a later phase are written when it starts. No single session is expected to reach the end.

## Plan

- [Full product plan and acceptance criteria](docs/PRD.md)
- [Technical specification and verification fixtures](docs/TECHNICAL_SPEC.md)
- [Implementation epic](https://github.com/jortega0033/offline-retail-pos-simulator/issues/1)

## Current status

The package skeleton exists (`retail_pos/`, `tests/`); no product behaviour does. Run `python -m unittest` for the scaffold smoke tests and `python -m retail_pos --help` for the planned options. The fixtures describe expected results for future checks. No working baseline or passing implementation tests are claimed beyond those smoke tests. Required runtime versions and offline dependencies must be checked before the first build.

## Licensing

A license for this project has not been selected. Any upstream reference or adapted code must retain its applicable notices; see the plan.
