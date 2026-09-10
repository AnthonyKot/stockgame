# Session status — 10 September 2026

Current work and proposed next steps are in [TODO.md](../TODO.md); restart from [START_HERE.md](START_HERE.md). The [dated debrief review](DATED_DEBRIEF_REVIEW.md) supersedes broad earlier claims of factual or spoiler completeness.

- Implemented: all-ten dated debriefs; Nektar financial snapshot redesign; Market snapshot before return statistics with the last close moved into it; What changed before Financial snapshot; removal of the repeated company-summary cutoff/hold line; aligned exit controls.
- Verified in the review: validators, arithmetic, simulator agreement, 28 available horizon exits and the browser regression passed. Deployment `ee0752c` succeeded and all ten live outcome bundles matched. Later UI deployment is not established by that check.
- Open proposal: correct Target, First Solar and Sarepta's identified verdicts; add focused/independent checks; make merging atomic before deleting outputs; then pause for playtesting. Documentation updates do not execute this batch.
- Campaign and RAG work remain deferred. No current worker runs or quota availability have been established.

## Historical session notes

Everything below is retained as a dated record. Earlier “next step,” “right now,” probability-field and Nektar-only statements may be superseded. Use the current checklist rather than treating these entries as instructions. Historical quota or worker statements are not current availability evidence.

## Nektar exit-aware debrief — 10 September 2026

Implemented the user-approved bounded patch; pause for Nektar playtesting before any rollout or campaign work.

- Nektar walkthrough and selected-thesis feedback use the actual simulated exit, including stop-loss and take-profit exits. One-/three-/five-year windows retain one/two/four authored stops respectively; earlier exits include only eligible stops.
- New outcome-only `scene_check.dated_debrief` contains baseline interpretations and event-linked updates. `site/story.js` selects evidence using both occurrence and source publication dates. Date-only evidence must precede the opening-price exit; month-only dates use month end conservatively. Retrospective legal material is not eligible at its earlier occurrence date.
- Results and primary stock/SPY chart for Nektar end at the actual exit; the final chart point uses the exit open, not that day's later close. Same-date benchmark tiles and drawdown reflect that boundary. Saved legacy forecast/calibration semantics remain unchanged.
- Default order: results/chart, selected-thesis check with source links, concise exit-scoped narrative. Full friend checks, horizon notes, event archive and alternative horizons are in a closed optional later-context section. Full outcome payloads still load after commitment; this is standalone presentation scoping, not campaign time-gating or access control.
- Removed unsupported closing/legal/cash-retention clauses from three Nektar walkthrough stops. Reused existing evidence; 2019 and April 2022 wire sources reopened during this patch, but the two SEC source URLs could not be reopened. This is not a complete source re-verification or readiness certification.
- Verified: all ten cases (`verify_cases.py`), builder regeneration, return arithmetic, simulator agreement, and `test_story_dates.js` (publication boundaries, early exits, all three horizons, no dated feedback in the player sheet). Updated `test_story_ui.cjs` passed on desktop and 390px: horizons, buy/short/skip, stop/target, reload before/within/after walkthrough, failed commitment/progress saves, optional later context and journal. Tests use isolated storage.
- Remaining: user playtest; broader opening/investigation wording and editorial readiness triage. No campaign integration in this patch. (Other nine stories got dated feedback later the same day, see below.)

# Status: ten-case MVP running locally; tightening pass in progress (2026-09-09, ~21:45 UTC)

> Superseded product priority (9 September 2026): [MASTER_PLAN.md](../MASTER_PLAN.md) defines the main game as one chronological portfolio campaign, with a fixed historical end date and play continuing until all timed trades close. This file retains earlier work, prompts or recommendations; conflicting standalone-quiz priorities and immediate future reveals do not govern campaign development. Check current code before repeating earlier tasks.

Read README.md, then ARCHITECTURE.md (what exists and how it connects). This file is only the current state and the next step. History of how the ten were chosen: research/SELECTION.md. Codex's review and proposals: research/FABLE5_NEXT_STEP.md; Codex's restart note: research/START_HERE.md.

## Published (2026-09-09, 20:10 UTC)

Repository https://github.com/AnthonyKot/stockgame (public), site live at https://anthonykot.github.io/stockgame/ via the Pages workflow. Journal and progress live in each visitor's browser only. A Feedback link in the top bar opens a new GitHub issue.

## What is true right now

- Ten cases are playable at http://localhost:8765/index.html (serve `site/` with `python3 -m http.server 8765`). All ten pass `scripts/verify_cases.py`; `scripts/test_returns.py` passes.
- Data flow and conventions are in ARCHITECTURE.md. Repo and live site: see Published above.
- 2026-09-10: Codex's review found two real defects. Fixed: the walk now ends at the simulated exit when a stop or target fired (was the anniversary). Also done the same day: Codex's `dated_debrief` (built for Nektar) rolled out to the other nine cases by nine Sonnet writers under cases/DATED_DEBRIEF_BRIEF.md; merged with scripts/merge_dated_debrief.py, checked by scripts/test_dated_debrief.js. The selector now limits updates by cited event/publication dates; the later review found content and verdict gaps that this mechanism does not detect.
- Done tonight against Codex's review: SPY benchmark on a total-return basis with the stock; commit saves and reads back before any reveal, failure shows an error and reveals nothing; masked source excerpts visible before commit; sector evidence collapsed by default; fixed "Decide" button on narrow screens; session-interval readout removed; derived valuation tiles (market cap, net cash, EV, EV/revenue; banks market cap only); rules in a side panel; per-case Brier score removed; other-horizon reveal; legend toggles and relative-to-SPY chart view.
- Kept on purpose despite the trim list: size chooser (user asked for it to be highlighted), probability question (unscored, defaulted), one shared renderer for all ten instead of a three-case pilot.

## Scenes (2026-09-09 late)

Every case opens with a scene from cases/scenes.json (five setup types, per Codex's proposal, combined with the real-headline strip). The debrief checks each scene claim against the aftermath record. Checks written for all 10.

## Horizon choice, stop loss, take profit (2026-09-09 night)

The player now picks 1, 3 or 5 years at the ticket (case default preselected; horizons past the cached data disabled) and optional stop loss / take profit levels. Results are simulated client-side by site/sim.js from outcome.sim under the same contract; the debrief shows the exit reason, the plain-hold comparison, and the chosen horizon's path. Legacy journal entries without horizon_years use the case horizon.

## Investigation layer rolled out to all ten (2026-09-09, ~21:40 UTC)

Every case now has three sourced investigation questions (label per setup), five selectable assumptions with evidence/meaning/unknown verdicts, and a 4 to 5 stop walk with stage-safe text, all in cases/scenes.json. Leak scan clean across sheet.json and walk stops. Easy UX done: index progress + continue button, folded optional ticket fields, debrief order (thesis, friend, record, then details), journal exit column. Next: user plays; then MASTER_PLAN.md campaign per Codex's implementation plan.

## Nektar story fixes against research/FABLE_CAMPAIGN_NEXT.md (2026-09-09, ~21:20 UTC)

Done: (1) walk resume with started/complete/skipped flags and a save check (Codex's fix, kept), plus stops limited to the chosen holding period; (2) pitch rewritten to the agreed-but-pending deal terms, claims aligned to the spoken clauses, friend's inference marked as inference; (3) walk stage text corrected (two months after closing; class action unresolved in 2019; March 2022 stop no longer leaks April; separate April 2022 stop; legal event dated to the month); (4) thesis verdicts rewritten as evidence / meaning for the assumption / unknown, with a 'your trade closed on' line; scene questions no longer state a horizon; the case card no longer repeats the question when a scene exists; the scene is labelled fiction. Codex is writing the campaign implementation plan in parallel; no campaign code here. Pause for the user to play Nektar.

## Investigation prototype on Nektar (2026-09-09 night)

Codex's four ideas prototyped on clinical-nktr-2018 only, generic code, data in cases/scenes.json: (1) 'What would you ask your friend?' three sourced answer cards; (2) first reaction (interested / unconvinced / against) before the decision; (3) 'My decision depends on…' one or two selectable assumptions replace the required reason, checked one by one in the debrief; (4) after commit, 'Walk through what happened' in three stops (June 2018 data, June 2019 data, March 2022 Phase 3 miss) with strengthens / weakens / unresolved at each, identity hidden until the end, or 'Show the result'. Other nine cases keep the plain flow. To extend: author the four fields for a case in scenes.json and rebuild.

## Aftermath

All ten cases/<id>/aftermath.json written (Sonnet workers, 9 to 12 dated sourced events each plus horizon notes), merged into outcome.json, rendered in the debrief with numbered markers. Leak check passed: no ticker, issuer name, aftermath or debrief_check text in any sheet.json. Nothing running.

## Next step

1. User plays a few cases with the aftermath timeline and says what reads well and what does not.
2. Editorial triage of each case's `repairs_needed` (evidence.json): mark blocking vs optional; only then consider a readiness gate in the builder.
3. Friends' feedback on the live site; then editorial triage (Codex's finding 3).

## Open questions for the user

- Keep the probability question at all, or drop it now that it is unscored per case?
- Calibration table in the journal: keep at five decisions with "too few to read" guards, or hide until more cases exist?

## Nektar financial snapshot presentation — 10 September 2026

- Added an authored `financial_snapshot.presentation` block for Nektar, matched to source metric labels rather than post-builder positions. Other cases retain their existing layout.
- Replaced crowded tiles with performance rows, a separate net-cash section and a valuation panel. Reporting periods and comparable priors stay visible. One-time revenue/cash-payment caveats are visible alongside the affected values; the non-comparable cash-only prior is explained and moved into details.
- Definitions, source/publication metadata, valuation formulas and full history remain expandable. Existing figures and calculations are preserved; the headline revenue multiple is rounded to one decimal with its inputs available below.
- Verified all ten case schemas and rebuilt bundles. Browser check at 1280px and 390px passed: five correctly mapped rows, no horizontal overflow or page errors, keyboard opening of the net-cash details. Existing journal data was not touched.
