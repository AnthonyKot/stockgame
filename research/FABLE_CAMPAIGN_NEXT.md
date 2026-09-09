# Fable handoff: finish the Nektar story experience

Review date: 9 September 2026. Read `MASTER_PLAN.md` first. This handoff provides instructions for the next implementation session; this review did not modify app code or case data. Inspect current files before editing because another session may be working on them.

## Latest user steering

The user clarified after this review: “We didn’t connect everything together. Let’s finish on story level a bit.” The immediate task is to polish and test Nektar as a standalone story. Missing campaign integration is expected, not a defect to fix in this batch. The campaign remains the master product direction, but its implementation is deferred here.

## Direction

Five opening setups fitting ten cases shows template reuse, not proof of scalable content quality. Treat setup as the way an opportunity reaches the investor, independent of sector, investment question and eventual outcome. Do not make friend pitches synonymous with biotech or bad-news headlines synonymous with buying a recovery. Do not assign a setup using future returns.

The main product is one chronological campaign starting with $100,000 cash plus 1 BTC, with overlapping positions and a fixed historical boundary. Role-play supports that loop. Finish one coherent Nektar story before extending the pattern. Do not implement the campaign ledger in this batch.

## What exists and what was checked

- `site/play.html` now opens with the scene, supports Nektar's three sourced question buttons, first instinct, selectable assumptions, chosen horizon, optional stop/target, and a three-stop walkthrough.
- Source excerpts distinguish the company and partner more clearly than the earlier version. Preserve this improvement.
- `site/sim.js` calculates one standalone trade; it still uses a starting equity of $100,000 per simulation. No shared campaign ledger or Bitcoin holding was found in the reviewed flow.
- `python3 scripts/test_returns.py` and `node scripts/test_simulate.js` passed. These establish the tested arithmetic and builder/simulator agreement, not campaign correctness or historical factual accuracy.
- Browser coverage: ten-card entry page -> Nektar -> source drawer -> buy 10% with an assumption -> walkthrough -> first reflection -> reload. Also inspected 390px mobile layout. No page errors or pre-commit outcome requests observed. The initial briefing had roughly 1,615 visible words. The mobile ticket starts about 8,047px down, with a fixed Decide shortcut.
- No independent web-source re-verification was performed in this review. Content contradictions below are established against the local packet and aftermath, not a fresh certification of original sources.

## Priority 1: repair progression and Nektar content

### High: reload skips unfinished walkthrough

Reproduction: commit to Nektar, start walkthrough, answer Weakens at stop 1, arrive at stop 2, reload. The page reveals the complete February 2023 result and identity.

Cause: `showDebrief()` checks whether `entry.walkthrough` exists, rather than whether every stop is complete. `walkPending` uses the same insufficient distinction. A single saved reflection makes an unfinished walk appear complete.

Use explicit progression state with a cursor and completion status. A partial reflection list is not completion. Resume exactly where the player stopped, with no future reveal. Keep selected assumptions and saved reflections intact. Test reload before the first reflection, midway, and after completion, including failed persistence.

In campaign mode, the campaign clock must govern unlocks. `outcome.json` currently loads the complete future immediately after commitment; merely fixing DOM visibility is insufficient. Build dated slices and avoid prefetching future narrative, prices or results in the normal player journey. Document static-file access limits honestly.

### High: opening pitch contradicts supporting evidence

`cases/scenes.json` still says "$1.85 billion up front" with equity "on top" and says it was already paid. The packet says $1 billion cash plus an $850 million equity investment, with closing still pending at the cutoff.

Suggested fictional pitch, subject to checking the existing claim mapping:

> A major pharma has agreed to put $1 billion into the partnership and buy $850 million of stock at a premium. They're backing this cancer treatment while it's still in early trials. That makes me interested—what do you think?

Clearly identify role-play as fictional framing. Keep factual clauses sourced and distinguish the friend's inference from reported terms. The current claims list also includes material not actually spoken in the pitch; align the spoken clauses, supporting questions and later checks explicitly rather than claiming sentence-level coverage merely because IDs exist.

### High: walkthrough text crosses its own timestamp

- The 2 June 2018 stop says "Four months after the deal closed"; the local timeline says it closed 3 April 2018. Correct the interval or omit it.
- The 1 June 2019 stop says the class action "came and went"; the local timeline describes a dismissal affirmed in 2022. Do not suggest the later resolution was already known.
- The 14 March 2022 stop reveals that both companies end the program a month later. Move that development to its own eligible April stop. Remove "expired worthless" and "keeps the cash" unless precisely defined and supported; they overstate the recorded facts.
- The local legal event uses an approximate October 2018 date but the UI renders an exact day. Preserve date precision and use a conservative availability boundary for any campaign update.

Every stop needs eligible source evidence and an explicit availability boundary. Check all clauses, not only the event headline/date. A later document describing an earlier event cannot automatically serve as contemporaneous reading material.

### High: thesis feedback overclaims

Examples in `thesis_check`:

- "Every subsequent data point subtracted" conflicts with the packet's account of recovering 2019 data.
- "Financing was never the problem" exceeds the evidence collected; the source describes up to $150 million of financing, not necessarily $150 million received.
- "On the June 2018 data alone" asserts price causation without sufficient support.
- A failed drug does not prove that its earlier valuation already assumed success. Keep that interpretation separate from the realized return.
- "The packet said so" turns the reveal into hindsight scolding.

Write feedback in three parts: what evidence arrived; what it supports or contradicts about the chosen assumption; what remains unknown. Scope feedback to the current clock/closed trade, not the furthest available horizon. "Insufficient evidence" is a defensible choice, not a retrospectively guaranteed winning thesis.

## Priority 2: make Nektar a coherent story

After correctness fixes, refine the existing interactions rather than adding more controls:

1. Open with one short fictional message and one neutral question. Remove the duplicated case question. Keep the date and selected holding horizon easy to find; narrative must not promise five years when the player selects one.
2. Preserve the three sourced investigation questions, but make the answers concise. The friend can express enthusiasm; explanatory answers must separate reported terms from editorial interpretation.
3. Keep first instinct optional. Let players choose one or two assumptions with optional supporting text; avoid making them complete several overlapping reasoning fields.
4. In the walkthrough, show the player's selected assumption beside the new evidence. Ask whether that specific assumption is strengthened, weakened or unresolved. A stock-price fall does not necessarily weaken a short thesis.
5. Scope stops and verdicts to the chosen holding period and actual exit. A one-year trade should not automatically walk through a 2022 event before its own closing debrief. Any later context must be an explicit, separate standalone exploration; it must not be presented as evidence for the earlier result.
6. End with the player's result and a concise check of their selected assumptions. Keep the full event archive and the generic friend-claim checks available in details, so the same story is not told three times.
7. Verify desktop and mobile: the opening scene is visible immediately, the decision is reachable, and a refresh preserves walkthrough progress.

A small optional creative enhancement: let the same fictional friend send a brief follow-up at each stop. It should add human continuity, not new facts or a lesson disguised as dialogue. Label fictional dialogue and support its factual clauses with stage-eligible evidence. Prototype this only after the existing loop reads well.

## Campaign work — deferred

No ledger, Bitcoin integration or chronological multi-case routing is requested in this story-polish batch. Follow MASTER_PLAN.md when campaign implementation resumes. Preserve a path to time-gated content, but do not require that migration to complete this standalone prototype. Full future payloads remain an acknowledged standalone architecture limitation; do not claim the walkthrough is secure against inspecting those files.

## Scene improvements that support the campaign

These are future supporting ideas, not additional requirements for this story-polish batch:

- Return to the same fictional friend when new evidence arrives. Use a short sourced update and show the player's original selected assumption beside it. Do not make the friend omniscient or consistently wrong.
- Replace the second repeated investment question with portfolio context: "Your Nektar position is still open. Available cash: ..." at the next story. This makes connectedness visible without adding more exposition.
- Ask what one assumption the player would revisit, rather than requiring multiple essays. Keep short/skip reasoning as legitimate as bullish reasoning.
- Keep broad sector/setup variation, but do not force new wrappers onto all ten before testing the campaign. Search in `RAG.md` remains deferred.

## Checkpoints and documentation

Repair the reproduced progression bug and Nektar's locally demonstrated contradictions, refine the single-story loop above, then pause for the user to play Nektar. Report changes, focused tests and remaining limitations. Wait for feedback before expanding the story pattern or beginning campaign integration.

Update `ARCHITECTURE.md` to distinguish actual implementation from plans. Its directory table still says CASE_FORMAT.md wins; correct it to MASTER_PLAN.md. Link this handoff from the restart note when beginning the implementation session. Do not claim campaign completion because ten standalone cases work or because simulation arithmetic tests pass.
