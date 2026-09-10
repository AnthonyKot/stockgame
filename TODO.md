## Nektar exit-aware debrief — 10 September 2026

Implemented the user-approved bounded patch; pause for Nektar playtesting before any rollout or campaign work.

- Nektar walkthrough and selected-thesis feedback use the actual simulated exit, including stop-loss and take-profit exits. One-/three-/five-year windows retain one/two/four authored stops respectively; earlier exits include only eligible stops.
- New outcome-only `scene_check.dated_debrief` contains baseline interpretations and event-linked updates. `site/story.js` selects evidence using both occurrence and source publication dates. Date-only evidence must precede the opening-price exit; month-only dates use month end conservatively. Retrospective legal material is not eligible at its earlier occurrence date.
- Results and primary stock/SPY chart for Nektar end at the actual exit; the final chart point uses the exit open, not that day's later close. Same-date benchmark tiles and drawdown reflect that boundary. Saved legacy forecast/calibration semantics remain unchanged.
- Default order: results/chart, selected-thesis check with source links, concise exit-scoped narrative. Full friend checks, horizon notes, event archive and alternative horizons are in a closed optional later-context section. Full outcome payloads still load after commitment; this is standalone presentation scoping, not campaign time-gating or access control.
- Removed unsupported closing/legal/cash-retention clauses from three Nektar walkthrough stops. Reused existing evidence; 2019 and April 2022 wire sources reopened during this patch, but the two SEC source URLs could not be reopened. This is not a complete source re-verification or readiness certification.
- Verified: all ten cases (`verify_cases.py`), builder regeneration, return arithmetic, simulator agreement, and `test_story_dates.js` (publication boundaries, early exits, all three horizons, no dated feedback in the player sheet). Updated `test_story_ui.cjs` passed on desktop and 390px: horizons, buy/short/skip, stop/target, reload before/within/after walkthrough, failed commitment/progress saves, optional later context and journal. Tests use isolated storage.
- Final browser edge case passed: a 25% buy take-profit exits on 9 March 2018, before the first story event, and opens the unresolved debrief directly.
- Remaining: user playtest; broader opening/investigation wording and editorial readiness triage. No campaign integration in this patch. Dated feedback now covers all ten cases (Claude, 2026-09-10).

# Tomorrow's work — 9 September 2026 handoff

## Direction and immediate scope

The main product is the connected historical portfolio campaign in [MASTER_PLAN.md](MASTER_PLAN.md): $100,000 cash plus 1 BTC, ten chronological decisions, overlapping positions, and play until all timed trades close within a fixed historical boundary.

**Immediate user instruction: finish the story experience first.** Campaign integration is intentionally not done. Polish Nektar, let the user play it, then decide how to extend the pattern. Do not start campaign implementation, more story research or a RAG platform tomorrow without the appropriate next instruction.

Read this file, MASTER_PLAN.md, and [the Fable story handoff](research/FABLE_CAMPAIGN_NEXT.md). Despite its filename, that handoff was revised to prioritize standalone Nektar. Inspect current code before editing: the user/Fable may have made further changes. Older findings are not automatically still open.

## Already completed — do not redo

- [x] Ten standalone cases, opening scenes, sourced evidence and aftermath are present.
- [x] Nektar has investigation buttons, first instinct, selectable assumptions and a walkthrough.
- [x] Horizon-dependent calculations and unavailable-horizon controls exist. Preserve them; the remaining concern is narrative scope.
- [x] Optional exit rules, probability, contrary fact and change-my-mind fields folded into “Add detail.”
- [x] Free-text reasoning optional everywhere. Nektar still requires one or two selected assumptions.
- [x] Walkthrough reload resumes the first unanswered stop instead of revealing the ending. Explicit started/completed state added; completed legacy results remain accessible.
- [x] Walkthrough refuses to advance if saving fails; selected assumptions appear beside each event.
- [x] Journal uses the revealed name without repeating the alias; skipped position return is a dash; compact Exit column added.
- [x] Browser regression checks passed for walkthrough resume/completion, storage failure, optional reason and journal rendering (`scripts/test_story_ui.cjs`).

Latest small code patch touched `site/play.html`, `site/journal.html`, added `scripts/test_story_ui.cjs`, and updated ARCHITECTURE.md. It did not edit story wording, scope walkthroughs to horizons, or implement campaign integration.

## First: finish Nektar

- [ ] Correct the opening pitch against its evidence: $1 billion cash plus $850 million equity, not $1.85 billion plus equity; agreement/expected closing versus already paid. Keep fictional framing clearly distinguished from sourced facts.
- [ ] Merge overlapping opening questions. Retain one short scene and one neutral investment dilemma; avoid narrating the eventual lesson before the player investigates.
- [ ] Remove fixed “you'd hold for five years” wording when the ticket offers horizon choice. Remove or correct awkward “built for a 5 years hold” text. The ticket introduction was already made horizon-neutral.
- [ ] Check factual clauses in investigation answers and match them to claim IDs. Distinguish editorial valuation interpretation from reported facts.
- [ ] Repair walkthrough chronology: June 2018 is about two months after the recorded April closing, not four; do not imply the class action had ended in 2019; do not mention April 2022 termination at a March 2022 stop.
- [ ] Respect approximate dates and source availability. An event described retrospectively is not automatically contemporaneous evidence at the event date.
- [ ] Rewrite overconfident thesis verdicts. “Every subsequent data point subtracted” conflicts with the packet's recovery account. “Financing was never the problem,” money received versus financing available, and price changes attributed to one cause need evidence or narrower wording. Remove hindsight scolding such as “the packet said so.”
- [x] Scope walkthrough stops and thesis feedback to the selected horizon/actual exit. For a February 2018 one-year call, the main story ends in February 2019; 2019/2022 developments belong in explicitly optional later context. Verify one-, three- and five-year choices, plus any retained early-exit behavior.
- [x] Put explanation earlier in the debrief: results/chart -> selected-thesis check and concise horizon narrative -> optional friend check, alternative horizons, full event archive and dividends. Avoid telling the same story three times.
- [ ] Playtest Nektar on desktop and mobile, including reload halfway through. Pause for the user's feedback before expanding the pattern.

The detailed handoff has examples and reproduction steps. Historical facts still require source checking when repaired; the previous review primarily identified contradictions within local content.

## Next, after the Nektar playtest

- [ ] Extend concise investigation questions, selectable assumptions and appropriate walkthroughs to the other nine stories. This is authoring and evidence review, not merely enabling a UI flag.
- [ ] Add simple progress (“3 of 10 decided”) and a continue-to-next-undecided action. Keep this standalone progress distinct from the future campaign timeline.
- [ ] Assess whether the now-collapsed probability field should default to an unanswered forecast. Currently 50% remains the existing default and can be saved without interaction; do not imply that an untouched default is an elicited belief. If changed, update journal/calibration and preserve legacy records.
- [ ] Consider a short fictional follow-up from the same friend at each stop, grounded in stage-eligible evidence. Optional experiment, not required for completion.

Five reusable setups are a useful editorial vocabulary, not proof that the content scales. Keep setup, sector, decision tension and eventual outcome independent; avoid teaching players that a particular framing predicts a winner or loser.

## Later: campaign implementation

Detailed design prepared in [CAMPAIGN_ENGINE_PLAN.md](CAMPAIGN_ENGINE_PLAN.md): ledger, event ordering, accounting fixture, persistence, spoiler boundaries and implementation checkpoints. Proposed numerical rules remain unsettled; this does not change the immediate story-polish priority.

- [ ] Define the fixed historical interval, eligible horizons, shared ledger and event ordering from MASTER_PLAN.md.
- [ ] Add sourced BTC valuation, available cash, position accounting, dividends, borrow/collateral and forced-exit rules.
- [ ] Replace immediate future reveals with campaign-clock-controlled updates; full outcome payloads currently still load in standalone mode.
- [ ] Prototype three chronological stories with overlapping trades, an automatic closure and continuation until all trades close; then user playtest before extending to ten.
- [ ] Reconcile ending assets and a passive comparison starting with the same cash and BTC.

No future extrapolation, silently shortened horizons or forced normal exits at a data boundary. Only offer trades whose scheduled exits have complete historical coverage.

Search-led investigation is recorded separately in [RAG.md](RAG.md), deferred. A curated local search prototype could precede any runtime LLM integration.

## Running and checking

Serve the existing app: `python3 -m http.server 8765 --directory site`, then open `http://localhost:8765`.

After content edits: `python3 scripts/verify_cases.py`, then `python3 scripts/build_bundles.py`. Schema checks do not certify historical truth.

For arithmetic changes: `python3 scripts/test_returns.py` and `node scripts/test_simulate.js`. Both passed during the earlier review; the last UI-only patch did not change arithmetic.

For the story UI regression, with a server running:

```bash
PLAYWRIGHT_MODULE=/home/diablo/book11/node_modules/playwright \
CHROMIUM_PATH=/home/diablo/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell \
STOCKGAME_URL=http://127.0.0.1:8765 \
node scripts/test_story_ui.cjs
```

These are the locally available browser paths at handoff time. The test uses fresh browser storage; do not clear the user's real journal. Update the test if the intended flow changes. Do not assume a previous background server is still running.

## Working agreement

Keep edits bounded and visible. Use Sonnet workers for narrowly scoped authoring/source repair if needed, not a new broad research batch. Pause for the user's playtest after Nektar. Old quota readings in other documents are historical; never report them as current. Update this checklist with what actually changed and was verified.
