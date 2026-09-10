# Dated debrief review — 10 September 2026

> Planning update, HEAD `c89addd`: subsequent commits implement the Target/Sarepta/First Solar corrections, expand dated tests, and move input deletion after saving. The findings below describe the earlier reviewed state. Atomic merging, broader payload checks and review of the new universal status-transition rule remain open. Follow [NEXT_SESSION_PLAN.md](NEXT_SESSION_PLAN.md) before treating any finding as still unimplemented.

Read-only review of commit `ee0752c` and the working implementation. This records verified behavior and proposed repairs; the repairs below have not been implemented by this documentation update. Product authority remains [MASTER_PLAN.md](../MASTER_PLAN.md); the immediate scope is standalone story refinement.

## Confirmed

- All ten cases contain `scene_check.dated_debrief`. The nine additions contain 6–8 updates each; Nektar has five. The existing schema and `site/story.js` selector were reused.
- The selector requires both occurrence and source publication dates to precede the actual opening-price exit. Stop-loss and take-profit exits are supplied by the simulator. Month-only dates use month end conservatively.
- Case validation, `merge_dated_debrief.py --check-only`, return arithmetic, simulator equivalence, `test_story_dates.js`, `test_dated_debrief.js`, and the browser regression passed during this review. The all-case test exercised 28 available calendar-horizon exits.
- All ten live outcome JSON files matched the local bundles during the review. [GitHub Pages deployment of ee0752c succeeded](https://github.com/AnthonyKot/stockgame/actions/runs/34445971499). This is a dated observation, not verification of later deployments or UI changes.
- Hershey's one-year exit is 5 February 2024 and has two eligible events. Its pricing-power verdict starts “Supported.” and includes a caveat, rather than literally “Supported, with a caveat.” The three-year exit includes the cocoa-cost developments; its latest narrative discusses late-2025 Salty Snacks growth.
- The commit records nine Sonnet writers. Their model selection and parallel execution were not independently established from retained run artifacts.

## Findings and proposed corrections

### High: verdicts sometimes change the assumption being assessed

In `cases/scenes.json`, First Solar (`growth-007`) assumption a3 asks whether proposed manufacturing incentives will become law. After enactment, later updates reset the verdict to Unresolved/Partly supported because durability and sourcing requirements change. Keep enactment Supported; discuss durability separately. For a2, factory openings establish capacity, not that customer demand fills it.

Sarepta (`clinical-srpt-2021`) a1 addresses the younger subgroup. A later restriction affecting a broader population should not silently replace that question with a verdict on the full approved population. Distinguish regulatory action, evidence of efficacy, safety and the population actually tested.

Acceptance: each revised verdict answers the exact original assumption. Later evidence may change the answer only when it bears on that proposition. A price gain, factory opening or regulatory decision is not interchangeable with evidence for a different claim.

### High: Target chronology and inference

`growth-004` a3 says guidance was cut twice within three weeks of resuming and treats the revisions as proof that earlier silence reflected genuine unpredictability. The local events date resumption to 1 March 2022 and the cuts to 18 May and 7 June. Three weeks separates the cuts, not resumption and both cuts. The later revisions cannot establish management's earlier motivation.

Suggested replacement:

> Unresolved. Guidance resumed in March and was reduced in May and June. Those revisions show forecast instability, but do not establish whether the original decision to withhold guidance reflected caution or an anticipated deterioration.

References: `cases/growth-004/aftermath.json` e1/e2/e3 and [Target's June update](https://corporate.target.com/press/release/2022/06/target-corporation-announces-updated-2022-plan-foc).

Acceptance: repair both the chronology and the intent inference; cite every event needed to support the replacement.

### High: Sarepta summaries overstate their cited evidence

The e4 update describes a $1.13 billion “program need,” while its cited event says substantial proceeds refinanced existing debt. Describe issuance and use of proceeds separately; do not equate gross debt issuance with new program funding.

The e5 update describes accelerated approval as based on the same ages 4–5 subgroup. The approval basis was micro-dystrophin expression; distinguish the authorized age range from the surrogate endpoint and from proof of functional benefit. See `cases/clinical-srpt-2021/aftermath.json` and the [FDA's June 2023 announcement](https://content.govdelivery.com/accounts/USFDA/bulletins/36175f5).

Acceptance: repair these summaries against their sources without adding new research scope or treating approval as proof of the original functional-effect assumption.

### Medium: passing tests are described too broadly

`test_dated_debrief.js` checks that the key string `dated_debrief` is absent from the sheet, that cited IDs exist, and that at least one assumption changes when eligible events exist. It does not establish that every clause is supported, every assumption is correctly assessed, or no future prose appears under another field. It also derives eligibility from the selector's own returned events rather than an independent expected result.

Proposed checks:

- Independent fixtures immediately before, on and after publication, including month precision and delayed retrospective sources.
- Early exits and zero-eligible-event behavior across representative cases, in addition to calendar anniversaries.
- Targeted regressions for the reviewed assumptions, with manual evidence review for entailment and chronology.
- Pre-decision payload checks for outcome text/fields, not only the name of one field.

Report the current checks as structural and behavioral coverage, not complete factual verification. Full outcome files still load after commitment; optional context is presentation separation, not campaign-clock isolation or access control.

### Medium: merging can lose writer output on failure

`merge_dated_debrief.py` unlinks per-case files before writing `scenes.json`. A crash or failed final write can lose unmerged output. It can also merge valid cases despite errors in others. Its docstring claims date-order validation that the implementation explicitly leaves to the renderer.

Proposed sequence: load and validate the entire batch; write a temporary merged file; atomically replace the destination; only then archive or delete the inputs. Preserve inputs on validation/write failure. Align the documentation with actual validation, including baseline checks, date formats and candidate identity.

Acceptance: failure-path tests prove input files and the old scenes file survive a failed write or invalid batch; a successful merge remains repeatable without duplicate content.

## Smallest proposed next batch

1. Correct the identified Target, First Solar and Sarepta verdicts against their existing sources.
2. Add the corresponding focused regressions and independent date-boundary fixtures.
3. Make merging recoverable and test its failure paths.
4. Rebuild affected bundles, run the relevant checks, and pause for a story playtest.

No new schema, all-ten rewrite, research-worker batch or campaign implementation is implied. Broader editorial readiness triage remains separate. The latest user request authorizes documentation updates, not automatic execution of this proposed repair batch.
