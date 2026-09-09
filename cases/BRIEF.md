# Case bundle brief (player.json + evidence.json)

You are writing the pre-decision bundle for ONE or TWO cases of a historical investing game. Read, in this order: research/MVP_PROMPT.md (hard rules and your case's section), CASE_FORMAT.md (eight-block sheet), then your case's folder under cases/<candidate_id>/ which already contains xbrl-facts.json (SEC XBRL facts filed on/before the cutoff, with `filed` dates) and, for some cases, local EDGAR filing copies under research/sources/.

Tools: Read, Write, WebFetch, WebSearch, Bash (read-only: cat, grep, python for parsing). Budget per case: 20 WebFetch, 8 WebSearch. Write ONLY cases/<candidate_id>/player.json and cases/<candidate_id>/evidence.json. Never read research/prices/, research/selected.json's screen fields, or any outcome material. Never look up what happened after the cutoff.

## Absolute rules

1. Every fact must have been public before the cutoff. Use `available_at` = the filing acceptance date or wire dateline (ISO date). If you only know a date, that is fine; the site treats it as eligible from the next session. If you cannot establish that a document was public before the cutoff, do not use it.
2. No fabrication. No consensus numbers, no prices, no market caps, no "the stock rose", no invented URLs. A number you did not see in a source is `null` with `status: "missing"` and a reason. Prefer xbrl-facts.json for financial rows; cite the accession number (`accn`) as the source id.
3. No future-relative language anywhere. Banned: later, eventually, subsequently, ultimately, turned out, ahead of, before the (crash/top/approval), in hindsight, and any year after the cutoff year.
4. Distinguish `reported`, `management_guidance`, `derived` (with formula and inputs), `interpretation` (editorial, labelled), `missing`, `not_applicable`.
5. Plain language. Explain a clinical or accounting term inline the first time. A reader who does not know biotech vocabulary must be able to follow.
6. Word budgets: first screen 150–220 words (blocks 2, 5, 7 prose); expanded research up to 1,000 words plus tables.

## player.json schema (write exactly these keys)

```json
{
  "candidate_id": "clinical-axsm-2019",
  "schema_version": "mvp-1",
  "cutoff": "2019-12-17T09:00:00-05:00",
  "horizon": {"unit": "calendar_years", "count": 1},
  "exchange_calendar": "XNYS",
  "sector_module": "biotech" | "software" | "operating",
  "masked": {
    "alias": "a clinical-stage CNS drug developer",   // no name, no ticker, no brand names
    "sector": "Biotechnology (central nervous system)",
    "business_two_sentences": "40-60 words, no identifying names"
  },
  "transparent": {
    "issuer": "Axsome Therapeutics, Inc.", "ticker": "AXSM", "exchange": "NASDAQ",
    "business_two_sentences": "40-60 words, names allowed"
  },
  "financial_snapshot": {
    "adapter": "development_biotech" | "commercial_biotech" | "operating",
    "headline": [ {"label": "Cash and investments", "value": 123.4, "unit": "USD_millions", "period": "2019-09-30", "available_at": "2019-11-07", "source_ids": ["0001558370-19-010123"], "status": "reported", "definition": "cash, cash equivalents and short-term investments", "prior": {"value": 100.0, "period": "2018-12-31"} } ],   // exactly six entries; use null value + status missing when unavailable
    "history": [ {"row": "Revenue", "unit": "USD_millions", "cells": [ {"period": "FY2018", "value": 1.2, "available_at": "2019-02-28", "source_ids": ["accn"], "status": "reported"} ]} ]   // income statement, balance sheet, cash flow, shares: as many rows as the sources support, horizon-appropriate depth (8 quarters for 1y, 3-5 annual periods for 3-5y)
  },
  "what_changed": [ {"date": "2019-12-16", "fact": "...", "relationship_to_business": "...", "source_ids": ["..."], "status": "reported"} ],   // exactly three, or fewer with an explicit "no material update" entry
  "sector_evidence": { ...module-specific, see below... },
  "upcoming_and_unresolved": {
    "catalysts": [ {"description": "...", "timing_window": "first half of 2020", "announced_on": "2019-11-07", "source_ids": ["..."]} ],
    "unresolved_questions": ["...", "...", "..."]   // exactly three; neutral; no outcome hints
  },
  "macro_context": [ {"item": "...", "business_connection": "...", "available_at": "...", "source_ids": ["..."]} ],   // at most three; may be empty
  "help_me_weigh": {"own": ["..."], "flat": ["..."], "short": ["..."]},   // evidence-based arguments from eligible evidence only; unequal lengths are fine; cite source ids inline in brackets
  "source_handles": [ {"id": "...", "kind": "8-K" | "10-K" | "10-Q" | "press_release" | "trial_registry" | "regulator" | "other", "title": "...", "available_at": "...", "masked_title": "Company press release, 16 Dec 2019"} ],
  "missing_data": ["..."],
  "editorial_notes": "anything the reviewer must know; interpretations labelled"
}
```

Sector modules:
- `biotech`: `programs`: list of material programs with indication, drug/mechanism in plain language, phase, ownership/partner, trial id, design (randomized/blinded/control), sample sizes (planned/enrolled/analyzed), population, primary and secondary endpoints, latest evidence (effect size, CI, p-value, comparator, safety), management_says vs regulator_or_independent_says, next milestone window with announced_on, economic relevance. Plus `existing_products` (sales, concentration) or "none".
- `software`: paying customers and definitions, large accounts, retention/expansion if disclosed, gross margin, sales spend, stock compensation, competition; reported revenue vs prior guidance vs new guidance in separate rows; consensus row = missing.
- `operating`: segment table (revenue, margin or operating profit by segment, latest period and prior), guidance table (metric, prior guidance, new guidance, date), capital allocation (capex, dividends, buybacks, debt maturities within 24 months), competitive position facts, at most six rows each.

## evidence.json schema

```json
{
  "candidate_id": "...",
  "sources": [ {"id": "accn or slug", "kind": "...", "title": "...", "url": "...", "published_at": "ISO date or datetime", "available_at": "ISO date", "availability_basis": "EDGAR acceptance 08:25 ET" | "wire dateline" | "date only, treated as next session", "opened": true, "local_copy": "research/sources/... or null", "excerpts": [ {"claim_ids": ["c1"], "text": "verbatim, max 60 words", "location": "Exhibit 99.1 para 2"} ]} ],
  "claims": [ {"id": "c1", "text": "the sentence as used in player.json", "source_ids": ["..."], "status": "reported" | "management_guidance" | "derived" | "interpretation", "formula": null, "input_ids": null} ],
  "search_log": [ {"query_or_url": "...", "result": "opened | 403 | timeout | not_found", "note": "..."} ],
  "exclusions": ["what you found and left out, and why"],
  "repairs_needed": ["what a reviewer must fix before this case is playable"]
}
```

Every prose sentence in player.json that states a fact must correspond to a claim id whose sources are eligible. Include the claim id in square brackets at the end of the sentence, e.g. "... in the pivotal GEMINI trial [c3]."

## Process

1. Read your case section in research/MVP_PROMPT.md and the listed primary sources. Open them (WebFetch); if blocked, use the local EDGAR copy or fetch the EDGAR filing index for that date (https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<cik>&type=8-K&dateb=<yyyymmdd>&owner=include&count=20).
2. Use xbrl-facts.json for every financial number you can. Compute derived metrics only from eligible inputs and show the formula. Market capitalisation and enterprise value: `missing` with reason "historical price not in packet" unless the filing states a market value with its own date.
3. Write evidence.json first, then player.json. Save both after the first complete draft, then refine.
4. Run this self-check before finishing and fix every hit:
   `grep -inE "later|eventually|subsequently|ultimately|turned out|ahead of|hindsight" cases/<id>/player.json`
   and check that no year in player.json exceeds the cutoff year.
5. Final reply to the caller: five lines: case id, word count of first-screen prose, number of claims, number of sources opened, list of repairs_needed. Nothing else.
