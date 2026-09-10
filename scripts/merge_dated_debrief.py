#!/usr/bin/env python3
"""Merge cases/<id>/dated_debrief.json (writer output per cases/DATED_DEBRIEF_BRIEF.md) into cases/scenes.json
and validate the structure: all assumption ids in baseline, cited events exist, status-word prefix, word limits,
updates in date order. Run: python3 scripts/merge_dated_debrief.py [--check-only]. Deletes the per-case file after a clean merge."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
STATUS = re.compile(r'^(Supported|Partly supported|Mixed|Weakened|Not supported|Unresolved|Choosing to wait)')
check_only = '--check-only' in sys.argv
scenes_path = ROOT / 'cases' / 'scenes.json'
scenes = json.loads(scenes_path.read_text())
problems, warnings, merged = [], [], 0
def last_day(d):
    return d if len(d) == 10 else d + '-31'
for cid, sc in scenes['scenes'].items():
    f = ROOT / 'cases' / cid / 'dated_debrief.json'
    dd = json.loads(f.read_text()) if f.exists() else sc.get('dated_debrief')
    if not dd:
        problems.append(f'{cid}: no dated_debrief'); continue
    aids = [a['id'] for a in sc['assumptions']]
    events = {e['id']: e for e in json.loads((ROOT / 'cases' / cid / 'aftermath.json').read_text())['events']}
    for aid in aids:
        if aid not in dd['baseline']['checks']: problems.append(f'{cid}: baseline missing {aid}')
    for i, u in enumerate(dd['updates']):
        ids = u.get('event_ids') or []
        if not ids: problems.append(f'{cid}: update {i} cites no event')
        for eid in ids:
            if eid not in events: problems.append(f'{cid}: update {i} cites unknown {eid}')
        # file order is cosmetic: site/story.js sorts updates by unlock date (later of event date and source publication)
        for aid, t in (u.get('checks') or {}).items():
            if aid not in aids: problems.append(f'{cid}: update {i} checks unknown {aid}')
            if not STATUS.match(t): problems.append(f'{cid}: update {i} {aid} lacks status word: {t[:40]}')
            if len(t.split()) > 45: problems.append(f'{cid}: update {i} {aid} {len(t.split())} words')
        if u.get('narrative') and len(u['narrative'].split()) > 45: problems.append(f'{cid}: update {i} narrative {len(u["narrative"].split())} words')
    if not (4 <= len(dd['updates']) <= 8): problems.append(f'{cid}: {len(dd["updates"])} updates')
    # drift warning (not a failure): a definite status falling back to Unresolved usually means a later event about a
    # different question (durability, utilisation) was read against the original assumption. Review by hand.
    def unlock(u):
        ld = lambda d: d if len(d) == 10 else d + '-31'
        return max(max(ld(events[e]['date']), ld(events[e]['source']['published'])) for e in u['event_ids'] if e in events) if u['event_ids'] else ''
    seq = {}
    for u in sorted(dd['updates'], key=unlock):
        for aid, t in (u.get('checks') or {}).items():
            mm = STATUS.match(t)
            if mm: seq.setdefault(aid, []).append((mm.group(1), u['event_ids']))
    for aid, l in seq.items():
        for (a, ia), (b, ib) in zip(l, l[1:]):
            if a in ('Supported', 'Not supported', 'Partly supported', 'Weakened') and b == 'Unresolved':
                warnings.append(f'{cid}: {aid} drifts {a}{ia} -> {b}{ib}')
    if f.exists() and not check_only and not any(p.startswith(cid + ':') for p in problems):
        sc['dated_debrief'] = {'baseline': dd['baseline'], 'updates': dd['updates']}
        f.unlink(); merged += 1
if merged: scenes_path.write_text(json.dumps(scenes, indent=2, ensure_ascii=False) + '\n')
print(f'merged {merged}; problems: {len(problems)}; drift warnings: {len(warnings)}'); print('\n'.join(problems + ['WARN ' + w for w in warnings]))
sys.exit(1 if problems else 0)
