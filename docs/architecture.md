# Implementer map (planned, not implemented)

Nothing described here exists yet. [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) states the design; this page adds only what an implementer needs and the spec leaves open: where code lives and who owns which data. Names are defaults chosen by the plan. The first ticket (#2) confirms or changes them here in the same pull request.

## Processes

| Process | Started by | Owns | Talks to |
|---|---|---|---|
| Store | `python -m retail_pos --role store ...` | its SQLite database, the static register UI, the outbox | head office, over bounded loopback HTTP |
| Head office | `python -m retail_pos --role head-office ...` | its SQLite database: ledger, per-store cursor, reports | stores answer to it only through acknowledgements |
| Fixture link | the fault harness, tests only | nothing | sits between a store and head office to refuse, delay or drop replies |

## Module map

One package, `retail_pos/`, plus `tests/`. Each row is a boundary; a new module is fine when a file would otherwise take a second job.

| Module | Job | Must not |
|---|---|---|
| `cli.py`, `__main__.py` | arguments (role, data directory, port, store ID), start-up errors | hold business rules |
| `http_common.py` | request guards (loopback Host, same-origin Origin, body cap), JSON in and out, static files, error envelope | run SQL, compute money |
| `money.py` | integer minor units, line gross, basis-point discount, largest-remainder allocation and split | do I/O, import `sqlite3` |
| `contract.py` | versioned event envelope, canonical form, digest, validation of a received envelope | do I/O |
| `store/` (`db.py`, `checkout.py`, `shifts.py`, `refunds.py`, `outbox.py`, `sync.py`, `routes.py`) | store schema and transactions, sale and refund logic, delivery of outbox rows, store routes | read head-office tables |
| `head_office/` (`db.py`, `ingest.py`, `reports.py`, `routes.py`) | ledger, cursor, acknowledgement, summaries | read store tables |
| `faults.py` | named checkpoints that exit the process, enabled only by a test-only switch | be reachable from a browser request |
| `static/` | register, receipt print view, operator panel, cash-up and refund screens in native JavaScript | use `innerHTML` for receipt or catalog text; call another host |
| `demo.py`, `evidence.py` | repeatable demo; two-store evidence report | change production behavior |
| `tests/` | `unittest`: pure arithmetic, storage, HTTP over a real server on an ephemeral port, restart and interruption cases, static-asset scan | use a fixed port or the network |

`db.py` in each process is the only code that imports `sqlite3`. Both databases use rollback journaling, `synchronous=FULL` and `PRAGMA foreign_keys=ON` on every connection ([TECHNICAL_SPEC.md](TECHNICAL_SPEC.md), "Local persistence and recovery").

## Data ownership

- Store: shifts (opening cash, closing snapshot), checkout requests (request ID, canonical input), immutable sales and refunds with receipt line and tender snapshots, and the mutable outbox (frozen payload, delivery state, last error). Sequence numbers per store are allocated here and nowhere else.
- Head office: an immutable ledger (unique event ID, unique store and sequence) and the greatest contiguous applied sequence per store, advanced in the same transaction as the append. Reports are computed from ledger rows, not from a cached total.
- The versioned event envelope is the only thing that crosses the process boundary. Its exact fields are frozen by ticket #3 (E86-2) and listed in `contract.py`; ticket #4 may not change them.

## Where each rule is stated

Money and shifts: [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md), "Money and shifts". Idempotency, single transaction, commit-before-receipt: "Local persistence and recovery". Ledger, cursor, acknowledgements, retries, link faults: "Reconciliation contract". Fixture numbers and interruption points: "Deterministic fixture and verification".

## Decisions this page makes that the plan did not

| Decision | Default | Where it is settled |
|---|---|---|
| Package and module names above | as listed | ticket #2 |
| Event digest | SHA-256 of the canonical JSON (UTF-8, keys sorted, no insignificant whitespace) of the normalized fields without the digest itself | ticket #3 |
| Test-only fault switch | environment variable read once at start, ignored unless the harness set it | ticket #3, used by ticket #7 |

Anything else the spec leaves open is an owner decision listed in the epic with its default.
