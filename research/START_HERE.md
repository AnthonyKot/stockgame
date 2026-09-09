# Restart handoff — 9 September 2026

## Latest immediate task

Read [TODO.md](../TODO.md) for the current checklist and completed fixes. The user explicitly wants to finish the standalone story experience before connecting the campaign. Polish Nektar and pause for playtesting; do not treat the earlier campaign-prototype instruction below as the immediate task.

## Latest user-approved priority

Read [MASTER_PLAN.md](../MASTER_PLAN.md) first. The MAIN game is a connected historical campaign with $100,000 cash plus 1 BTC, ten chronological decisions, overlapping 5/10/20% long/short positions, and automatic 1/3/5-year exits. Keep advancing until every timed trade closes. Use a fixed historical end date; never offer a holding period that cannot complete within verified data. Do not reveal future outcomes while earlier scenes remain.

This overrides the older three-independent-quizzes refinement priority below. Reuse current app/content work; next prototype is three chronological scenes sharing a portfolio, with overlap, a closure and an eventual final report. Search/RAG and role-play refinements support this loop. This update records direction, not completed campaign code. Preserve user pause checkpoints.


Work in `/home/diablo/stockgame`. An existing ten-quiz historical investing MVP is implemented. Continue it; do not restart research or rebuild the app.

## Read in this order

1. `README.md` for running and checking the app.
2. `ARCHITECTURE.md` for the pipeline, source data, generated bundles and site.
3. `research/SELECTION.md` for the selected ten cases.
4. `research/FABLE5_NEXT_STEP.md` for the previous review and proposed simplification.
5. Inspect the actual code and relevant case data before choosing work.

`research/PAUSED.md` contains useful history but mixes earlier partial completion with later completion notes. Its quota figures are historical, not current. `research/MVP_PROMPT.md` and `CLAUDE_RESEARCH_TASK.md` are older task prompts.

## Important freshness caveat

The latest architecture document describes derived valuation and aftermath timelines that were absent from the earlier review in `FABLE5_NEXT_STEP.md`. Re-check those findings against current code and data; do not duplicate completed work. That handoff is a proposed next stage, not evidence that its changes have been implemented or that the user has approved every recommendation.

## User intent and working preferences

- Fun buy/skip/short decisions using only evidence available at a historical cutoff; retain 1-, 3- and 5-year horizons.
- Keep the ten selected stories and sector variety, including biotech successes, failures and mixed cases. Avoid obvious outcomes and an IT-heavy set.
- Prioritize a usable briefing and explanatory reveal over more content or features.
- Use Claude Code Sonnet for bounded research tasks when needed; subscription access was available previously, but availability and quota must be checked anew. Do not purchase data or enable overages.
- Pause at agreed checkpoints and let the user review. Do not start an unattended research marathon. Never report old quota readings as current.
- The previous review proposed correctness/recovery fixes, then simplifying First Solar (1y), Target (3y) and Madrigal (5y), then user playtesting before extending the format to the other seven. Confirm the current task from the new session's user message.

## Suggested opening message for a new session

> Continue stockgame. Read MASTER_PLAN.md and research/START_HERE.md, then inspect current implementation. The priority is the connected portfolio campaign within a fixed historical boundary. Reuse the existing ten cases and UX work. Give me current status and the smallest campaign prototype step before starting a long batch; preserve agreed pause checkpoints.
