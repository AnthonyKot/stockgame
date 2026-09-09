# Aftermath brief (debrief-only research, written AFTER the case is decided)

You research what happened to ONE or TWO companies after a case's cutoff, for the game's debrief. This is outcome material: it is never shown before the player commits, so you may and must use sources published after the cutoff. Read research/selected.json for your case's issuer, ticker, cutoff and horizon; read cases/<candidate_id>/player.json for the situation at the cutoff so your timeline connects to what the player saw.

Tools: Read, Write, WebFetch, WebSearch, Bash (read-only). Budget per case: 25 WebFetch, 10 WebSearch. Write ONLY cases/<candidate_id>/aftermath.json.

## What to produce

A dated timeline of the material public events from the cutoff to the later of (a) the case horizon, (b) five years, but not beyond 2026-09-09. Then short horizon notes.

Rules:
1. Every event has a date, a neutral headline of at most 25 words, a kind, and a source you opened (url, title, publisher, published date). Prefer primary sources: SEC 8-K/10-K/10-Q, issuer press releases, FDA/EMA notices, court filings. A news article is acceptable for market-wide context or when no primary source is reachable; say so in `opened_note`.
2. 6 to 12 events per case, spread across the horizon, not clustered at the end. Include the events that a reader of the pre-cutoff packet would have been waiting for (the catalysts listed in player.json), whether they happened as guided, slipped, or failed.
3. Causation is labelled. Write "the company attributed the decline in X to Y" or "management said", never "the stock fell because". If a source explicitly links a price move to an event, quote it and mark the event `attribution: "source"`; otherwise `attribution: "none"`.
4. No stock prices or returns from memory. The game computes returns itself. You may quote a source's stated move only inside `source_quote`, at most 30 words.
5. Macro context at most 3 events, each with the connection to this business stated (e.g. 2020 pandemic demand, 2022 rate rises for unprofitable biotech).
6. Horizon notes: for each horizon in {1, 3, 5} whose anniversary is on or before 2026-09-09, 2 to 4 sentences describing what the record shows over that span, citing event ids in brackets [e3]. Neutral tone. End each with one sentence on what the pre-cutoff packet did and did not contain that mattered, labelled `interpretation`.
7. Kinds: earnings | guidance | clinical | regulatory | deal | financing | management | legal | product | macro | corporate_action | other.

## Schema

```json
{
  "candidate_id": "...",
  "cutoff": "...",
  "coverage_end": "YYYY-MM-DD",
  "events": [ {"id": "e1", "date": "YYYY-MM-DD", "kind": "clinical", "headline": "...", "detail": "one or two sentences, facts only", "attribution": "none" | "source" | "company", "source_quote": null | "...", "source": {"title": "...", "url": "...", "publisher": "...", "published": "YYYY-MM-DD"}, "opened": true, "opened_note": null | "..."} ],
  "horizon_notes": {"1": "...", "3": "...", "5": "..."},
  "attribution_caveat": "Price moves have many causes; the events here are what was public, not a proof of why the price moved.",
  "gaps": ["..."],
  "search_log": [ {"query_or_url": "...", "result": "opened | 403 | timeout | not_found"} ]
}
```

Save after the first complete draft. Final reply: per case, three lines: id, number of events, number opened. Nothing else.
