# Next two hours: verify the repairs, play the stories, close remaining gaps

Prepared 10 September 2026 against HEAD `c89addd`. Time blocks are estimates of active work, not deadlines or permission to skip checks. User playtesting or unavailable sources can extend elapsed time.

Interim evidence and the agreed division of work: [SESSION_PROGRESS.md](SESSION_PROGRESS.md). Step 1 and the four subsequently authorized engineering points are implemented; source-of-truth verification and the playtest checkpoint are recorded there. The original broader editorial/user-review steps below remain distinct.

## Intended outcome

A small, reviewed set of stories whose feedback answers the player's original assumptions and whose revised financial summaries are useful to read. Finish with tested changes, a clear playtest checkpoint and an accurate handoff. Keep the shared-portfolio campaign and new research batches deferred.

This document plans the next work; its unchecked steps are not completed implementation. [TODO.md](../TODO.md) remains the master checklist. [The earlier review](DATED_DEBRIEF_REVIEW.md) supplies examples, but several fixes have since landed.

## Planning-time evidence — historical baseline

- Target corrections: `56d4119`; Sarepta corrections: `912a622` and `16bc3b2`; assumption-consistency corrections: `ecbd188`.
- Financial presentation rolled out to all ten cases in `4d94147`; label guard and trillion formatting exist. Nektar is no longer the only case with an authored presentation.
- The dated merge script now writes scenes.json before deleting writer inputs. It still writes directly to the destination and can merge valid cases despite errors elsewhere in the batch. Atomic replacement and failure-path coverage remain open.
- `test_dated_debrief.js` now includes verdict checks and publication boundaries. Planning-time run passed: 10 cases, 28 horizon exits, 73 publication boundaries, 71 status transitions and six named verdict checks. Merge check-only passed with no problems or drift warnings.
- The test universally rejects certain definite statuses reverting to Unresolved. That is a new review concern: evidence can legitimately reopen an empirical question. Review assumption identity and evidence, rather than enforcing confidence that can only increase.
- The working tree contains documentation changes. Inspect it before editing, and recheck HEAD at each patch boundary because concurrent sessions have committed during this work.

## 1. Establish the exact remaining work — 0–15 minutes

- [x] Inspect the latest commits, working tree, three corrected cases, dated selector/tests, and both merge scripts.
- [x] Read each changed verdict beside the original assumption and its cited event. Record confirmed defects separately from editorial preferences.
- [x] Confirm existing validators and identify only the tests relevant to the next patch. Do not repeat all research or rewrite unchanged cases.

Deliverable: a short list of remaining issues, each with the affected case/date, expected behavior and smallest fix. If a reviewed issue is already resolved, mark it done rather than implementing it again.

## 2. Finish the feedback corrections and focused checks — 15–40 minutes

- [ ] Verify Target's guidance dates and removal of inferred motives, First Solar's enactment-versus-durability and capacity-versus-demand distinctions, and Sarepta's financing/approval/population distinctions.
- [ ] Correct only residual unsupported or misleading statements. Use existing primary sources; reopen the specific source if a factual clause needs confirmation. Report unavailable evidence and narrow the wording rather than starting broad research.
- [x] Review the blanket status-transition failure. Keep specific checks for fixed historical propositions (such as enactment), but allow evidence-backed uncertainty for empirical assumptions. Add an example demonstrating a legitimate return to Unresolved and preserve regressions for the actual reviewed errors.
- [x] Verify selection at before/on/after-publication boundaries using explicit expected dates, including a retrospective source, month-only date, and exit before any event. Check the rendered replacement, not only the list of eligible events.

Deliverable: a small content/test patch and concise before/after examples. Automated checks protect date selection and known regressions; manual source review establishes whether the conclusions follow.

## 3. Exercise three complete reading journeys — 40–65 minutes

- [ ] Play Target (1y and 3y), First Solar (1y and 3y; inspect later policy update separately), and Sarepta (3y and 5y). Choose assumptions implicated in the review.
- [ ] Check that each debrief explains the selected assumption at the actual exit, that the main view ends there, and that later context requires an explicit action.
- [ ] Include one stop/target exit and a midway reload. Reuse existing tests where they cover the path; add coverage only for a new failure or meaningful gap.
- [ ] Inspect the authored financial summaries for those cases on desktop and 390px: correct labels/values, comparable periods, visible material caveats, accessible disclosures, and a reachable decision control.
- [ ] If a problem repeats across these examples, identify the shared cause. Do not launch an all-ten presentation rewrite.

Deliverable: evidence-backed journey results and direct local playtest links. Resolve blockers in this slice before presenting it as ready.

## 4. User playtest checkpoint — roughly 65–80 minutes

- [ ] Present the corrected Target 3y journey first, with one short example of what changed. Offer First Solar/Sarepta for comparison.
- [ ] Ask whether the evidence helps the player judge their chosen assumption and whether the financial section has the right amount of detail.
- [ ] Capture feedback as concrete next edits. Keep changes small; do not infer approval for a broader redesign from silence.

Pause player-facing expansion here. If feedback is pending, the independent merge-safety work below can proceed once implementation of this plan is underway; waiting is not approval of new product changes.

## 5. Finish merge recovery and payload checks — 80–105 minutes

- [x] Validate the entire dated-debrief batch before any mutation. Invalid JSON, unknown IDs or invalid dates should give useful errors and preserve all inputs.
- [x] Write to a temporary file beside scenes.json, replace the destination atomically, then archive/delete inputs. If cleanup fails, leave recoverable inputs and report the issue; rerunning must not duplicate content.
- [x] Use temporary fixtures to test invalid mixed batches, failed writes/replacement, successful merge and rerun. Never test failure handling against real writer files.
- [x] Inspect the presentation merge script for the same risk; record any separate repair needed rather than silently claiming both are fixed.
- [x] Strengthen pre-decision checks to detect outcome fields and distinctive outcome text copied under another field. Preserve legitimate overlap with starting assumptions; document the limits of text checks.

Deliverable: recoverable dated merging with failure-path tests, and a narrower, defensible payload-isolation claim.

## 6. Verify and hand off — 105–120 minutes

- [x] Rebuild only when source content changed; inspect generated changes for unintended case churn.
- [x] Run case/presentation validators, merge check-only, dated tests and the relevant browser regression. Arithmetic suites are required if execution/builder logic changed; otherwise retain the earlier passing evidence and state its scope.
- [x] Run syntax/whitespace checks and inspect the final diff. Preserve unrelated edits and the user's journal.
- [x] Update TODO and architecture with what actually passed, unresolved issues and the next player action.
- [x] Report the exact local/committed/deployed state. Planning or local testing does not establish deployment; if publishing becomes authorized, verify the resulting build and served version.

Deliverable: a concise change/test report and a clear stop. If the two-hour window ends early, leave remaining steps unchecked rather than broadening or rushing the work.

## Scope rules

No new stories, account system, RAG platform, portfolio ledger or schema migration in this session. No worker batch is needed. A source blocker gets a bounded follow-up; a failing verification stays open. User feedback can change the sequence, and newly landed commits must be inspected before repeating planned work.
