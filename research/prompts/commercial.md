# Historical investment story research: exactly 10 candidate records

We are building an investing quiz game. The user wants 30 researched candidates, from which 10 will be selected manually by the lead agent. This is candidate discovery, NOT complete playable packets. Use Claude Sonnet as a cheap research worker. Your only tools are WebSearch and WebFetch. Do not delegate, run commands, access accounts, purchase data or edit files.

Return a single JSON object with keys batch, candidates, limitations. Exactly 10 candidates. Keep each candidate concise (roughly 200-300 words). Use public primary sources, at least 2 distinct relevant primary source URLs per candidate: one genuinely public at/before the proposed cutoff and another contemporary source OR an explicitly outcome-only later source. Actually open sources where possible. Do not fabricate URL paths or historical figures. At most 25 searches and 30 fetches total; stop with gaps when access fails. Search multiple companies in one query only if effective.

For every candidate return:
- id, issuer, historical_ticker, exchange, security_description;
- proposed_cutoff (ISO datetime with offset; default next trading weekday 09:00 America/New_York after a sourced release), horizon_years (1,3,5), proposed_exit_date (calendar anniversary; actual exchange-calendar verification is pending);
- neutral_title (no future spoiler), player_question (the actual economic tradeoff);
- as_of_facts: 3 concise facts with source_id and publication date, clearly distinguish reported result, guidance, interpretation;
- sources: [{id,url,title,published_date,role:as_of|outcome_only,opened:boolean,availability_notes}];
- retrospective_story: short editor-only outcome description supported by outcome sources, or null if not verified. Business/event outcome is not the same as investment return;
- return_hypothesis: buy|short|cash|unknown; this is explicitly an UNVERIFIED hypothesis for sorting the research queue, not a correct answer. Do NOT provide numerical stock returns from memory;
- learning_tension, information_gaps (including unverified execution prices/corporate actions), recognition_risk low|medium|high, data_complexity low|medium|high;
- status:research_candidate.

Requirements: all horizons must be complete as of 2026-09-09. Avoid ticker confusion (Merck US MRK vs Merck KGaA; Acadia Pharma ACAD vs Acadia Healthcare ACHC). Select precise security/share class and use historical names. Dates are proposed, not certified. For macro context/publications, public availability matters rather than accounting period. Source publications AFTER cutoff belong only in outcome metadata. Do not write a pre-event financial summary from a later retrospective report. Do not label an observed rally a short squeeze without positioning/covering evidence. An ordinary operating update is a valid story; don't manufacture drama.

Batch commercial. Find 10 DISTINCT biotech/pharma issuers emphasizing existing business, product concentration, patent/cliff risk, financing and ordinary earnings. Suggested leads (replace if poor coverage): Regeneron REGN 2019 (5y), Exelixis EXEL 2018 (5y), Gilead GILD 2019 (5y), Biogen BIIB 2021 (3y), Amgen AMGN 2018 (5y), Alnylam ALNY 2022 (3y), Incyte INCY 2020 (3y), Merck & Co. US MRK 2019 (5y), Harmony HRMY 2023 (1y), Neurocrine NBIX 2023 (1y). Explicitly include normal operating cases, not just binary trial gambles. ID prefix commercial-.

