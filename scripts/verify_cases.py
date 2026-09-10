"""Cheap deterministic checks on cases/<id>/player.json and evidence.json. Exit 1 on any failure."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BAN = re.compile(r"\b(later|eventually|subsequently|ultimately|turned out|took years|would go on|went on to|ahead of|before the (top|crash|collapse|approval)|in hindsight|retroactively)\b", re.I)
sel = json.loads((ROOT/'research'/'selected.json').read_text())
fail = 0
for r in sel['selected']:
    d = ROOT/'cases'/r['id']; pj, ej = d/'player.json', d/'evidence.json'
    if not pj.exists(): print(f'{r["id"]}: player.json MISSING'); fail += 1; continue
    try: p = json.loads(pj.read_text()); e = json.loads(ej.read_text()) if ej.exists() else {}
    except Exception as ex: print(f'{r["id"]}: JSON error {ex}'); fail += 1; continue
    probs = []
    cy = int(r['proposed_cutoff'][:4])
    txt = json.dumps({k: v for k, v in p.items() if k not in ('transparent', 'editorial_notes', 'editor_corrections')})
    for m in BAN.finditer(txt): probs.append('banned word: ' + txt[max(0, m.start()-50):m.end()+30].replace('\n', ' '))
    GUIDE = re.compile(r'expect|anticipat|target|guidance|guided|plan|could begin|window|into (the )?(first|second|third|fourth|Q[1-4]|20)|estimate|forecast|outlook|scheduled|subject to|announced_on|timing', re.I)
    for m in re.finditer(r'\b(20[12]\d)\b', txt):
        if int(m.group(1)) > cy and not GUIDE.search(txt[max(0, m.start()-160):m.end()+80]):
            probs.append(f'future year {m.group(1)} without guidance wording: ...' + txt[max(0, m.start()-70):m.end()+30].replace('\n', ' '))
    if p.get('cutoff') != r['proposed_cutoff']: probs.append(f'cutoff mismatch {p.get("cutoff")} vs {r["proposed_cutoff"]}')
    h = p.get('financial_snapshot', {}).get('headline', [])
    if len(h) != 6: probs.append(f'headline has {len(h)} entries, need 6')
    pres = p.get('financial_snapshot', {}).get('presentation')
    if pres:   # the renderer skips a row silently when a label does not match, so catch it here
        labels = [t['label'] for t in h]
        for i, m in enumerate(pres.get('metrics', [])):
            if m.get('metric') not in labels: probs.append(f'presentation metric {i} does not match a headline label: {m.get("metric")!r}')
        used = [j for g in pres.get('groups', []) for j in g.get('metrics', [])]
        if any(not (0 <= j < len(pres.get('metrics', []))) for j in used): probs.append('presentation group index out of range')
        if sorted(used) != list(range(len(pres.get('metrics', [])))): probs.append('presentation groups do not use each metric exactly once')
    uq = p.get('upcoming_and_unresolved', {}).get('unresolved_questions', [])
    if len(uq) != 3: probs.append(f'{len(uq)} unresolved questions, need 3')
    cids = {c['id'] for c in e.get('claims', [])}; sids = {s['id'] for s in e.get('sources', [])}
    used = set(re.findall(r'\[(c\d+)\]', txt))
    if used - cids: probs.append(f'claims cited but undefined: {sorted(used - cids)[:5]}')
    for c in e.get('claims', []):
        if set(c.get('source_ids', [])) - sids: probs.append(f'claim {c["id"]} cites unknown source')
    for s in e.get('sources', []):
        if str(s.get('available_at', '9999'))[:10] > r['proposed_cutoff'][:10]: probs.append(f'source {s["id"]} available_at after cutoff')
    for name in (p.get('transparent', {}).get('issuer', ''), p.get('transparent', {}).get('ticker', '')):
        if name and re.search(r'\b' + re.escape(name.split(',')[0].split(' ')[0]) + r'\b', json.dumps(p.get('masked', {}))): probs.append(f'masked block leaks "{name}"')
    words = len((p.get('masked', {}).get('business_two_sentences', '') + ' ' + ' '.join(x.get('fact', '') for x in p.get('what_changed', [])) + ' ' + ' '.join(uq)).split())
    print(f'{r["id"]}: claims {len(cids)} sources {len(sids)} first-screen-ish words {words} repairs {len(e.get("repairs_needed", []))}' + (' OK' if not probs else ''))
    for x in probs: print('   -', x)
    fail += bool(probs)
sys.exit(1 if fail else 0)
