# Session progress — 10 September 2026

Plan: [NEXT_SESSION_PLAN.md](NEXT_SESSION_PLAN.md). Master checklist: [TODO.md](../TODO.md). This file holds interim findings, evidence and the next action; durable raw results go in [session-results/](session-results/).

## Ownership agreed with the user

- **Codex:** payload checks, test/merge-script fixes, integration verification, and the handoff/progress documents. Owns `scripts/` for this work; coordinate any needed runtime change separately.
- **Other content session:** valuation framing by case type and Nektar's pending-deal note beside net cash, in authored case content. Codex will not edit those content files while that work is active.
- The content session reports changed files, validation results and any generated bundles in its reply. Codex records the handoff here to avoid simultaneous edits to the log. Coordinate bundle regeneration after source edits have settled.
- Residual Sarepta feedback questions below are review findings, not an instruction to expand that session's two agreed content items.

## Step 1 — complete: establish remaining work

Baseline HEAD: `c89adddffc69fc5341bf25cca20947f35068a2d6`. Existing documentation edits were preserved. No application code or authored case content was changed in Step 1.

### Repairs already present

- Target a3 now dates resumption to March 2022 and the cuts to May/June, keeping the original motivation unresolved.
- First Solar distinguishes enactment from durability and capacity from demand in the reviewed updates.
- Sarepta financing now distinguishes repayment of previous debt; its accelerated-approval feedback names the surrogate rather than equating approval with the functional result.
- All-ten financial presentation and label validation have landed.
- Dated merge now saves before deleting inputs. It is still not atomic or all-or-nothing.

These findings come from direct inspection of the current assumptions and updates. They do not certify every clause against original sources.

### Step 1 issue register (findings at baseline)

| ID | Evidence/status | Smallest next action | Owner |
| --- | --- | --- | --- |
| S1 | Observed in `test_dated_debrief.js`: a blanket assertion forbids Supported/Partly supported/Weakened/Not supported → Unresolved. This can reject legitimate reassessment; current data pass. | Keep checks for specific historical propositions; permit evidence-backed uncertainty and test a synthetic valid reassessment. | Codex |
| S2 | Reproduced in a temporary fixture: a mixed valid/invalid dated batch exits 1 but changes scenes.json and deletes the valid writer input. | Validate the complete batch before writes; add a failure-path regression. | Codex |
| S3 | Reproduced in a temporary fixture: an unknown event ID crashes check-only with `ValueError: max() iterable argument is empty`. Inputs remain intact, but the useful validation message is lost. | Stop dependency processing for invalid references; return a clear validation failure. | Codex |
| S4 | Observed direct `write_text` in both merge scripts. Dated merge has no atomic replacement; presentation merge can leave partially written destinations on failure. Destructive write failure not exercised against real files. | Implement/test dated atomic replacement on fixtures; track presentation transaction handling separately. | Codex |
| S5 | Observed: pre-decision assertion checks only the `dated_debrief` key. New boundary tests check event membership, not the actual selected check/narrative. | Add explicit expected-output fixtures and checks for distinctive outcome text under other payload keys. | Codex |
| C1 | Needs further source review: Sarepta a1 e7 says “Supported so far” while its own caveat does not establish the functional effect; e10/e11 says “never confirmed,” which may exceed the bounded record. | Read alongside the original compound assumption; consider “Partly supported” and a record/exit-scoped limitation. Do not silently broaden current content ownership. | Later content review |

Raw reproduction and baseline results: [step-01-evidence.json](session-results/step-01-evidence.json). Reproductions used disposable `/tmp` copies; no real writer inputs were deleted.

### Checks run

- `verify_cases.py`: all ten passed.
- `merge_dated_debrief.py --check-only`: zero problems, zero drift warnings.
- `merge_presentation.py --check-only`: zero pending inputs, zero problems. This does **not** independently validate all ten stored presentations; the case verifier performs their label checks.
- `test_story_dates.js`: passed.
- `test_dated_debrief.js`: 10 cases, 28 horizon exits, 73 publication boundaries, 71 status transitions and six named verdict checks passed.

## Authorized engineering work — four points complete locally

The user subsequently authorized all four engineering points. Local work integrates valuation content `0b1a673` and concurrent scene-text commit `c4de944`. Authored case files and scene-review documents are preserved. The latter landed during verification, so case/build/payload/date checks were repeated on that version.

- **Point 1 / S5:** added recursive payload checks for outcome-only fields and distinctive copied outcome sentences across all ten sheets/markets and the index, with deliberate contamination fixtures. Added 12 independent expected verdict/narrative assertions before/on/after publication, including delayed and retrospective publication, month precision and no eligible event.
- **Point 2 / S1:** removed the universal ban on returning to Unresolved. The synthetic selector and merge fixtures demonstrate a legitimate reassessment; six specific known-regression checks remain.
- **Point 3 / S2–S4 (dated):** the whole batch validates before mutation; scenes.json is written to a flushed sibling temporary file and atomically replaced before input deletion. Unknown events return useful errors. Validation/save failure preserves inputs; cleanup failure reports a safely retryable state. Twelve isolated fixture tests cover these paths. Presentation multi-file transaction recovery remains a separate open item.
- **Integration protection:** presentation merges preserve an omitted existing valuation_mode, accept revenue/pipeline/bank and reject invalid values. Four fixture tests cover explicit, omitted and invalid modes; the case verifier checks stored modes.
- **Content handoff:** Nektar, Axsome and Madrigal pipeline valuation framing, Nektar's pending partnership proceeds note and corrected share units are present in `0b1a673`. No authored content changes were needed for these script repairs.

### Verification

Case verifier: all ten passed. Both merge check-only commands: zero problems (presentation has no pending writer inputs). Twelve dated-merge and four presentation-merge fixture tests passed. Builder, return arithmetic, simulator equivalence, payload tests, story dates and all-case dated tests passed. Dated coverage: 28 horizons, 73 publication boundaries and six verdict pins; 71 transitions inspected without a blanket monotonicity rule.

Existing desktop/mobile story regression passed again after c4de944, including actual exits, stop/target, no-event exit, reload, save failures and journal behavior. The new four-case valuation integration browser test caught Madrigal mobile overflow from the long funding-runway unit. A scoped snapshot-number wrapping rule fixes it; all eight desktop/mobile case journeys now pass, including keyboard disclosure and corrected share units. The fixture was also corrected to accept cases that go straight to the debrief without a walkthrough gate. Rebuild changed only index.json's build timestamp; case bundles match the integrated content.

### Remaining limits and checkpoint

Text copying checks cannot certify historical truth or catch arbitrary paraphrases. Full outcome files still load after commitment. C1 and broader editorial/source review remain separate from these engineering safeguards. The original plan's manual Target/First Solar/Sarepta reading journeys are not all replaced by the narrower automated integration coverage.

Madrigal still renders a raw underscore-separated funding-runway unit; its reader-facing wording is an editorial follow-up.

Next user-facing action: playtest the integrated local build. No commit, push or deployment was performed by Codex for this repair batch; the content session's reported deployment has not been independently reverified here.

Durable results: [step-02-04-evidence.json](session-results/step-02-04-evidence.json).
