# Stockgame checklist — 10 September 2026

## Scope and checkpoint

The immediate work is standalone story refinement and user playtesting. The connected campaign remains the long-term direction in [MASTER_PLAN.md](MASTER_PLAN.md), with implementation deferred. This checklist records completed changes and planned next work. The user authorized the four engineering points; implementation and verification are recorded in the session progress log.

Read [the latest review](research/DATED_DEBRIEF_REVIEW.md) before implementing its repairs. Preserve existing code, journal entries and concurrent edits.

## Completed — do not repeat

- [x] Ten standalone stories with opening scenes, three investigation questions, selectable assumptions and aftermath material.
- [x] Shared horizon selector, unavailable-horizon controls, allocation choice and optional stop-loss/take-profit levels.
- [x] Optional free-text rationale; one or two selected assumptions required where authored. New decisions save no default probability (`p_beats_spy: null`); older forecasts remain in the journal.
- [x] Save-before-reveal, failed-save feedback, walkthrough resume and persistence checks; legacy completed entries remain accessible.
- [x] Progress count and next-undecided navigation; journal name, skip-return and exit-column fixes.
- [x] Stock/SPY dividend-aware calculations, derived valuation and masked pre-decision excerpts.
- [x] Nektar opening corrected to agreed $1 billion cash plus $850 million equity, pending closing; duplicated investment question removed when a scene supplies one.
- [x] Nektar walkthrough chronology repaired; unsupported closing/legal/cash-retention clauses trimmed. Date precision preserved.
- [x] Dated debrief mechanism uses actual exits and eligible event/publication dates. Nektar's one/three/five-year paths have one/two/four stops; early exits can have fewer or none.
- [x] Dated feedback authored for the other nine cases using the same schema. This is implementation coverage, not complete editorial approval.
- [x] Default debrief: result and exit-bounded chart, selected-thesis feedback, concise narrative; full story and other horizons behind optional context.
- [x] Nektar financial snapshot reorganized into business performance, cash position and valuation. One-time-payment caveats visible; non-comparable cash prior kept out of the primary comparison; definitions and formulas expandable.
- [x] Removed repeated cutoff/holding line from the company summary.
- [x] Moved last-close value/date into Market snapshot and placed it before Where the stock stands.
- [x] Moved What changed directly before Financial snapshot.
- [x] Aligned stop-loss and take-profit labels/dropdowns.

Interim findings, ownership and step completion: [SESSION_PROGRESS.md](research/SESSION_PROGRESS.md).

## Current checkpoint

The four authorized engineering points are implemented locally: copied-outcome payload checks, explicit temporal selection fixtures, legitimate returns to Unresolved, whole-batch atomic dated merging and integration with valuation commit `0b1a673` and scene-text commit `c4de944`. Valuation presentation merges also preserve and validate `valuation_mode`.

See [SESSION_PROGRESS.md](research/SESSION_PROGRESS.md) for actual verification. The next user-facing step is playtesting. The original [NEXT_SESSION_PLAN.md](research/NEXT_SESSION_PLAN.md) remains a record of the broader proposed work; unchecked editorial/user-review items are not silently completed by automated checks.

## Remaining repair verification and implementation

The checklist below now distinguishes landed patches from remaining review. Detailed timing, deliverables and pause points are in the session plan. No new schema or research-worker batch is needed.

- [ ] **Target:** verify the landed fix for the March/May/June guidance chronology and remove the inference that later guidance cuts prove management's earlier intent. Review a3's updates together.
- [ ] **First Solar:** verify the landed corrections keep verdicts tied to the stated assumptions. Enactment and durability are different questions; factory openings do not establish demand utilization.
- [ ] **Sarepta:** verify the landed corrections distinguish gross debt issuance from new program funding, age eligibility from the approval's surrogate-endpoint basis, and the original subgroup assumption from a broader population.
- [x] Review the new verdict and publication-boundary tests; add independent expected-output fixtures where needed, and replace the universal status-regression ban with checks that permit evidence-backed uncertainty. Expand early-exit coverage where relevant.
- [x] Strengthen pre-decision payload checks beyond absence of the `dated_debrief` key. Retain manual clause/source review; structural tests cannot establish factual support.
- [x] Finish merge recovery beyond the landed save-before-delete fix: validate the whole batch, save atomically, then archive/delete inputs. Test failed writes and invalid batches; correct misleading validator documentation.
- [ ] User playtest after local integration checks; record remaining editorial feedback.
- [ ] Presentation merge multi-file transaction recovery (dated merging is fixed separately).

Detailed evidence, replacement wording and acceptance criteria: [DATED_DEBRIEF_REVIEW.md](research/DATED_DEBRIEF_REVIEW.md).

## Later standalone work

- [ ] Continue user playtesting after the recent layout changes; assess whether the snapshot and investigations make the decision easier.
- [ ] Review remaining investigation clauses, valuation interpretations and full-record archive wording against sources. Include Madrigal’s raw funding-runway unit wording; mobile wrapping is fixed.
- [ ] Triage `repairs_needed` into blocking versus optional work before adding a publication-readiness gate. `sheet_ready` currently does not certify factual completeness.
- [ ] Consider friend follow-ups only if useful after playtesting; this is optional, not a completion requirement.

## Campaign — deferred

Follow [CAMPAIGN_ENGINE_PLAN.md](CAMPAIGN_ENGINE_PLAN.md) and MASTER_PLAN when campaign work resumes:

- [ ] Freeze a historically covered interval and eligible horizons.
- [ ] Implement a shared ledger, sourced BTC valuation, cash/position accounting, dividends, borrow/collateral rules and event ordering.
- [ ] Replace immediate future payloads with campaign-clock-controlled updates.
- [ ] Prototype three chronological scenes with overlap and an automatic closure; continue until every timed trade closes, then reconcile the final portfolio and passive comparison.
- [ ] Pause for playtesting before extending the connected loop to ten scenes. [RAG.md](RAG.md) remains separate and deferred.

## Verification and running

Serve locally: `python3 -m http.server 8765 --directory site`. Port 8766 was also used during this session; check whether a server exists before starting another. Nektar: `/play.html?case=146743bdc9`. Use a private window for a fresh playtest; never clear the user's journal automatically.

For content changes, run `python3 scripts/verify_cases.py`, `python3 scripts/merge_dated_debrief.py --check-only`, then `python3 scripts/build_bundles.py`. The merge command is read-only only with `--check-only`.

Relevant regression commands:

```bash
python3 scripts/test_returns.py
node scripts/test_simulate.js
python3 scripts/test_merge_dated_debrief.py
python3 scripts/test_merge_presentation.py
node scripts/test_payloads.js
node scripts/test_story_dates.js
node scripts/test_dated_debrief.js
```

Browser regression, with the server running:

```bash
PLAYWRIGHT_MODULE=/home/diablo/book11/node_modules/playwright \
CHROMIUM_PATH=/home/diablo/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell \
STOCKGAME_URL=http://127.0.0.1:8765 \
node scripts/test_story_ui.cjs
```

Current execution results are recorded in research/SESSION_PROGRESS.md. Run scripts/test_presentation_ui.cjs with the same browser environment for valuation integration coverage. The all-case dated test covers 28 available horizon exits. Browser coverage includes Nektar 1/3/5-year, buy/short/skip, stop/target, no-event exit, reload, failed commitment/progress saves, desktop/390px, optional context and journal behavior. It does not constitute an exhaustive all-ten content or accessibility audit.

The review verified deployment `ee0752c` and matching live outcome bundles. Do not infer that subsequent UI changes are deployed without a new check. No current quota or worker-availability claim is made.
