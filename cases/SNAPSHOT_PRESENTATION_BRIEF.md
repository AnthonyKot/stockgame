# Snapshot presentation brief (interpretation beside the number, written from the case's own packet)

You author the `financial_snapshot.presentation` block for ONE case. The page renders it as rows: label, period, the number, the prior, and one short context line that says what the number does and does not mean. Definitions, sources and formulas stay available under a fold. Exemplar: `cases/clinical-nktr-2018/player.json` → `financial_snapshot.presentation`, rendered by `site/play.html` (`if (fs.presentation)`).

Inputs (read only these; no web access, no new facts):
- `cases/<candidate_id>/player.json`: `financial_snapshot.headline` (the tiles: `label`, `value`, `unit`, `period`, `prior`, `definition`, `status`), `financial_snapshot.history`, `what_changed`, `business`, `known_gaps`.
- `site/data/<opaque_id>/sheet.json`: the derived `valuation` object (market cap, net cash, enterprise value, `annual_revenue_musd`, `ev_to_revenue`, `inputs`, `caveats`). The prompt gives you the opaque id.
- The exemplar above.

Output: write ONLY `cases/<candidate_id>/presentation.json`:

```json
{
  "candidate_id": "...",
  "intro": "one sentence telling the reader how to read this block",
  "groups": [ {"title": "Business performance", "metrics": [0, 2, 1]}, {"title": "Cash position", "metrics": [3]} ],
  "metrics": [
    {"label": "Revenue", "metric": "<exact headline label>", "context": "...", "display_value": null, "prior_comparable": true}
  ],
  "valuation_context": "...",
  "valuation_mode": "revenue | pipeline | bank"
}
```

Rules:
1. `metric` must equal a headline tile's `label` EXACTLY (copy it). A tile that is a valuation placeholder (enterprise value, EV/revenue, market cap) is NOT listed: the valuation panel covers it. List every other tile once; 4 to 6 metrics.
2. `label` is a short reader-facing name (Revenue, Operating margin, Free cash flow, Net debt, Cash, Runway...). Keep the unit conversion to the page; do not put numbers in `label`.
3. `context` is at most 35 words and must come from the tile's own definition, the history, or `what_changed`. It says what the number means for this business and what it does not establish. Flag one-time items, mixed periods (quarter vs year), and pre-cutoff staleness. No forecasts, no valuation opinions, no words like cheap/expensive.
4. `display_value` is null unless the raw number would mislead (near-zero, or a percentage stored as a fraction); then give the display string exactly as the reader should see it. `prior_comparable` is false only when the prior is a different measure; explain why in `context`.
5. Groups: 2 or 3, titled for this business (Business performance / Cash position / Balance sheet / Funding runway / Concentration). Order metrics inside a group from most to least important for the decision.
6. `valuation_context`: at most 45 words. State which revenue the multiple uses (read `valuation.annual_revenue_musd` and its `period` in `inputs`; it is often the prior fiscal year, not the tile's), that share count and cash dates predate the price, and any caveat in `valuation.caveats`. For a bank or a pre-revenue biotech say what the panel does not mean.
7. `valuation_mode`: `revenue` (default) keeps the EV/revenue multiple; `pipeline` (pre-revenue or royalty biotech valued on its programmes) hides the multiple under the fold and shows net cash as a share of market cap; `bank` is market cap only. Pick by what the price actually rests on.
8. Neutral register, no hindsight; everything shown here is pre-decision material and must not hint at the outcome.

The merger and case verifier reject invalid valuation_mode values. An omitted writer mode retains the existing destination mode; when neither supplies one, the UI defaults to revenue.

Final reply: three lines: candidate id, number of metrics, number of groups. Nothing else.
