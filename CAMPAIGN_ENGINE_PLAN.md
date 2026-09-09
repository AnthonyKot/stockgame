# Campaign engine implementation plan

Planning only, 9 September 2026. [MASTER_PLAN.md](MASTER_PLAN.md) owns product scope. This document prepares the difficult accounting and timing work; it does not change the immediate task of finishing Nektar in [TODO.md](TODO.md). Numerical rules labeled “proposed” are game-design choices, not historical broker rules or user-approved parameters.

## Architecture: keep one clock and one ledger

Reuse the static app, evidence pipeline and chart components. Introduce a pure campaign engine separate from rendering. Do not add up `SIM.simulate()` portfolio returns: that function assumes a fresh account per trade and already knows its eventual exit.

Proposed files:

| File | Responsibility |
| --- | --- |
| `scripts/build_campaign.py` | Validate a closed interval; normalize sessions, actions and eligible story updates; produce manifest and dated data slices |
| `site/campaign-engine.js` | Pure command validation, event application, positions, balances and valuation; usable from Node tests |
| `site/campaign-store.js` | Versioned persistence, revision checks, recovery and export |
| `site/campaign.html` | Current scene, portfolio strip, updates, trade ticket and advance control |
| `site/data/campaigns/<version>/manifest.json` | Rules, start/end, instrument IDs, opaque chronological scene schedule, coverage metadata |
| dated slice files | Market events and public story material through a requested checkpoint; never a complete future price series |

API sketch:

```text
validateCommand(state, command, visibleData) -> accepted | reason
applyEvent(state, event, rules) -> newState
advance(state, eligibleEvents, targetTimestamp) -> proposedState + notices
portfolioView(state, eligibleMarks) -> equity, cash, positions, income, costs
visibleStory(state, documents) -> documents available at state.clock
```

No network, DOM, randomness or wall-clock time inside the engine. Appending a decision and advancing history are separate transactions. A trade commitment never directly calls the old full-outcome debrief.

## Minimum data model

Manifest: `campaign_id`, immutable `content_version`, `rules_version`, `start_at`, `end_at`, starting cash/BTC, price conventions, session calendar, horizon eligibility by scene, cost and margin parameters.

State: schema/content/rules versions, revision, simulated clock and event cursor, scene progress, orders, positions, ledger, latest eligible marks, and completion status. Save human decision time separately from simulated time.

Order: stable ID, originating scene, action, selected percentage, decision equity, fixed dollar budget/notional, reservation, intended horizon, pending/filled/rejected status and eventual fill.

Position: stable ID, instrument, direction, quantity, entry fill, cost basis, scheduled exit, collateral bucket if short, distributions, costs, and open/pending-close/closed status. Separate lots even if the same instrument appears again.

Event: stable ID, effective timestamp, event kind, instrument/position reference, source reference and payload. Public content also needs `available_at` and timestamp precision. Accounting event time and document availability are not interchangeable.

Ledger entry: event ID, account debits/credits or explicit cash/quantity deltas, reason, before/after balances, source and rule version. Store monetary precision consistently; proposed implementation uses decimal arithmetic or scaled integers with documented rounding. Do not round holdings to display precision after every event.

## Accounting identity

Use separate balances for free cash, order reservations, short collateral and restricted short-sale proceeds. All are assets, but only free cash is spendable.

```text
equity = free cash + reserved cash + restricted cash
       + BTC market value + long market value
       + dividend receivables
       - short market liability - dividend payables - accrued unpaid fees
```

Moving free cash to a reserve changes buying power, not equity. Receiving short-sale proceeds creates an equal short liability before costs, not instant wealth. Paying an accrued fee reduces its liability and cash together; do not expense it twice.

At closure, reconcile the position's realized P/L from actual fills, distributions and costs. Never calculate a short's return by negating the long return.

## Allocation and fills — proposed mechanics

Freeze the dollar budget as selected percentage × marked equity at commitment. The player chooses a dollar allocation, not a share count based on an unknowable next opening price.

- Long: reserve that budget now. At the eligible open, buy fractional shares such that price plus declared slippage fits the budget. This avoids silently resizing because of an overnight gap. Display that final quantity is determined at execution.
- Short: freeze gross short notional. Reserve the declared collateral and execution-cost allowance now; at the open determine shares from notional/open. Restrict sale proceeds and charge costs once. Reject unaffordable orders explicitly.
- Do not use equity recomputed at the fill to change an already accepted order's target budget.
- No automatic BTC sale, account top-up or borrowing to fund an ordinary long purchase.
- Future proceeds cannot fund current orders. Multiple pending orders reserve cash cumulatively.

Clarify the short size label: 10% refers to exposure, while required reserved cash may differ. These rules should be reviewed before implementation because they are more explicit than the existing single-trade simulator.

## Event ordering and advancement

Use timestamped events with a stable secondary order, not a date-only loop. Session calendars must handle daylight saving, holidays and early closes. Never hardcode every New York open as one UTC hour.

Suggested ordering within a session:

1. Overnight accrual to the current timestamp and effective pre-open corporate actions/entitlements.
2. Public information available by the scene cutoff; valuation uses the last eligible completed observations. A 09:00 scene cannot use the 09:30 fill or that day's close.
3. Player commitment and cash reservation, if this is a decision stop.
4. At the open: scheduled/forced closes, then eligible pending entries, using a documented stable order. Already accepted entry reservations remain intact; a future opening sale did not retrospectively increase 09:00 buying power.
5. Cash distributions at modeled payment timestamps and other intraday events with trustworthy timing.
6. Session-close marks, fees and margin checks. A detected breach schedules a next-tradable-open cover; do not fill at the close already observed.

If only daily data exist, define conservative modeled phases rather than invent precise publication/payment times. Daily OHLC can be sliced so an open event contains only the open, with high/low/close released after the session ends. A full daily bar at 09:30 leaks future information.

`Advance` stops at the next user decision or meaningful update/closure; it may process many market sessions internally. Author update schedules from known publication events, not from future price extrema. Weekend BTC marks and calendar-day costs must still advance even when equities are closed.

## Dividends, splits and Bitcoin

Prefer ex-date entitlement plus payment-date cash: record a receivable/payable when entitlement is established, then settle it later. Selling after entitlement does not erase a receivable. If payment dates cannot be sourced, use an explicitly versioned ex-date cash approximation consistently in holdings and benchmark; do not imply exact payment-date buying power.

Preflight includes all required settlement events. The final trade closing does not justify discarding unsettled distributions: settle through a covered final settlement date or report the receivable/payable as a remaining asset/liability. Choose the finish convention before publishing the manifest.

Splits adjust quantity and per-share basis together; total value remains continuous except actual price movement. Use prices consistent with quantities. Current cached levels reconstructed around later splits need a dedicated audit before reuse in the ledger. In the initial prototype, exclude unsupported corporate actions rather than guessing treatment.

BTC stays at one coin initially. Choose one documented USD price series and valuation convention. At a checkpoint, use only the most recent completed eligible observation, display its timestamp and staleness. A UTC daily close cannot be used earlier that same day. Match BTC observations in the passive baseline.

## Shorts and insolvency — proposed simple policy

Prefer conservative isolated collateral for the first campaign: reserve 100% of initial short notional from the player's cash in addition to restricted sale proceeds. This is a game parameter, not a claim about brokerage requirements.

For each short, compute collateral equity = its restricted assets minus marked liability and accrued obligations. A proposed maintenance threshold is 30% of current short liability. On breach, schedule full cover at the next available open; no automatic collateral top-up or hidden liquidation of unrelated assets. Borrow and dividend obligations debit the short bucket, preserving their accounting trail.

Gaps can exceed collateral. Apply a deficit to remaining free cash, then record any unpaid debt explicitly. If obligations cannot be funded, block new orders and follow a defined account-default policy; do not clamp equity to zero or silently delete liabilities. Before shipping shorts, decide whether default ends play or triggers orderly liquidation of other assets. This unresolved choice is a release blocker for short-enabled campaigns, not for a long/skip engine fixture.

Use the existing illustrative 5% annual borrow assumption only if retained in rules, with an explicit day-count/accrual convention. No claim of reconstructed historical borrow availability. Accrual tests must cover weekends, holidays and covering at the open.

## Small arithmetic fixture

Synthetic prices only; disable fees and dividends for this fixture. Fractional shares allowed.

| Event | Free cash | Restricted cash | Long value | Short liability | BTC value | Equity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Start; BTC = $10,000 | 100,000 | 0 | 0 | 0 | 10,000 | 110,000 |
| Buy A: 10%, $11,000 at $100 = 110 shares | 89,000 | 0 | 11,000 | 0 | 10,000 | 110,000 |
| A reaches $120; BTC $8,000 | 89,000 | 0 | 13,200 | 0 | 8,000 | 110,200 |
| Short B: 10%, $11,020 at $50 = 220.4 shares; reserve full notional plus proceeds | 77,980 | 22,040 | 13,200 | 11,020 | 8,000 | 110,200 |
| Close A at $130 | 92,280 | 22,040 | 0 | 11,020 | 8,000 | 111,300 |
| Cover B at $40; release $13,224 | 105,504 | 0 | 0 | 0 | 8,000 | 113,504 |

Reconciliation: $3,300 long gain + $2,204 short gain - $2,000 BTC move = $3,504 change in total wealth. Passive cash plus BTC ends at $108,000; player trades add $5,504 in this fixture. This also catches the common error of counting short proceeds as profit.

## Save/resume and content versions

Compute the entire next transition in memory, validate identities/balances, persist the new versioned state, verify the save, then render/advance. Failed persistence leaves the previous scene and state visible with retry. Repeated commands and duplicate event IDs must not apply twice.

Use a separate campaign storage key; do not convert old independent quiz records into a fictional portfolio. Store a monotonic revision and reject stale-tab commands when the stored revision changed. Retain a recoverable prior snapshot/export strategy. Invalid stored data gets a recovery view, not an automatic reset.

Content/rule changes cannot silently rewrite an active run. Pin immutable versions. If a version becomes unavailable, offer export and an explicit new run. Ledger replay and snapshot restoration should produce the same state.

## Ending and spoilers

Before accepting any horizon, ensure its calendar-anniversary exit, actual eligible trading session, price coverage and required action/settlement data fit the fixed historical boundary. Apply the same check to API/engine commands, not just disabled buttons.

After all scenes are decided, continue processing until there are no pending entries, open timed positions or pending closes. Apply the selected settlement convention. All-skip runs still progress through all stories; they have no extra trade horizon to wait for. Value remaining BTC and compare the passive baseline at the exact same ending time.

Normal client requests should stop at the campaign clock. Use sequentially dated slices, not the current full `outcome.sim.path`. Opaque static URLs do not provide security; accept that private-MVP limitation explicitly. An authenticated server is a later option if competitive play needs protection.

## Implementation checkpoints

1. **Contract + fixtures:** settle proposed sizing, margin/default, dividend and timestamp choices. Write independent arithmetic/time fixtures; no UI dependency.
2. **Long/skip engine:** reservations, fills, BTC marks, overlap, exits, ledger reconciliation, save/resume. Test with synthetic data first.
3. **Short engine:** collateral, liabilities, borrow, dividend obligations, forced covers and default behavior. Short-enabled UI waits for these tests.
4. **Three real stories:** Nektar -> Madrigal -> JPMorgan is an existing chronological candidate set, subject to coverage audit. Integrate current story UI with shared portfolio and time-gated updates. Stop for user playtest.
5. **Ten-story campaign:** extend content only after the connected loop and accounting pass. Keep search/RAG deferred.

Essential tests: same-day cash ordering; unavailable horizons; split invariance; dividend entitlement versus payment; weekend borrow; short gap past collateral; duplicate events; reload during advance; storage rejection; competing tabs; zero/negative equity; no full-day close before market close; no future narrative before availability; last decision with positions still open; all-skip finish; baseline and ledger reconciliation.

The next session still starts with story polish. This plan is ready for the later campaign stage, not an instruction to use the remaining session quota on implementing it now.
