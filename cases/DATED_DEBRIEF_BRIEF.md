# Dated debrief brief (exit-scoped thesis feedback, written from existing outcome material)

You convert one case's full-record thesis feedback into dated, event-linked feedback so that a player who exits after one year reads only what was knowable by then. The renderer (`site/story.js`, `STORY.atExit`) shows the `baseline` texts, then applies each `update` whose events all occurred AND were published before the player's exit date, in date order; a later check or narrative for the same key replaces the earlier one.

Inputs (read only these; no web access, no new facts):
- `cases/scenes.json` → `scenes[<candidate_id>]`: `assumptions` (five, each with id, text, side), the current flat `thesis_check` (one verdict string per assumption, written against the full record), `walkthrough` (the stops), `debrief_check`.
- `cases/<candidate_id>/aftermath.json`: `events` with `id`, `date` (day or month precision), `headline`, `detail`, `source.published`.
- `cases/<candidate_id>/player.json` for the situation at the cutoff.
- Exemplar: `scenes["clinical-nktr-2018"].dated_debrief` in `cases/scenes.json`. Match its shape and register exactly.

Output: write ONLY `cases/<candidate_id>/dated_debrief.json`:

```json
{
  "candidate_id": "...",
  "baseline": {
    "narrative": "1-2 sentences for a player whose window ended before the first eligible event.",
    "checks": {"a1": "...", "a2": "...", "a3": "...", "a4": "...", "a5": "..."}
  },
  "updates": [
    {"event_ids": ["e2"], "narrative": "optional, the running story as of this date", "checks": {"a1": "..."}}
  ]
}
```

Rules:
1. No new facts. Every clause must be supported by an aftermath event's headline, detail or source_quote, or by the existing thesis_check text. If the existing verdict claims something the events do not show, drop the claim.
2. Baseline checks: one per assumption, all five ids. Status is Unresolved (for a "wait/skip" style assumption, the Nektar a4 pattern: consistent with uncertainty, this outcome alone cannot tell us whether waiting was better). Say in one sentence why the starting record cannot settle it.
3. Updates: 4 to 8, in date order, one or two event_ids each (prefer one). An update unlocks only when every cited event's date AND its source's published date are before the exit, so do not pair an early event with a late-published one. Include at least one update inside the first year after the cutoff if any event falls there, so a one-year player gets feedback.
4. A check text starts with a status word: Supported / Partly supported / Mixed / Weakened / Not supported / Unresolved, optionally qualified ("Not supported in the tested setting."). Then one sentence on what the event showed, then one sentence on what it does not settle. At most 45 words. It REPLACES the previous check for that assumption, so it must stand alone as the state at that date; a few words may recall earlier updates ("after the earlier decline").
5. Narrative (optional per update, at most 45 words): the running story as of that date, replacing the previous narrative. Write one whenever the picture changes. Never mention anything later than the cited event.
6. Neutral register. No hindsight scolding, no "the stock fell because", no verdict on the player's decision. Use "this record does not establish", "cannot tell us", "does not answer".
7. For assumptions with side "bear", the status is about the assumption as stated, not about the trade.
8. Wording is shown only after the reveal, but keep the exemplar's generic style (the randomized trial, the partner, the product) and use names only as they appear in aftermath headlines.
9. Only assumptions the event actually bears on get a check in that update; leave the others out.

Final reply: three lines: candidate id, number of updates, number of events cited. Nothing else.

## Review amendments — 10 September 2026

These are authoring/review requirements following [the rollout review](../research/DATED_DEBRIEF_REVIEW.md). Existing blocks have not yet all been corrected to meet them. The merge validator does not enforce semantic support.

- Keep the original assumption's proposition, population and horizon fixed. Enactment is not durability; installed capacity is not utilization; a permitted patient group is not an efficacy endpoint.
- Separate observed developments from interpretation. Later guidance revisions cannot establish an earlier management motive. A return cannot establish that a wait decision lacked sufficient evidence.
- Describe financing proceeds and their uses separately; refinancing old debt is not equivalent to funding new development.
- For clinical/regulatory events, distinguish surrogate endpoints, functional outcomes, approval pathway, safety and patient population. Do not broaden a subgroup verdict without explicitly explaining the evidence boundary.
- Check relative chronology against actual dates. When a replacement recalls prior events, cite the needed events and verify that all dependencies are eligible; do not import later clauses from a flat full-record thesis check.
- Choose the status only after checking the evidence against the exact assumption. If evidence bears only on part of it, say which part remains unresolved.
- Human review must examine each replacement as a standalone statement at its unlock date. Schema checks, word limits and an applicable update do not certify factual accuracy.

Proposed pipeline improvement, not current behavior: retain writer outputs until the entire batch is validated and the merged file is safely written; only then archive or delete them. See TODO before running a new merge batch.
