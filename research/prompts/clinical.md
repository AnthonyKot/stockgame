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

Batch clinical. Find 10 DISTINCT issuers, emphasizing clinical/regulatory uncertainty and mixed evidence. Suggested leads (replace if source coverage is poor): Axsome AXSM late 2019 (1y), Sage SAGE 2019 (1y), FibroGen FGEN 2021 (3y), Nektar NKTR 2018 (5y), Intercept ICPT 2016 (5y), Madrigal MDGL 2018 (5y), BioMarin BMRN 2020 (3y), Acadia Pharma ACAD 2021 (3y), Sarepta SRPT 2020 (3y), bluebird bio BLUE 2019 (5y). Include successes, failures and mixed/business-as-usual outcomes as source-supported editorial stories. Do not favor famous terminal outcomes. ID prefix clinical-.

