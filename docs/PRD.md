# Offline Retail POS Simulator

> This document specifies phase 1 of the program in [#39](https://github.com/jortega0033/offline-retail-pos-simulator/issues/39). Hour figures in it are early estimates for that phase; its open tickets add up to 60 to 95 hours (2026-11-24). Work that it defers is planned in the later phases only where the program names it.

Engineering plan for a fictional retail chain. One epic and six future tickets estimate **18–30 engineering hours**. The product, fault harness, and performance measurements are planned.

## Product requirements

A store operator needs to finish a sale during a head-office outage, give the customer a receipt, and later verify that all recorded transactions reached head office exactly once. A supervisor needs to see pending deliveries and reconcile the virtual cash drawer at shift close.

**First working slice.** Start one local register from a clean directory, open a shift, add a bundled item by keyboard, record exact virtual cash, and print or reopen the receipt. Restart the store process and recover the sale and receipt while head office stays unavailable.

**Target workflow.** Start two local store processes with separate databases and a head-office process. Disconnect one store, finish a sale, inspect its pending count, reconnect, and compare receipts with head-office totals. Split virtual cash across shares, apply a basket discount, issue a full compensating refund, and close the shift against a counted amount.

**Scope.** Synthetic catalog and stores, fixed currency, keyboard-first browser UI, printable receipts, full refunds, cash-up, and offline reconciliation. Real payments, personal data, tax integration, inventory reservations, loyalty, price distribution, and partial refunds are outside this epic.

**Finish line.** The clean-checkout demo records and reopens a receipt offline. A second demo reconciles two stores after disconnects and controlled process exits. Raw ledger rows match an independent fixture calculation. Repeated delivery changes neither count nor totals. Pending and blocked events are visible. Record resource-use results from execution.

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

## Epic E86 · Complete and reconcile fictional in-store sales offline

Deliver a register that records sales offline, reopens printable receipts, appends audited full refunds, and closes its drawer with an explicit variance. A separate head office catches up after disconnection and shows the exact fixture totals. Verify this workflow with repeatable duplicate-delivery and interruption checks.

| Ticket | Dependencies | Remaining effort |
|---|---|---:|
| E86-1 Working cash sale and receipt | — | 2–4 h |
| E86-2 Deterministic split and durable outbox | E86-1 | 3–5 h |
| E86-3 Central event acceptance and reconciliation | E86-2 event contract frozen | 3–5 h |
| E86-4 Offline queue, retries, and operator status | E86-2, E86-3 | 4–6 h |
| E86-5 Full refund and shift cash-up | E86-2 | 3–5 h |
| E86-6 Fault harness and offline acceptance | E86-4, E86-5 | 3–5 h |

**Parallel lanes.** E86-1 establishes the local receipt workflow. E86-2 freezes the event and reversal envelopes early so E86-3 can start while local persistence is finished. E86-5 can proceed in the register and ledger lane alongside E86-4 in the delivery lane. E86-6 combines the lanes and runs the independent checks.

### E86-1 · Working cash sale and receipt

Build launch, synthetic catalog and shift, keyboard basket, exact virtual cash confirmation, sale persistence, receipt history, and print view. **Acceptance and verification.** From a fresh data directory with head office unavailable, sell one 150-cent item by keyboard. The print view shows 150 and a stable receipt ID. Restart and reopen that receipt. An incorrect tender shows a clear error and produces no receipt. Document launch and verification commands.

### E86-2 · Deterministic split and durable outbox

Add basis-point discounts, largest-remainder allocation, checkout idempotency, sequence, and outbox persistence. Freeze sale and refund fixture envelopes. **Acceptance and verification.** Test 65 cents discount, net lines 358 and 224, and shares 146, 145, 291. The same request ID returns the original receipt. Changed input conflicts. A controlled pre-commit failure leaves no sale or outbox row. Successful finalization leaves one receipt and one pending event after restart.

### E86-3 · Central event acceptance and reconciliation

Implement the separate process, validated ingest, cursor and duplicate handling, and summary API from ledger rows. **Acceptance and verification.** Accept the first sequence from each store. Retrying the exact Store A sale preserves one central row and the same acknowledgement. A gap reports the expected sequence. Changed payload under the same identity conflicts. Invalid amounts and missing refund references leave ledger and cursor unchanged.

### E86-4 · Offline queue, retries, and operator status

Connect the outbox and build status and central summary views. Keep checkout available while the link is down. **Acceptance and verification.** Sell while disconnected and observe one pending event. Drop the acknowledgement after central commit. Restart or reconnect and see the original event confirmed with one remote row. Deliver two pending events in sequence. A persistent conflict pauses only the affected store, with pending and confirmed totals visible.

### E86-5 · Full refund and shift cash-up

Add original-receipt lookup, an immutable full reversal, one-refund enforcement, and cash closing snapshots. **Acceptance and verification.** Refund −582 once with exact negative shares. Concurrent attempts or retries create at most one reversal. The original receipt remains unchanged. Check expected cash of 10,000 and variance +2. A sale against a closed shift fails without creating an outbox row.

### E86-6 · Fault harness and offline acceptance

Build seeded two-store fixtures and a local CLI evidence report. Exercise the keyboard receipt path and each controlled exit checkpoint. **Acceptance and verification.** From fresh databases, see all three central events once and net 150. Recalculate from raw rows without using the summary logic. Report checkpoints actually executed. Confirm zero external browser requests for the demo. Report observed receipt latency and backlog catch-up with workload, environment, repeats, and failures.

[Official project inspiration](https://docs.google.com/document/d/1R5MyfVvn033KoXZXgXP65qRAXnhcjtVvO_VF7IxUZaA/edit?tab=t.ef9a30wzb1z5)
