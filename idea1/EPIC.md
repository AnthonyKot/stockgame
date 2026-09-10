# Epic 1: one portfolio through historical time

Extracted 10 September 2026 from [MASTER_PLAN.md](../MASTER_PLAN.md) (product authority) and [CAMPAIGN_ENGINE_PLAN.md](../CAMPAIGN_ENGINE_PLAN.md) (engine design). This document turns those two into one end-to-end game scenario with stories, acceptance criteria and the decisions still open. Where it and the master plan disagree, the master plan wins. Nothing here is implemented yet; the ten standalone cases in `site/` are the foundation.

## 0. Status

2026-09-10: first milestone built in this repo (`site/campaign.html`, engine, store, builder, two test suites): three stories, long and skip, Bitcoin marked, ex-date dividends, automatic closures, a reconciled report, save and resume. Playtest pending. Shorts, dated story updates between stops, and the ten-story campaign are not started. See ARCHITECTURE.md for the file map.

## 1. The scenario, end to end

The player is one person with **$100,000 cash and 1 Bitcoin** on the morning of **15 February 2018**. They meet ten investment stories in the order they happened, decide each one from what was public that morning, and live with the consequences in one shared account until the last timed trade closes. The clock only moves forward. Nothing from a story's future is shown until the clock reaches it.

### The ten stops, in campaign order

| # | Date (09:00 New York) | Story (masked until revealed) | Default hold | Horizons that fit the data |
|---|---|---|---|---|
| 1 | 2018-02-15 | Nektar: a mid-cap biotech signs a multibillion-dollar oncology partnership | 5y | 1, 3, 5 |
| 2 | 2018-11-13 | Madrigal: a small-cap presents positive Phase 2 liver-disease data | 5y | 1, 3, 5 |
| 3 | 2019-01-16 | JPMorgan: a large bank reports record profit at the end of a rate cycle | 5y | 1, 3, 5 |
| 4 | 2019-02-05 | Gilead: an HIV/HCV giant with a shrinking franchise and $31bn of cash | 5y | 1, 3, 5 |
| 5 | 2019-12-17 | Axsome: a depression drug hits its second pivotal trial | 1y | 1, 3, 5 |
| 6 | 2020-08-24 | Deere: a cyclical equipment maker cuts costs at the bottom | 3y | 1, 3, 5 |
| 7 | 2021-01-08 | Sarepta: a gene therapy hits its biomarker, misses function | 3y | 1, 3, 5 |
| 8 | 2021-03-03 | Target: a pandemic-year surge and no guidance | 3y | 1, 3, 5 |
| 9 | 2022-03-02 | First Solar: profit guided to zero while capacity is built | 1y | 1, 3 (5y exit 2027 is beyond coverage) |
| 10 | 2023-02-03 | Hershey: pricing-driven growth, decelerating guidance | 1y | 1, 3 (5y exit 2028 is beyond coverage) |

Price coverage in the repo ends 2026-09-09. The latest exit any offered horizon can schedule is Target's five-year anniversary, **2026-03-03**, so the campaign's fixed end is on or shortly after that date (settlement convention decides, see section 5). Every offered horizon must have its actual exit session and all settlement events inside that boundary; a horizon that does not fit is disabled with a one-line reason, never shortened.

### What one stop looks like

1. **Arrive.** The date, total equity, free cash, Bitcoin quantity and value, and each open position with direction, size, current gain or loss and scheduled exit. A short "since your last stop" note: dividends received or owed, borrow costs, positions that closed and their result, Bitcoin's move.
2. **Story.** The existing scene: pitch or warning, three friend questions, the packet, the chart. All of it ends at this morning's cutoff. A position opened at an earlier stop may be in this same sector; its later story is still hidden.
3. **Decide.** Buy, skip or short; 1, 3 or 5 years among the horizons that fit; 5, 10 or 20% of current equity. The ticket shows the dollar budget that percentage means today and whether free cash covers it. An unaffordable order is refused with the reason; nothing is silently resized. Assumptions and reason are recorded as today.
4. **Commit.** The decision, budget, horizon and execution assumptions are saved before anything advances. The entry fills at the next eligible open with fractional shares inside the budget.
5. **Advance.** The engine walks every session between this stop and the next: marks, dividends on their dates, borrow accrual on calendar days, scheduled exits at anniversary opens, forced covers if a short breaches its collateral rule, Bitcoin marks including weekends. It stops at the next story, or earlier at a closure or a dated story update worth showing.
6. **Debrief on closure.** When a position closes, its debrief is available through its closing date only: the exit-scoped thesis feedback that exists today, but gated by the campaign clock rather than by the commit. Alternative horizons for that trade unlock only when the clock reaches their dates.

### After the tenth decision

The game does not end. The player keeps advancing until every timed position has closed: a five-year Target buy made in March 2021 runs to March 2026 while the clock passes Hershey and beyond. An all-skip run still walks through all ten stories and then finishes at once, because it has no timed trade to wait for. Bitcoin is never force-sold; it is valued at the ending timestamp.

### The ending

One report that reconciles starting and ending wealth: every decision and its exit, realized results per position, dividends and income, slippage and borrow costs, the remaining Bitcoin and cash, the portfolio path, and a passive comparison that started with the same $100,000 and 1 BTC and did nothing. Gains from Bitcoin are separated from gains from the player's calls. The report explains reasoning and uncertainty; a profitable outcome is not presented as proof of a good decision.

## 2. Scope

**In Epic 1**

- One campaign, ten stories in cutoff order, the roster above.
- Long, skip and short with the sizes and horizons above. Shorts ship only when the short stories in section 4 pass their tests; a long/skip campaign can ship first.
- Bitcoin as a passive starting holding, marked from one documented series.
- Time-gated content: the campaign clock, not a commit, controls every reveal.
- Save and resume in the browser, deterministic, duplicate-safe.
- The ending report and the cash-plus-Bitcoin baseline.

**Out of Epic 1** (master plan): manual early exits, resizing, reversals, deposits, Bitcoin trading, accounts, leaderboards, a general search or RAG platform, a server. Static files remain readable by a curious player; the epic states that limitation rather than claiming spoiler-proof security.

## 3. Stories and acceptance criteria

Numbered for reference. Each story is done when its criteria hold in an automated check where one is possible, and in a playtest where it is not.

**S1 Campaign manifest and coverage audit.**
A versioned `manifest.json` with campaign id, immutable content and rules versions, start and end timestamps, starting cash and BTC, session calendar, the chronological scene schedule, and per-scene horizon eligibility.
- Every offered scene/horizon has its anniversary exit session, prices through it and all settlement events inside the end boundary; the audit script lists any that do not and they are not offered.
- The manifest records the price, dividend and Bitcoin conventions it relies on.

**S2 Ledger engine, long and skip.** A pure module (`site/campaign-engine.js`, runnable in Node) with `validateCommand`, `applyEvent`, `advance` and `portfolioView`, no DOM, network, randomness or wall clock.
- Separate balances: free cash, reserved cash, restricted cash, long value, short liability, BTC value, receivables, payables, accrued fees. The equity identity in the engine plan holds after every event.
- Allocation is percentage × marked equity at commitment, frozen as a dollar budget; the long fill buys fractional shares within budget including slippage; an unaffordable order is rejected with a reason.
- Overlapping positions constrain later orders; pending orders reserve cash cumulatively; a future fill never funds an earlier decision.
- The engine plan's synthetic fixture reconciles to the cent.

**S3 Time advance and event ordering.** Timestamped events with a stable secondary order; the session calendar handles holidays, early closes and daylight saving.
- Within a session: accrual and pre-open actions, then public information to the cutoff, then commitment, then at the open scheduled and forced closes before pending entries, then distributions, then close marks and margin checks.
- A 09:00 decision never sees that day's open, high, low or close. Daily bars are sliced so the open is released at the open and the rest after the close.
- Advancing across a gap processes every intervening session and calendar day; nothing is skipped when the UI jumps.
- Anniversary exits fill at the first eligible open on or after the anniversary; 29 February maps to 28 February as today.

**S4 Bitcoin.** One coin, passive.
- One documented USD daily series is added to `research/prices` with its source and timestamp convention; the repo has none today.
- Valuation at a checkpoint uses the most recent completed observation, shown with its timestamp and staleness; a UTC daily close is not used earlier that same day.
- Weekend and holiday marks advance; the passive baseline uses the same observations.

**S5 Dividends, splits and corporate actions.**
- Ex-date entitlement with payment-date cash where payment dates are sourced; otherwise an explicitly versioned ex-date convention applied identically to holdings and baseline. Never counted in both cash and an adjusted price.
- Splits adjust quantity and basis together with no value discontinuity. The cached levels un-adjusted for later splits get an audit before ledger use; unsupported actions exclude the scene rather than guess.
- Selling after entitlement keeps the receivable; the campaign end settles or reports every open receivable and payable.

**S6 Shorts.** Behind the long/skip engine; a release blocker only for short-enabled play.
- Short proceeds are restricted, never spendable; collateral of 100% of initial notional is reserved from free cash (proposed game parameter); maintenance breach at 30% of current liability (proposed) schedules a full cover at the next open, never a fill at the observed close.
- Borrow at the retained 5% annual rate with a stated day-count, accruing on calendar days; dividend obligations debit the short bucket.
- A gap beyond collateral applies to free cash and then records explicit unpaid debt; new orders are blocked; the default policy in section 5 decides what happens next.
- A short's result comes from its own fills, distributions and costs, never from negating the long return.

**S7 Campaign screen (`site/campaign.html`).**
- Persistent portfolio strip: date, equity, free cash, BTC, open positions with exit dates.
- "Since your last stop" summary with every closure, dividend and cost since the previous stop.
- The existing scene and packet, unchanged in substance, below the strip; the ticket shows dollar budget and funding constraint; ineligible horizons disabled with the reason.
- An "advance" control when only existing positions remain; a clear end state.

**S8 Time-gated content slices.** `scripts/build_campaign.py` produces dated slices, not whole-future files.
- Market data and story updates are served only through the requested checkpoint; the current full `outcome.sim.path` is not loaded by the campaign page.
- A trade's debrief becomes available at its closing date; alternative-horizon results unlock at their own dates or after the campaign, labelled.
- Story updates are authored from publication events, and a retrospective source unlocks at its publication, as `site/story.js` already does.
- The payload checker runs on every slice in the build.

**S9 Save, resume and versions (`site/campaign-store.js`).**
- A separate storage key from the quiz journal; old quiz entries are never converted into a portfolio.
- Each transition is computed in memory, validated, persisted with a monotonic revision, read back, then rendered. A failed save leaves the previous state visible with retry.
- Reload during an advance never duplicates a fill, dividend or closure; a stale tab's command is rejected.
- Content and rule versions are pinned to the run; a missing version offers export and a new run, never a silent rewrite.

**S10 Ending report and baseline.**
- Every timed position closed on or before the fixed end; remaining BTC valued at the end; the cash-plus-BTC baseline valued at the same instant.
- Ledger replay from events and the saved snapshot produce the same balances.
- The report separates trade results, income, costs and Bitcoin, and lists every decision with its exit.

**S11 Tests in the one runner.** New suites join `scripts/run_checks.sh` and the CI gate: same-day cash ordering; unavailable horizons; split invariance; entitlement versus payment; weekend borrow; short gap past collateral; duplicate events; reload during advance; storage rejection; competing tabs; zero and negative equity; no full-day bar before the close; no narrative before availability; last decision with positions open; all-skip finish; baseline and ledger reconciliation.

**S12 Prototype, playtest, extend.**
- Three chronological stories with overlap and at least one automatic closure (Nektar, Madrigal, JPMorgan is the candidate set), run to their closures with Bitcoin and a reconciled report.
- User playtest at that checkpoint; no extension to ten before it.

## 4. Decisions to settle before building

These are open in both plans and must be chosen and written into the manifest, not discovered in code.

1. **Start and end timestamps.** Proposed: start 2018-02-15 09:00 New York; end the first session on or after the last offered exit (2026-03-03) plus the settlement window chosen in item 5.
2. **Bitcoin series and convention.** Which daily USD series, which timestamp (UTC close), how a 09:00 New York stop maps to it.
3. **Short parameters.** Collateral share, maintenance threshold, borrow day-count, and the default policy: does an unfundable obligation end play or trigger orderly liquidation of other assets?
4. **Same-timestamp ordering.** Confirm the section-3 order, including where a new decision's reservation sits relative to that morning's fills.
5. **Dividend convention.** Payment-date cash where dates are sourced, or a single ex-date convention for the whole campaign; and the finish rule for unsettled receivables.
6. **Allocation semantics for shorts.** 10% means gross exposure; state what cash is reserved and show both on the ticket.
7. **Baseline.** Cash-plus-BTC is required; whether to add a labelled SPY-plus-BTC alternative.

## 5. Sequence and checkpoints

1. Decisions above written into a draft manifest; independent arithmetic and time fixtures (S1, S2 fixture, S3, S4 data).
2. Long/skip engine with synthetic data, save/resume, ledger reconciliation (S2, S3, S9, S11 subset).
3. Coverage audit and dated slices for the three-story prototype; campaign screen (S1, S7, S8).
4. **Pause: user plays the three-story prototype** (S12). Nothing past this point starts before the playtest.
5. Short engine and its tests (S6); short-enabled UI only after they pass.
6. All ten stories, ending report, full test set in CI (S5 audit, S10, S11).

## 6. Dependencies and data work

- A Bitcoin daily series (none in the repo).
- Dividend ex and payment dates for the ten issuers through 2026-03; today's bundles carry amounts on ex-dates only.
- A split audit of cached price levels for any window that crosses a split.
- A New York session calendar with holidays and early closes for 2018 to 2026.
- The existing scene, evidence, aftermath and dated-debrief content, reused unchanged; the standalone quiz stays as an authoring and testing surface.

## 7. Definition of done

The master plan's acceptance criteria, verbatim: one persistent portfolio with no reset or double counting; overlapping positions that constrain later allocations; a clock that never moves backward and never leaks; closures, income and costs exactly once at the right simulated times; short collateral that keeps restricted proceeds out of buying power; deterministic resume; decision ten does not end the game while positions are open; every offered horizon has a covered exit; a finish with every timed position closed and a reconcilable report including Bitcoin and the same-starting-assets benchmark.

## 8. Working agreement

Engine, store, builder and tests are one lane; scene content, dated slices' editorial text and the campaign screen's copy are the other. Both sessions run `scripts/run_checks.sh` before every push, and the CI gate blocks a deploy that fails. Structural changes update ARCHITECTURE.md in the same commit. The playtest pause in section 5 is a hard stop.
