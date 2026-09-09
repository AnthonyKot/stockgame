# Fable 5 handoff — tighten the existing ten-quiz MVP

> Superseded product priority (9 September 2026): [MASTER_PLAN.md](../MASTER_PLAN.md) defines the main game as one chronological portfolio campaign, with a fixed historical end date and play continuing until all timed trades close. This file retains earlier work, prompts or recommendations; conflicting standalone-quiz priorities and immediate future reveals do not govern campaign development. Check current code before repeating earlier tasks.

Work in `/home/diablo/stockgame`. You are continuing an existing application, not starting over. The user wants a fun historical investing game: read the evidence available at a date, choose buy/skip/short for a fixed 1-, 3- or 5-year horizon, then see the outcome and understand the story. Ten quizzes are already implemented. Do not collect more stories or change the technology stack in this stage.

Read `site/index.html`, `site/play.html`, `site/journal.html`, `site/app.js`, `site/style.css`, `scripts/build_bundles.py`, `scripts/verify_cases.py`, `research/SELECTION.md`, and the three representative case bundles below. Consult CASE_FORMAT.md and FRAMEWORK.md only as background; the simpler scope in this handoff supersedes their optional features. `research/MVP_PROMPT.md` is the older initial-build prompt, not the current state of work. Inspect repository instructions if present.

## Current evidence, checked 9 September 2026

- Ten case cards and ten player/evidence bundles exist. Five biotech/pharma and five non-IT businesses; keep that sector variety and the 1/3/5-year horizons.
- The deterministic `python3 scripts/verify_cases.py` check passes for all ten. It checks structure and some text/date patterns, not financial truth or complete point-in-time eligibility.
- Browser review of the first case (First Solar): load → evidence drawer → buy → reveal → reload → journal works without page errors. No reveal/outcome request occurred before commitment in masked mode.
- The initial First Solar reading area contains about 1,402 visible words. At 390×844 the decision ticket starts at y≈10,147px. It is reachable but far too distant from the decision context.
- The masked evidence drawer repeats the claim and a source label; original excerpts are only supplied by reveal.json after commitment. The player cannot inspect a sanitized supporting excerpt before deciding.
- Eight cases have an explicitly missing market-cap/EV/valuation headline. They may convey a business story without enough evidence to judge its price. Use sector-appropriate valuation rather than the same multiple everywhere.
- Every case retains a repair list; `build_bundles.py` nevertheless sets `sheet_ready` whenever player.json exists. Some list items are genuine repairs, others are documentation or optional improvements. Triage them rather than treating every string as a blocker.
- `build_bundles.py` includes dividends in stock-long return, but calculates SPY from opening prices alone. For the JPM five-year case, current cached data give about 82.21% SPY price return versus 93.70% including cash dividends before costs. Compare equivalent return conventions and explain any cost difference.
- When Storage.prototype.setItem throws QuotaExceededError, submission still fetches and reveals the outcome and leaves no saved decision. Reproduced in a fresh browser context. `SG.safe` swallows storage failures and `upsertCommit` returns no success status.
- Debrief headings currently provide the path and sources, but no authored account of the developments during the holding period. The game shows numbers more effectively than it explains the story.
- The journal labels calibration after as few as five revealed decisions. These ten curated cases do not support confident calibration judgments.

This was a representative desktop/mobile review, not an exhaustive audit of every case or of assistive-technology support.

## Goal and scope

Make one short, trustworthy, enjoyable loop using existing code and data. Keep the ten cases. First refine three representative cases: First Solar (`growth-007`, 1y), Target (`growth-004`, 3y), and Madrigal (`clinical-mdgl-2018`, 5y). Once the user approves the pattern, apply it to the remaining seven.

Do not add accounts, dashboards, a backend solely for hiding static files, more instruments, leaderboards, portfolio rebalancing, a large data vendor integration, or another framework. Static hosting and local storage are sufficient for this private MVP; clearly state the limits of static outcome-file separation without turning the player interface into implementation documentation.

## Stage 1: fix correctness and recovery

1. Put stock and SPY outcomes on equivalent dividend/return conventions, using identical holding timestamps. Prefer fixed-share holdings with dividends accumulated as cash for both, if that matches existing logic; disclose costs consistently. Update the displayed benchmark, charts where necessary, journal fields and any beat-SPY calculation. Check entry/exit inclusion, leap-day handling, dividend entitlement and applicable split adjustments. Never silently turn unknown corporate actions into an empty list.
2. Make commitment transactional from the user's perspective: save successfully before loading future/identity data. On failure, preserve the form, show a useful error and retry control, and do not reveal. Restore focus appropriately. Handle corrupt stored JSON and failed outcome fetches without losing the saved decision.
3. Distinguish blocking factual/time/price gaps from optional research. Require blocking gaps to be cleared before a case is presented as ready. Do not certify source accuracy solely because a schema checker passes.
4. Add focused regression tests for the return conventions and commit-before-reveal/storage-failure behavior. Run the existing data verifier and re-exercise the real browser journey.

## Stage 2: simplify three representative quizzes

Default reading order:

- Neutral case title, cutoff and holding horizon.
- A 40–60-word situation summary and one clear investment question.
- Four to six decision-relevant facts, including usable valuation or a clearly explained limitation. Keep reported facts, guidance and editorial interpretation distinct.
- One historical chart, with price, operating history and source detail available on demand.
- The most material catalyst and risk within the stated horizon.
- Buy / Skip / Short and one short optional rationale.

Make a decision possible after a roughly 200–300-word briefing. Collapse full financial history, detailed sector evidence, methodology and optional arguments. Replace generic nested-JSON rendering with concise labeled fields for the important sector information. Avoid generic “item” labels and machine identifiers in prose.

For this MVP, use one fixed illustrative position size (e.g. 10% of the virtual account) and keep the existing execution/short-cost assumptions visible in a compact rules drawer. Remove the size chooser, required essay, two additional thesis textareas, numerical probability question and journal calibration judgments from the default flow. Preserve existing saved decisions and do not silently reinterpret their sizes or probabilities; mark older records as legacy where needed.

Keep the 1/3/5-year comparison after reveal, collapsed by default: this directly supports the user's intended learning. Remove the unrelated 5/21/63/126-session readout from the main debrief. Keep a simple journal for revisiting decisions. Do not build a replacement analytics dashboard.

On mobile, show a persistent compact decision action that opens or jumps to an accessible ticket. The player must not have to scroll through the entire evidence packet to act. Test keyboard focus, drawer closing/return focus, reduced motion and 390px width.

Before commitment, evidence buttons should show a short sanitized excerpt with date and source type. Keep identifying URLs and names out of masked pre-decision payloads. Do not hide contrary evidence just because it complicates the story.

## Stage 3: give each representative case an actual debrief

Create a separate outcome-side narrative with:

- What the chosen action returned over the committed horizon, versus cash and the consistent benchmark.
- Two or three dated, sourced developments during the holding period.
- Which starting assumptions were supported or contradicted, with uncertainty stated.
- One transferable question, such as whether an attractive business was already expensive or whether financing diluted a clinical success.

Do not claim that a particular announcement caused a price move unless supported. Do not turn one realized outcome into proof that a reasonable starting thesis was foolish. No new outcome text can enter the pre-decision sheet or a pre-decision network response.

## Working style and checkpoints

The user wants pauses and wants to protect quota. Use inexpensive Sonnet workers for narrowly scoped source repairs if available; Fable should coordinate, implement and review. Save outputs incrementally with visible progress logs. Avoid sending every worker the whole repository. Do not purchase data or enable paid overages.

Pause after Stage 1 with a brief change/test report and remaining quota if accessible. Wait for the user before Stage 2. Pause again once the three representative quizzes demonstrate the simplified design and debrief. The user will play those before approving rollout to the other seven. Do not re-research all 30 candidates.

## Success criteria

- Consistent stock/benchmark returns with meaningful arithmetic tests.
- No outcome reveal when saving fails; successful decisions survive reload.
- A short first read, with source evidence available before choosing.
- A usable decision control within reach on desktop and mobile.
- Three refined quizzes whose reveals explain the business developments as well as showing returns.
- Clear separation of verified facts, assumptions and remaining optional gaps.
- Existing case diversity and the user's 1/3/5-year horizons preserved.

Finish each checkpoint with what changed, what was tested, remaining limitations, and the exact next action for the user. Do not claim all ten are polished when only three have been refined.
