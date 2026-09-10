#!/usr/bin/env python3
"""Merge cases/<id>/presentation.json (writer output per cases/SNAPSHOT_PRESENTATION_BRIEF.md) into
cases/<id>/player.json as financial_snapshot.presentation, after validating: every metric label matches a headline
tile exactly, group indices are in range, 4-6 metrics, word limits, no outcome words. Inputs are deleted only after
every player.json has been written. Run: python3 scripts/merge_presentation.py [--check-only]"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
check_only = '--check-only' in sys.argv
BANNED = re.compile(r'\b(cheap|expensive|undervalued|overvalued|will (rise|fall)|turned out|in hindsight|later)\b', re.I)
problems, ready = [], []
for f in sorted((ROOT / 'cases').glob('*/presentation.json')):
    cid = f.parent.name
    pr = json.loads(f.read_text())
    pj = ROOT / 'cases' / cid / 'player.json'
    player = json.loads(pj.read_text())
    labels = [h['label'] for h in player['financial_snapshot']['headline']]
    mode = pr.get('valuation_mode', player['financial_snapshot'].get('presentation', {}).get('valuation_mode'))
    if ('valuation_mode' in pr or mode is not None) and mode not in ('revenue', 'pipeline', 'bank'):
        problems.append(f'{cid}: invalid valuation_mode {mode!r}')
    metrics = pr.get('metrics') or []
    if not (4 <= len(metrics) <= 6): problems.append(f'{cid}: {len(metrics)} metrics')
    for i, m in enumerate(metrics):
        if m.get('metric') not in labels: problems.append(f'{cid}: metric {i} label not found: {m.get("metric")!r}')
        if len((m.get('context') or '').split()) > 35: problems.append(f'{cid}: metric {i} context {len(m["context"].split())} words')
        if BANNED.search(m.get('context') or ''): problems.append(f'{cid}: metric {i} context has a banned word')
        if not m.get('label'): problems.append(f'{cid}: metric {i} has no label')
    used = [j for g in pr.get('groups') or [] for j in g.get('metrics', [])]
    for j in used:
        if not (0 <= j < len(metrics)): problems.append(f'{cid}: group index {j} out of range')
    if sorted(used) != list(range(len(metrics))): problems.append(f'{cid}: groups do not use each metric exactly once: {sorted(used)}')
    if not (2 <= len(pr.get('groups') or []) <= 3): problems.append(f'{cid}: {len(pr.get("groups") or [])} groups')
    if len((pr.get('valuation_context') or '').split()) > 45: problems.append(f'{cid}: valuation_context {len(pr["valuation_context"].split())} words')
    if BANNED.search(pr.get('valuation_context') or '') or BANNED.search(pr.get('intro') or ''): problems.append(f'{cid}: intro/valuation_context has a banned word')
    if not any(p.startswith(cid + ':') for p in problems):
        player['financial_snapshot']['presentation'] = {k: pr[k] for k in ('intro', 'groups', 'metrics', 'valuation_context')}
        if mode is not None:
            player['financial_snapshot']['presentation']['valuation_mode'] = mode
        ready.append((f, pj, player))
if problems or check_only:
    print(f'ready {len(ready)}; problems: {len(problems)}'); print('\n'.join(problems)); sys.exit(1 if problems else 0)
for f, pj, player in ready:   # write every player.json first, then remove the inputs
    pj.write_text(json.dumps(player, indent=2, ensure_ascii=False) + '\n')
for f, pj, player in ready:
    f.unlink()
print(f'merged {len(ready)}; problems: 0')
