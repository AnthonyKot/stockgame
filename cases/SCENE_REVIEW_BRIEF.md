# Scene review brief (pre-decision text checked against the case's own evidence)

You review ONE case's opening scene: the text a player reads BEFORE deciding. You report; you do not edit. The same class of defect was found in the debriefs (wrong chronology, motive read into facts, a number attributed to the wrong period or population), so read every clause as a sceptic.

Inputs (read only these; no web access):
- `cases/scenes.json` → `scenes[<candidate_id>]`: `voice` (the pitch), `claims` (scene claims `s1..` each mapped to evidence `claim_ids`), `question`, `ask_friend[{q, a, claim_ids}]`, `assumptions[{id, text, side}]`.
- `cases/<candidate_id>/evidence.json`: `claims[{id, text, source_ids, status, formula}]`, `sources` (title, publisher, available_at / published date, excerpt), `repairs_needed`.
- `cases/<candidate_id>/player.json`: the packet (what_changed, financial_snapshot, catalysts, unresolved questions), with its own citations.
- `research/selected.json`: the cutoff date for the case.

Check, for every sentence of `voice`, every `claims[].text`, every `ask_friend[].a`, and every assumption:
1. Support: does a cited evidence claim (or its source excerpt) actually say this? Note numbers that differ, periods that differ (quarter vs year, fiscal vs calendar), populations that differ (subgroup vs all patients, one segment vs the company).
2. Point in time: is anything stated as fact that was only expected, proposed, or agreed-but-not-closed at the cutoff? Is any date, or "recently", "just", "last week", wrong relative to the cutoff?
3. Motive and causation: does the text say why management or the market did something when the source only says what happened?
4. Leaks: any name, ticker, product name or later-known fact that the masking should have hidden, or any hint of the outcome.
5. Assumptions: is each one a single proposition a later event could support or weaken? Flag compound assumptions and ones that already contain a verdict.
6. `question`: is it neutral, or does it lead toward one answer?

Output: write ONLY `research/scene-review/<candidate_id>.md` with three sections:
- `## Confirmed defects` — one bullet each: quote the exact sentence, name the field (voice / s2 / ask_friend[1] / a3), cite the evidence claim id and quote the excerpt that contradicts or fails to support it, state what is wrong in one line, and give a minimal corrected wording that stays within the evidence.
- `## Unsupported or unverifiable` — clauses with no cited claim or whose cited claim does not cover them; say what evidence would be needed.
- `## Editorial preferences (not defects)` — anything else, briefly.
If a section is empty, write "None found." Keep the file under 900 words.

Final reply: three lines: candidate id, number of confirmed defects, number of unsupported clauses. Nothing else.
