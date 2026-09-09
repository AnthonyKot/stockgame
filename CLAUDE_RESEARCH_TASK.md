# Bounded research pilot for the historical investing game

Research TWO candidate cases using public primary sources and return structured JSON only. You are a research worker; do not edit files, run commands, delegate, access private accounts or purchase data. Use WebSearch and WebFetch. Budget the work: at most 12 searches and 16 page fetches total. If tools or sources are unavailable, report the blocker promptly rather than retrying indefinitely.

1. Alphabet, US Class A common stock GOOGL, proposed decision cutoff 2024-02-02 at 09:00 America/New_York, one-calendar-year holding period.
2. Merck & Co., US common stock MRK (NOT Merck KGaA), proposed decision cutoff 2019-02-04 at 09:00 America/New_York, five-calendar-year holding period.

These are proposed historical dates, not verified packet dates. Check eligible earnings and corporate disclosures preceding the cutoff. The user explicitly wants multiple time horizons. State the next regular trading session for entry and the proposed anniversary exit convention, but do not invent a stock price or return. Calendar-year horizons use the first regular-session open on or after the entry's calendar anniversary; this is a deterministic game rule, not 252/1260 trading sessions.

Read CASE_FORMAT.md for the eight-block presentation contract if useful. For this pilot, return research drafts with explicit missing-data lists; do not claim a playable case if market/valuation coverage is incomplete. Keep the whole response under 1800 words.

For each candidate return:
- candidate_id, issuer, historical ticker, share class, cutoff, horizon unit/count;
- neutral business summary (40-60 words);
- 6 material financial/operating facts, each with value/unit/period/publication date/primary source URL and clear claim type (reported, guidance, derived);
- 3 dated recent developments known by the cutoff;
- 3 horizon-relevant open questions, labeled editorial interpretations;
- the sector evidence needed (Alphabet: search/cloud/advertising, spending, competition; Merck: commercial portfolio, concentration, pipeline, patent/disclosed exclusivity timelines, financing);
- at least 3 distinct relevant primary documents if available (no current company profile substituted for a historical one);
- available_at confidence and gaps for each source: verify original public timing separately from the reporting period, archive upload date or later amended version;
- missing_data, repairs_needed, and status "research_draft".

Return root fields "cases", "source_checks", "limitations". Do NOT include future outcomes, retrospective winners/losers, later regulatory decisions, later financial results, future-relative labels such as "before the top", or an investment recommendation. For the Merck outcome pipeline, flag that a five-year total-return reconstruction must check dividends and corporate actions, including any distributed securities; do not fetch future events into the player evidence packet.

If a fact cannot be verified, omit it or use null with a reason. Do not fabricate consensus, valuation, publication timestamps, historical market prices, or source URLs. Preserve fiscal/calendar period distinctions. We will validate the output before publishing anything.
