# Stockgame master plan: one portfolio through historical time

User-confirmed main product direction, 9 September 2026. This is the highest-priority product document. Where older documents disagree, this plan wins. Individual case layouts, role-play scenes, research/search UX and scoring ideas support this campaign; they do not replace it.

This records the intended game, not a claim that the campaign is implemented. The existing ten-case app and evidence bundles are the foundation. This documentation update does not authorize an unattended implementation batch or override agreed pause checkpoints.

## The game

The player starts at a historical timestamp with **$100,000 cash and 1 Bitcoin**, encounters ten investment stories in chronological order, and makes buy/skip/short calls from information available at each timestamp. One shared portfolio persists throughout. Capital does not reset between scenes.

Each call has a declared **1-, 3- or 5-calendar-year** holding period. The player can allocate **5%, 10% or 20%** to a long or simulated short position, or skip. Positions can overlap. The game automatically closes each position at its scheduled exit, subject to explicit market and forced-liquidation rules.

After the tenth decision, **keep playing forward until every timed position is closed**. Do not end the campaign at decision ten or jump to a five-year outcome while earlier decisions remain. The final Bitcoin holding can remain in the account, valued at the ending timestamp; it is not a timed trade that must be sold.

## Core loop

1. **Arrive at a timestamp.** Show the historical date, current portfolio value, available cash, Bitcoin and open positions. Explain changes since the last stop.
2. **Encounter a story.** A friend, headline or other scene introduces an investment opportunity. Research and charts reveal only what was available then.
3. **Make a call.** Choose buy/skip/short and an allocation. Persist the decision, intended holding period and execution assumptions before advancing.
4. **Advance time.** Process market valuation, dividends, borrow costs, corporate actions and scheduled/forced exits in chronological order. Show relevant updates and completed trades as they become available.
5. **Continue.** The next story uses the resulting portfolio and available capital. After all ten calls, continue through the remaining closures.
6. **Finish.** Show final assets and portfolio value, all decisions and exits, investment income, costs, the portfolio path and a passive comparison with the same starting assets.

Skipping leaves capital available for later opportunities. A long holding period commits capital across intervening stories. These consequences are central to the game.

## Portfolio and execution contract

Accepted direction, with numerical implementation details to be specified and tested before shipping:

- Allocation percentages refer to current portfolio equity, including marked Bitcoin and open positions; available cash constrains new trades. Show the requested dollar exposure and any funding constraint before commitment. Do not silently resize a trade.
- Starting equity is $100,000 **plus the starting USD value of 1 BTC**, not $100,000 inclusive of Bitcoin. No automatic capital reset or top-up.
- Treat Bitcoin as a passive starting holding for the first campaign. Trading it is a later feature. Use a documented historical USD series and timestamp convention; its continuous market must be aligned with stock-market timestamps.
- Long purchases consume cash. Short-sale proceeds are restricted, not additional spendable cash. Distinguish free cash, collateral, long asset value and short liability in the ledger.
- Shorts require an explicit collateral, borrow-cost and forced-liquidation policy. Choose and document the numerical policy before implementation; previous drafts' margin examples are not settled campaign rules. Process breaches between story dates, not only when a scene opens. Handle gaps and insolvency explicitly.
- Keep existing next-eligible-open entry and calendar-anniversary exit conventions where suitable. Display reference prices separately from fills. Specify ordering when fills, exits, distributions and a new decision share a date; cash from a future fill cannot fund an earlier decision.
- Credit long dividends and debit short dividend obligations as time passes. Prefer documented payment dates with correct entitlement; if coverage requires an approximation, declare the convention and apply it consistently to the benchmark. Do not count dividends twice in both cash and adjusted prices.
- Process applicable splits, terminal proceeds, delistings and other corporate actions consistently. Missing settlement or valuation data cannot silently become zero or an invented fill.
- Retain declared slippage, cash-yield and borrow assumptions unless deliberately revised. Label simulation assumptions and preserve them in the campaign version.
- Compare against a passive portfolio starting with the same $100,000 cash and 1 BTC. Retain that cash-plus-BTC baseline; an additional SPY-plus-BTC alternative is optional and must be separately labeled with consistent distributions and costs.

Exact campaign start/end dates, Bitcoin price source, margin parameters and same-timestamp event ordering remain implementation choices to resolve. They must not be presented as already verified behavior.

## Closed historical campaign

User clarification: the game is a **closed historical interval**, not a simulation into an unknown future. Freeze a campaign start and end timestamp in its versioned manifest. The end must be supported by complete verified price, settlement and event coverage for the offered trades and passive assets; today's date alone is not proof of coverage.

Only offer a scene/horizon combination if its actual scheduled exit (including adjustment to the next eligible trading session) fits within this end boundary and the required data is available. For example, do not offer a three-year investment starting in 2024 when its 2027 exit lies beyond the campaign's verified historical coverage. If horizons are selectable, disable ineligible choices with a short explanation. If a scene has one authored horizon, it must pass eligibility before inclusion.

Never shorten a promised holding period, force a normal trade to close at the data boundary, extrapolate prices or invent outcomes to make it fit. Replace or omit an ineligible scene/horizon during campaign authoring. Post-decision time advancement ends after the final actual timed trade closes, which must be on or before the fixed historical end. Any alternative-horizon comparisons follow the same coverage rule.

## Time and information boundaries

**The campaign clock controls every reveal. A saved trade does not unlock its future.**

- At each stop, prices, charts, headlines, financial facts and narration end at the current information cutoff.
- A five-year position stays open while intervening stories occur. Its eventual result and later narrative remain unavailable until the clock reaches them.
- A closed trade can receive a debrief through its closing timestamp. Alternative 1/3/5-year outcomes cannot be revealed early just because this trade closed; unlock them only once the campaign clock reaches those dates, or after the campaign where clearly labeled.
- Separate event occurrence time from public availability time. A retrospective source describing an earlier event is not evidence that the player could read that description at the earlier stop.
- Advance the ledger through intervening sessions/events even when the UI jumps between selected stops. Do not skip borrow accrual, dividends or forced exits during a time jump.
- Reveal only the relevant dated slices in normal app payloads. Hiding full future data in the DOM or chart is insufficient. Static files are not access control; retain the private MVP limitation explicitly rather than claiming spoiler-proof security.
- Save enough campaign state to resume deterministically: clock, scene progress, orders, positions, scheduled exits and processed ledger events. Reloading must not duplicate a fill, dividend or closure.

## Main screen and ending

The portfolio is persistent context, not a separate optional analytics feature. At minimum show:

- Current date and total portfolio value.
- Available cash and Bitcoin quantity/value.
- Open positions with direction, allocation, current gain/loss and scheduled exit.
- A concise “since your last stop” update with dividends, costs and closures.
- The current story and decision controls, or an advance action when only existing positions remain.

Keep the investment scene readable. Detailed financials, source excerpts and research interactions can be progressively disclosed. Role-play and the possible search experience in `RAG.md` are supporting layers.

The final report reconciles starting and ending wealth, realized trade results, income, costs and remaining passive assets. Distinguish gains from Bitcoin from gains from player calls. Explain reasoning and uncertainty without treating one profitable outcome as proof of a good decision.

## Build sequence and scope

1. Inspect current code and reuse the ten selected stories, source evidence, price caches and existing UX work. Order stories by cutoff and audit coverage through the last scheduled exit. Do not restart the 30-story research exercise.
2. Define the campaign manifest, shared portfolio ledger and event/visibility rules. Resolve the execution details above with concrete examples.
3. Prototype **three chronological stories with overlapping positions and at least one automatic closure**, then continue until their timed trades close. Include Bitcoin valuation and a reconciled final report.
4. Verify accounting, temporal isolation and save/resume; let the user play the prototype at an agreed pause checkpoint.
5. Extend the same system to all ten stories. Scale content only after the connected loop works.

Manual early exits, resizing, reversals, deposits, Bitcoin trading, accounts, leaderboards and a general RAG platform are outside this first campaign scope. Existing standalone quizzes can remain useful for authoring/testing, but are no longer the primary product destination.

## Acceptance criteria

- One starting portfolio persists across all decisions, with no reset or double counting.
- Multiple positions can overlap and constrain later allocations.
- The clock never moves backward; future outcomes do not leak into earlier scenes.
- Automatic closures and intervening income/costs occur exactly once at the correct simulated times.
- Short collateral and liquidation prevent restricted proceeds from becoming free buying power.
- Saved campaigns resume to the same balances and progression.
- Decision ten does not end the game while timed positions remain open.
- Every offered horizon has a covered exit within the fixed historical boundary; unavailable future horizons cannot be selected.
- The campaign finishes with every timed position closed and a reconcilable report including remaining Bitcoin and a same-starting-assets benchmark.
