# Three ideas, one recommendation

Product-owner page, 10 September 2026. Each idea has a folder with a scenario (`EPIC.md`) and an assessment (`README.md`): [idea1](idea1/README.md) the campaign, [idea2](idea2/README.md) investigate by asking, [idea3](idea3/README.md) the case as a quest. [MASTER_PLAN.md](MASTER_PLAN.md) remains the product authority; ideas 2 and 3 change how a scene is played, idea 1 connects the scenes.

## Side by side

| | Idea 1: campaign | Idea 2: ask the packet | Idea 3: quest |
|---|---|---|---|
| Player value | Decisions with consequences, a final report | Investigate in your own words | One screen, one fact, plain choices |
| Answers "cryptic"? | No, inherits today's page | Yes, if questions land | Yes, most directly |
| Effort | 8 to 12 sessions, 3 to 4 weeks | Stage A 3 sessions; Stage B +2 to 3 plus infrastructure | 3.5 sessions to ten quests |
| Runtime dependency | None | None for Stage A; a model and a proxy for Stage B | None |
| New data needed | Bitcoin series, dividend dates, split audit, calendar | None | None (pictures optional) |
| Chance built correctly | 80% | 90% (A), 70% grounding (B) | 90% |
| Chance preferred to today | 50%, 70% if presentation fixed first | 60% (A), 65% (B) | 70% newcomers, lower for experts |
| First playtest | Three stories with overlap | Nektar with search and notes | Nektar as a quest, with the "cryptic" friend |
| Kill criteria | Prototype no more engaging than three standalone cases; ledger needs invented data | Under half of natural questions land; "felt like guessing the engine" | Friend still cannot say what the game asks; clicks through without opening a fact |

## The shared first task

Ideas 2 and 3 both need **answer units**: ten to fifteen per case, one question, one cited answer under 60 words, dated, tagged, with synonyms, authored from packet text that already exists (`cases/<id>/units.json`, schema in [idea2/EPIC.md](idea2/EPIC.md) section 3). Idea 1 gates the same units by its clock. Whichever idea starts, the units for Nektar and their validator are the first day's work, and they land on `main`.

## Recommendation

**Branch `idea3` first.** It is the smallest, has no runtime dependency, is the direct answer to the only feedback we have, and everything it produces (units, the plain-language decision screen, the visited-node debrief) is reused by the other two. Its playtest is one evening with one friend.

**Then `idea2` Stage A** over the same units, behind the same front-page mode switch, so the friend can compare "choices" with "ask". Stage B waits for evidence from that comparison.

**Then `idea1`** on top of whichever presentation the playtests prefer. Its seven open decisions can be settled in the meantime, and the Bitcoin and dividend data fetched, so that the engine work starts with nothing missing.

## Branch plan

- `main` stays deployable; the CI gate runs the twelve suites on every push to it.
- The content layer (`units.json`, validator, builder emission) is developed on `idea3` and merged to `main` as soon as Nektar's units pass, so `idea2` branches from it.
- Each idea lives on its own branch and merges behind a front-page mode switch, never replacing the current page until a playtest says so.
- Engine and scripts are Codex's lane; content, screens and copy are Claude's; both run `scripts/run_checks.sh` before pushing.

## Decision requested

Confirm the order idea3 → idea2 → idea1, or name a different first branch. Nothing starts until then.
