# Restart handoff — 10 September 2026

Work in `/home/diablo/stockgame`. Continue the existing ten-case app; do not restart research or rebuild the stack.

## Immediate scope

Finish and refine the standalone story experience through user playtesting. Nektar's exit-aware debrief is implemented; dated feedback has since been authored for all ten cases. The latest review found editorial and verification gaps in that rollout. The user authorized four engineering points: payload/temporal checks, flexible verdict tests, recoverable dated merging and integration. Current results and ownership are in [SESSION_PROGRESS.md](SESSION_PROGRESS.md); inspect that log before repeating work.

Read in this order:

1. [TODO.md](../TODO.md) and [NEXT_SESSION_PLAN.md](NEXT_SESSION_PLAN.md): current checklist and the sequenced two-hour plan.
2. [Dated debrief review](DATED_DEBRIEF_REVIEW.md): evidence, limitations and concrete repairs.
3. [ARCHITECTURE.md](../ARCHITECTURE.md): current pipeline and UI behavior.
4. [README.md](../README.md): running the app.
5. [MASTER_PLAN.md](../MASTER_PLAN.md): long-term product authority.
6. Inspect the current code and case data before editing; concurrent sessions have changed and committed files during this work.

## Current state

- Ten standalone stories have investigations, selectable assumptions, walkthroughs and dated debriefs. The selector uses the actual exit and both event/publication dates. Full future payloads still load after commitment.
- Nektar's financial snapshot now groups business performance, cash position and valuation, with key caveats visible and detail expandable.
- The case page places Market snapshot (including last close) before Where the stock stands, then What changed before Financial snapshot. The repeated company-summary cutoff/holding line is removed. Exit-level controls are aligned.
- Structural, arithmetic and browser checks passed in the latest review; they do not certify every authored statement. See the review for precise coverage and the dated deployment observation.

## Next checkpoint

The engineering safeguards are implemented locally. See [SESSION_PROGRESS.md](SESSION_PROGRESS.md) for verification and remaining editorial limitations. Pause for user playtesting; source review and presentation multi-file recovery remain separate follow-ups. Do not start an unattended rollout, research batch or campaign implementation from this handoff alone.

## Campaign direction — deferred

The main product remains one chronological portfolio beginning with $100,000 cash plus 1 BTC, ten decisions, overlapping 5/10/20% positions and automatic 1/3/5-year exits within a verified fixed historical boundary. Play continues until all timed trades close. [CAMPAIGN_ENGINE_PLAN.md](../CAMPAIGN_ENGINE_PLAN.md) is design work, not an implemented ledger. [RAG.md](../RAG.md) remains deferred.

## Historical documents and working preferences

[SELECTION.md](SELECTION.md) records the ten selected cases. [FABLE5_NEXT_STEP.md](FABLE5_NEXT_STEP.md) and [FABLE_CAMPAIGN_NEXT.md](FABLE_CAMPAIGN_NEXT.md) are earlier reviews; their findings are not automatically still open. [PAUSED.md](PAUSED.md) preserves chronological history, including outdated quota readings and superseded tasks.

Keep the selected stories and sector diversity. Prefer a readable briefing and explanatory debrief over more features. Preserve existing journal data and agreed playtest pauses. If new research becomes necessary, use bounded tasks, check availability/quota anew, and do not buy data or enable overages.
