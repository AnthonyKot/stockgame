#!/usr/bin/env python3
"""Validate the complete dated-debrief batch, atomically save scenes, then remove inputs.

Run with --check-only to validate without writes. The renderer orders updates by
publication/occurrence dates; this validator checks dates, references and text shape,
not whether the evidence supports the prose. Writer inputs survive validation or
save failure. Inputs left by a cleanup failure can safely be merged again.
"""
import argparse
import calendar
import datetime
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
STATUS = re.compile(r'^(Supported|Partly supported|Mixed|Weakened|Not supported|Unresolved|Choosing(?: to wait| not to take a position))\b')


def last_day(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?', value):
        raise ValueError(f'invalid date {value!r}; expected YYYY-MM or YYYY-MM-DD')
    parts = list(map(int, value.split('-')))
    if len(parts) == 2:
        parts.append(calendar.monthrange(*parts)[1])
    return datetime.date(*parts).isoformat()


def read_object(path):
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError('expected a JSON object')
    return value


def validate(dd, scene, events, candidate, writer=False):
    errors = []
    if not isinstance(dd, dict):
        return ['no dated_debrief object']
    if (writer or 'candidate_id' in dd) and dd.get('candidate_id') != candidate:
        errors.append('candidate_id does not match destination')
    aids = {a['id'] for a in scene['assumptions']}

    def text(value, label, status=False):
        if not isinstance(value, str) or not value.strip():
            errors.append(f'{label}: expected nonempty text')
        elif len(value.split()) > 45:
            errors.append(f'{label}: exceeds 45 words')
        elif status and not STATUS.match(value):
            errors.append(f'{label}: lacks status word')

    baseline = dd.get('baseline')
    if not isinstance(baseline, dict):
        errors.append('baseline: expected object')
    else:
        text(baseline.get('narrative'), 'baseline narrative')
        checks = baseline.get('checks')
        if not isinstance(checks, dict):
            errors.append('baseline checks: expected object')
        else:
            if set(checks) != aids:
                errors.append('baseline checks must cover exactly the assumption ids')
            for aid, value in checks.items():
                text(value, f'baseline {aid}', status=True)
    updates = dd.get('updates')
    if not isinstance(updates, list):
        return errors + ['updates: expected list']
    if not 4 <= len(updates) <= 8:
        errors.append('expected 4–8 updates')
    for i, update in enumerate(updates):
        label = f'update {i}'
        if not isinstance(update, dict):
            errors.append(f'{label}: expected object')
            continue
        ids = update.get('event_ids')
        if not isinstance(ids, list) or not ids or not all(isinstance(eid, str) for eid in ids):
            errors.append(f'{label}: expected nonempty list of event ids')
        else:
            if len(ids) != len(set(ids)):
                errors.append(f'{label}: duplicate event id')
            for eid in ids:
                if eid not in events:
                    errors.append(f'{label}: unknown event {eid}')
                    continue
                event = events[eid]
                try:
                    last_day(event.get('date'))
                    last_day((event.get('source') or {}).get('published'))
                except (ValueError, TypeError, AttributeError) as exc:
                    errors.append(f'{label} event {eid}: {exc}')
        checks = update.get('checks', {})
        if not isinstance(checks, dict):
            errors.append(f'{label}: checks must be an object')
        else:
            for aid, value in checks.items():
                if aid not in aids:
                    errors.append(f'{label}: unknown assumption {aid}')
                text(value, f'{label} {aid}', status=True)
        if 'narrative' in update:
            text(update['narrative'], f'{label} narrative')
        if not checks and not update.get('narrative'):
            errors.append(f'{label}: no narrative or checks')
    return errors


def atomic_write(path, text):
    """Replace one destination only after a complete, flushed temporary write."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix='.' + path.name + '.', suffix='.tmp', delete=False) as f:
            temporary = Path(f.name)
            os.chmod(temporary, path.stat().st_mode & 0o777)
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def merge(root=ROOT, check_only=False):
    path = root / 'cases/scenes.json'
    problems, pending = [], []
    try:
        scenes = read_object(path)
        if not isinstance(scenes.get('scenes'), dict):
            raise ValueError('scenes must be an object')
    except (OSError, ValueError) as exc:
        return [f'{path}: {exc}'], 0
    unknown = {f.parent.name for f in (root / 'cases').glob('*/dated_debrief.json')} - set(scenes['scenes'])
    problems.extend(f'{cid}: unknown candidate writer input' for cid in sorted(unknown))
    for cid, scene in scenes['scenes'].items():
        source = root / 'cases' / cid / 'dated_debrief.json'
        try:
            dd = read_object(source) if source.exists() else scene.get('dated_debrief')
            aftermath = read_object(root / 'cases' / cid / 'aftermath.json')
            events = {e['id']: e for e in aftermath['events']}
            errors = validate(dd, scene, events, cid, writer=source.exists())
            problems.extend(f'{cid}: {error}' for error in errors)
            if source.exists() and not errors:
                pending.append(source)
                scene['dated_debrief'] = {'baseline': dd['baseline'], 'updates': dd['updates']}
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            problems.append(f'{cid}: invalid input: {exc}')
    if problems or check_only or not pending:
        return problems, 0
    try:
        atomic_write(path, json.dumps(scenes, indent=2, ensure_ascii=False) + '\n')
    except OSError as exc:
        return [f'save failed; writer inputs retained: {exc}'], 0
    for source in pending:
        try:
            source.unlink()
        except OSError as exc:
            problems.append(f'{source}: merged successfully, cleanup failed; rerun safely: {exc}')
    return problems, len(pending)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    problems, merged = merge(check_only=args.check_only)
    print(f'merged {merged}; problems: {len(problems)}')
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
