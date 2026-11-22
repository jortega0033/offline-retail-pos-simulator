# Offline Retail POS Simulator: technical specification

Planning document. Implementation and verification remain future work.

## Technical design

### Runtime and interface

Use Python 3.12, standard-library SQLite and HTTP, and native HTML, CSS, and JavaScript. Store and head-office processes bind to separate loopback ports and own separate local databases. The CLI takes a role, data directory, port, and fictional store ID. Serialize writes within each process, bound body size, use parameterized SQL, and render receipt strings as text. Check loopback Host and same-origin Origin for browser mutations. The simulated service uses a fixed set of store IDs. Fault controls act only on fixture links and owned test subprocesses.

The register has product search, quantities, basket, discount, tender shares, and a finalize action. Provide tab order, visible focus, labelled errors, and a text summary of total and outstanding amount. Print from the persisted receipt, including transaction ID, store, shift, line and tender amounts, and any refund reference. The operator panel shows pending count, last confirmed sequence, and reasons for blocked deliveries.

### Money and shifts

Use integer minor units. Calculate line gross as price times quantity with checked bounds. Apply an integer basis-point basket discount with one round to the nearest cent, ties up. Allocate that rounded amount proportionally across positive lines by largest remainder with ties in line order. Use the same rule to split tender across positive integer weights, breaking ties in share order. The shares must add to the exact sale total. Finalization snapshots prices, rules, computed amounts, and tender shares.

An open shift records opening cash. Expected cash at close is opening cash plus signed cash events in the shift. Store the counted amount and variance as a closing snapshot. Reject new transactions against closed shifts. A still-open shift at the same store can record one full refund for an unrefunded original sale. Save it as a new signed event. Its amount and tender shares negate the original exactly. Preserve the original receipt. Enforce the one-refund limit with a unique origin reference.

### Local persistence and recovery

Each store owns tables for shifts, checkout requests, immutable sales and refunds, receipt line and tender snapshots, and mutable outbox delivery state. In a single explicit transaction, look up the request ID before checking shift state. A committed request ID with the same canonical input returns the same receipt, even after shift close. Changed input conflicts before writing. For a new request, validate the open shift, allocate the next sequence, append the event, persist its receipt snapshot, and enqueue the outbox payload. Commit before showing the receipt. Keep the unresolved request ID and submitted snapshot stable through a reload until the browser gets a definitive result. Enforce keys, valid references, uniqueness, and ranges in the database, and enable foreign keys on each connection.

Use one transactional database per process. The initial test profile uses rollback journaling and synchronous FULL on local disk. Reopen after controlled process exits and verify the resulting state. A store commit and central acknowledgement are separate steps. Report the test filesystem, journal settings, and SQLite version. Durability claims cover the observed process-interruption conditions. [SQLite transactions](https://www.sqlite.org/lang_transaction.html) · [SQLite synchronous settings](https://www.sqlite.org/pragma.html#pragma_synchronous) · [SQLite atomic commit assumptions](https://www.sqlite.org/atomiccommit.html)

### Reconciliation contract

Sync one contiguous event sequence at a time per store over bounded loopback requests. The versioned event contains store ID, sequence, event ID, shift ID, type, signed amount, line and tender integers, original sale ID for a refund, and a digest of normalized fields. Send the same saved payload on every retry. Head office revalidates identities, ranges, totals, refund references, and the digest before writing.

Head office keeps an immutable ledger with unique event ID and unique store-and-sequence, plus the greatest contiguous applied sequence. Appending an event and advancing that cursor commit together. An exact duplicate returns the original acknowledgement after digest comparison. A gap reports the next expected sequence. An identity with changed content returns a conflict and pauses that store. Central reports sum verified ledger rows and mark stale stores visibly.

Return acknowledgements after central commit. Confirm their store ID, sequence, event ID, and digest before marking the local outbox row confirmed. Disconnects and timeouts leave rows pending. Retry transient failures with capped delays and stop automatic retries on permanent conflicts. The test link can refuse a connection, delay a reply, or drop the reply after central commit. A store may still show pending after head office has recorded the event. Retrying resolves delivery status without recording the event twice. [SQLite uniqueness conflict handling](https://sqlite.org/lang_upsert.html)

## Deterministic fixture and verification

| Scenario | Expected result |
|---|---|
| Store A sale | Two notebooks at 199 and one pen at 249 total 647 cents. A 10 percent discount rounds to 65. Line discounts are 40 and 25. Net lines are 358 and 224, totaling 582. |
| Store A split | Weights 1, 1, 2 produce 146, 145, and 291 cents. Floors are 145, 145, and 291. The remaining cent goes to the first of the tied shares. |
| Store A refund | One reversal records −582 with shares −146, −145, −291. The original receipt still shows 582. A second refund fails. |
| Store A cash-up | Opening cash of 10,000 and counted cash of 10,002 after the sale and refund produce expected cash of 10,000 and variance +2. |
| Store B sale | One 150-cent eraser produces one receipt for 150. |
| Head office | Deliver Store B first. Deliver Store A's sale twice by dropping its first acknowledgement, then deliver the refund. The central ledger has exactly three entries. Store A net is 0, Store B net is 150, and combined net is 150. |

Use new local databases and generated IDs. Check screens, receipts, cursor and raw event rows against paper arithmetic or an independent decoder. Inject controlled exits before local commit, after local commit before the client reply, after central commit before acknowledgement, and after acknowledgement before marking the outbox. Restart only owned test processes. Expect an all-or-nothing store write, a recoverable receipt, and one central effect per event. For a separate seeded backlog, report pending counts, elapsed time, and recovery diagnostics. Run two stores before considering an eight-store or 100-exit run.
