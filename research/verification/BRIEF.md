# Source verification brief (stage: verify before selection)

You verify research candidates in research/candidates-screened.json for ONE batch. Read-only web work plus writing ONE output file: research/verification/<batch>.json. Do not edit any other file. Do not run the research runner. Tools: WebFetch, WebSearch, Read, Write, Bash (only for reading/writing JSON).

Budget: at most 45 WebFetch and 15 WebSearch calls for the whole batch. Prefer the candidate's own as_of URLs; if one fails, try one alternative (SEC EDGAR filing index, issuer IR page, GlobeNewswire/BusinessWire/PRNewswire copy, or web.archive.org). Do not retry a dead host more than twice. Stop with gaps rather than exceeding the budget.

For each of the 10 candidates, check and record:
1. sources: for every source with role as_of: http status / opened, the publication date as shown on the page, whether that date is strictly before proposed_cutoff (true/false/unknown), whether the document is the ORIGINAL contemporaneous version and not a later profile, amendment, or retrospective, and whether the security identity matches (issuer, ticker, share class, exchange). Outcome-only sources: just confirm reachable and dated after the cutoff; do not summarize them.
2. material_fact: pick ONE as_of fact, confirm it verbatim against an opened source; record a short excerpt (max 40 words) and confirmed true/false/partial.
3. spoiler_scan: read neutral_title, player_question, as_of_facts and learning_tension. Flag any phrase that reveals the outcome or uses future-relative framing ("before the crash", "ahead of approval", "what turned out to be"). Flag any as_of fact whose real publication date is after the cutoff.
4. cutoff_check: is proposed_cutoff the first weekday 09:00 America/New_York after the triggering release? If the release came after market close, the next session is fine; if it came premarket the same day, the cutoff must be the following session. Note the correct cutoff if different.
5. corporate_actions: list any splits, spin-offs, distributed securities, mergers, or delisting inside the holding window that you already know of or that an opened source mentions. Mark each as known_from_source or model_memory_unverified. Do not fetch future news to build this list; only note what you know.
6. verdict: pass (all as_of sources opened, dated before cutoff, one fact confirmed, no spoiler) | repair (fixable gaps, list them) | reject (source fabricated or wrong security or fact contradicted). Add reject_reason or repairs list.

Write the output file after every 3 candidates finished, then rewrite in full at the end. Schema:
{"batch": "...", "verified_at": ISO, "budget_used": {"fetch": n, "search": n}, "candidates": [{"id", "verdict", "sources": [...], "material_fact": {...}, "spoiler_scan": {...}, "cutoff_check": {...}, "corporate_actions": [...], "repairs": [...], "reject_reason": null|str, "notes": str}]}

Do not add stock prices or returns from memory. Do not rewrite the candidate's content. Keep each candidate's record under 250 words. Final reply to the caller: a 10-line table id | verdict | main gap. Nothing else.

## Addendum after the first Haiku pass (rejected)

The first growth-batch pass was rejected for these defects. Do not repeat them:
- Every source marked opened=true while the fetch count was smaller than the source count. Record opened=true only for a URL you actually fetched in this run; otherwise opened=false and http_status null.
- Excerpts that mention analyst consensus or "beat estimates". Earnings releases do not contain consensus. The excerpt must be copied verbatim from the fetched page; if you cannot copy verbatim, set confirmed="unverified".
- publication_before_cutoff and security_identity_match left null. Both are required true/false/unknown per source.
- Spoiler scan returned empty on records that contain phrases like "given the company later missed and cut guidance", "whose payoff took years to show up", "ultimately unsuccessful", "only became a visible headwind roughly three years later", "later cocoa-cost commentary (2024)". Scan every text field (neutral_title, player_question, learning_tension, each as_of fact) for: later, eventually, subsequently, ultimately, turned out, took years, would go on to, ahead of, before the, any year later than the cutoff year, and any named future event. Quote each hit.
- corporate_actions returned empty for a ticker with a reverse split and two spin-offs inside the window. Consult the cached vendor events: research/prices/<TICKER>.json has chart.result[0].events.splits and .dividends (unix timestamps). List every split event inside the window as known_from_source (vendor), and add anything else you know as model_memory_unverified.
