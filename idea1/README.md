# Idea 1: one portfolio through ten decisions

Product-owner assessment, 10 September 2026. Scenario, stories and acceptance criteria are in [EPIC.md](EPIC.md); the product authority is [MASTER_PLAN.md](../MASTER_PLAN.md), the engine design [CAMPAIGN_ENGINE_PLAN.md](../CAMPAIGN_ENGINE_PLAN.md). Comparison with the other two ideas: [IDEAS.md](../IDEAS.md).

## 1. In one paragraph

You start on 15 February 2018 with $100,000 and 1 Bitcoin, meet ten investment stories in the order they happened, and decide each from what was public that morning. One account carries through. A five-year buy in 2018 is still open when the 2021 stories arrive and constrains what you can afford. After the tenth decision you keep advancing until the last trade closes, then read a final report that reconciles every dollar and compares you with doing nothing.

## 2. How it is built on today's code

Reused unchanged: the ten scene packets, evidence and aftermath files, the dated debrief and its selector (`site/story.js`), the price caches, the chart code, the builder's masking, the payload checker and the CI gate.

Replaced: the per-trade simulator `site/sim.js` cannot be summed into a portfolio (it assumes a fresh account and knows its own exit). A ledger engine takes its place for campaign play; the simulator stays for the standalone cases and as a cross-check.

New: `site/campaign-engine.js` (pure ledger, positions, valuation, event application), `site/campaign-store.js` (versioned save and resume), `site/campaign.html` (portfolio strip, since-last-stop, ticket with funding constraint, advance control), `scripts/build_campaign.py` (manifest, coverage audit, dated slices instead of whole-future outcome files), `site/data/campaigns/<version>/`.

New data the repo does not have: a Bitcoin daily USD series, dividend payment dates for ten issuers through March 2026, a split audit of cached levels, a New York session calendar with holidays and early closes.

## 3. Effort

Large. Roughly 8 to 12 agent sessions over three to four weeks at the current pace, in this order:

| Milestone | Sessions | Who |
|---|---|---|
| Settle the seven open decisions, write the manifest, arithmetic and time fixtures | 1 | main session, user decides |
| Long/skip engine on synthetic data, save/resume, reconciliation | 2 to 3 | Codex (its plan) |
| Data: Bitcoin series, dividend dates, split audit, calendar | 1 | scripted fetches plus review |
| Dated slices, coverage audit, campaign screen | 2 | split: builder Codex, screen Claude |
| Three-story prototype and playtest | 0.5 plus the user's time | pause |
| Shorts: collateral, borrow, forced cover, default policy | 2 | Codex, tests first |
| Ten stories, tail after decision ten, final report | 1 to 2 | both |

Sonnet writers have little to do here; this is engine and data work.

## 4. Pros and cons

Pros
- It is the game the master plan describes: decisions with consequences for later decisions.
- Skipping and sizing finally matter, because cash is scarce and time passes.
- A real final report, with income, costs and a same-assets baseline, is something to share.
- Replay value: a different order of calls gives a different ending.

Cons
- The hardest accounting in the project: reservations, restricted proceeds, entitlement versus payment, forced covers, same-day ordering. Every rule is a place to be wrong.
- Seven policy decisions are open and none can be discovered in code.
- Outcome data remains static files; the private-MVP spoiler limit stays.
- One run spans 2018 to 2026. That is a long game for a friend with an evening.
- It inherits today's cryptic case page. A portfolio strip on top of it makes a newcomer's first screen worse, not better.

## 5. Confidence

These are judgments, not measured probabilities; the playtest is the measurement.

- **We can build it: medium.** Gate: the master plan's acceptance criteria pass as automated checks in `run_checks.sh`. Codex's engine plan is thorough and the test list is enumerable; the risk is data (Bitcoin timestamps, dividend dates, splits), where invented numbers creep in.
- **Players prefer it: low until the presentation is fixed.** Consequences are compelling on paper; nobody has felt them yet. A long run may not finish in one sitting.

Evidence that would move it: the three-story playtest. If the player talks about the earlier position while deciding the third story, the mechanic works.

## 6. Risks and unknowns

- Short policy and default handling: unresolved; block short-enabled play until decided and tested.
- Bitcoin series: none in repo; pick a documented source and convention before any fixture uses it.
- The raw Yahoo caches are back-adjusted for later splits (Nektar's 2025 one-for-fifteen shows 2018 opens near 1,292 instead of 86); the builder reverses this for display, so `market.json` levels are real. The campaign must use one convention everywhere and never show a per-share level from the raw cache. Audit every window that crosses a split.
- Session length: consider a two-story or five-story short campaign as a mode if the ten-story run proves long.
- Concurrent work: engine files are Codex's lane, screen and content Claude's; the CI gate runs on every push.

## 7. First milestone and its playtest

Nektar (Feb 2018) → Madrigal (Nov 2018) → JPMorgan (Jan 2019), long and skip only, with Bitcoin marked, at least one automatic closure, and a reconciled report at the end. The friend plays it and is asked one question: "When you decided on the bank, were you thinking about the biotech you still held?"

## 8. Kill criteria

Stop or reshape if the three-story playtest is not more engaging than three standalone cases, if the ledger cannot reconcile without inventing a settlement or price, or if the seven decisions cannot be settled in one sitting.
