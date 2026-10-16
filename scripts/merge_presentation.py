#!/usr/bin/env python3
"""Merge cases/<id>/presentation.json (writer output per cases/SNAPSHOT_PRESENTATION_BRIEF.md) into
cases/<id>/player.json as financial_snapshot.presentation, after validating: every metric label matches a headline
tile exactly, group indices are in range, 4-6 metrics, word limits, no outcome words. All target player.json files
are staged to flushed sibling temp files and committed with multi-file rollback before any presentation.json inputs
are deleted. Run: python3 scripts/merge_presentation.py [--check-only]"""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
BANNED = re.compile(r'\b(cheap|expensive|undervalued|overvalued|will (rise|fall)|turned out|in hindsight|later)\b', re.I)


def read_object(path):
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError('expected a JSON object')
    return value


def validate(pr, player, candidate):
    errors = []
    if not isinstance(pr, dict):
        return ['no presentation object']
    if 'candidate_id' in pr and pr.get('candidate_id') != candidate:
        errors.append('candidate_id does not match destination')
    snapshot = player.get('financial_snapshot')
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get('headline'), list):
        return errors + ['financial_snapshot.headline: expected list']
    labels = [h['label'] for h in snapshot['headline'] if isinstance(h, dict) and 'label' in h]
    existing = snapshot.get('presentation')
    existing_mode = existing.get('valuation_mode') if isinstance(existing, dict) else None
    mode = pr.get('valuation_mode', existing_mode)
    if ('valuation_mode' in pr or mode is not None) and mode not in ('revenue', 'pipeline', 'bank'):
        errors.append(f'invalid valuation_mode {mode!r}')
    metrics = pr.get('metrics')
    if not isinstance(metrics, list):
        errors.append('metrics: expected list')
        metrics = []
    elif not (4 <= len(metrics) <= 6):
        errors.append(f'{len(metrics)} metrics')
    for i, m in enumerate(metrics):
        if not isinstance(m, dict):
            errors.append(f'metric {i}: expected object')
            continue
        if m.get('metric') not in labels:
            errors.append(f'metric {i} label not found: {m.get("metric")!r}')
        context = m.get('context')
        if not isinstance(context, str) or not context.strip():
            errors.append(f'metric {i} has no context')
        elif len(context.split()) > 35:
            errors.append(f'metric {i} context {len(context.split())} words')
        if isinstance(context, str) and BANNED.search(context):
            errors.append(f'metric {i} context has a banned word')
        if not isinstance(m.get('label'), str) or not m.get('label').strip():
            errors.append(f'metric {i} has no label')
    groups = pr.get('groups')
    if not isinstance(groups, list):
        errors.append('groups: expected list')
        groups = []
    elif not (2 <= len(groups) <= 3):
        errors.append(f'{len(groups)} groups')
    used = []
    for i, g in enumerate(groups):
        if not isinstance(g, dict) or not isinstance(g.get('title'), str) or not g.get('title').strip() or not isinstance(g.get('metrics'), list):
            errors.append(f'group {i}: expected title and metrics list')
            continue
        used.extend(g['metrics'])
    valid_indices = True
    for j in used:
        if not isinstance(j, int) or isinstance(j, bool) or not (0 <= j < len(metrics)):
            errors.append(f'group index {j} out of range')
            valid_indices = False
    if valid_indices and sorted(used) != list(range(len(metrics))):
        errors.append(f'groups do not use each metric exactly once: {sorted(used)}')
    intro = pr.get('intro')
    vctx = pr.get('valuation_context')
    if not isinstance(intro, str) or not intro.strip():
        errors.append('intro: expected nonempty text')
    if not isinstance(vctx, str) or not vctx.strip():
        errors.append('valuation_context: expected nonempty text')
    elif len(vctx.split()) > 45:
        errors.append(f'valuation_context {len(vctx.split())} words')
    if (isinstance(vctx, str) and BANNED.search(vctx)) or (isinstance(intro, str) and BANNED.search(intro)):
        errors.append('intro/valuation_context has a banned word')
    return errors


def stage_temp(path, text):
    """Write and fsync a sibling temporary file ready for os.replace."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix='.' + path.name + '.', suffix='.tmp', delete=False) as f:
            temporary = Path(f.name)
            os.chmod(temporary, path.stat().st_mode & 0o777)
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        return temporary
    except Exception:
        if temporary is not None and temporary.exists():
            temporary.unlink()
        raise


def atomic_write(path, text):
    """Replace one destination only after a complete, flushed temporary write."""
    temporary = stage_temp(path, text)
    try:
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def commit_batch(ready):
    """Two-phase multi-file commit: stage all sibling temp files, replace all targets, or roll back on error."""
    staged = []
    committed = []
    try:
        for source, pj, player, original_text in ready:
            text = json.dumps(player, indent=2, ensure_ascii=False) + '\n'
            staged.append((source, pj, stage_temp(pj, text), original_text))
        for source, pj, temporary, original_text in staged:
            os.replace(temporary, pj)
            committed.append((pj, original_text))
    except OSError as exc:
        rollback_errors = []
        for pj, original_text in reversed(committed):
            try:
                atomic_write(pj, original_text)
            except OSError as rb_exc:
                rollback_errors.append(f'{pj}: rollback failed: {rb_exc}')
        if rollback_errors:
            raise OSError(f'{exc}; ' + '; '.join(rollback_errors)) from exc
        raise
    finally:
        for _, _, temporary, _ in staged:
            if temporary.exists():
                try:
                    temporary.unlink()
                except OSError:
                    pass


def merge(root=ROOT, check_only=False):
    cases_dir = root / 'cases'
    problems, ready = [], []
    known = {f.parent.name for f in cases_dir.glob('*/player.json')}
    unknown = {f.parent.name for f in cases_dir.glob('*/presentation.json')} - known
    problems.extend(f'{cid}: unknown candidate writer input' for cid in sorted(unknown))
    for cid in sorted(known):
        pj = cases_dir / cid / 'player.json'
        source = cases_dir / cid / 'presentation.json'
        try:
            original_text = pj.read_text()
            player = json.loads(original_text)
            if not isinstance(player, dict):
                raise ValueError('expected a JSON object')
            snapshot = player.get('financial_snapshot') or {}
            stored = snapshot.get('presentation') if isinstance(snapshot, dict) else None
            if not source.exists() and stored is None:
                continue
            pr = read_object(source) if source.exists() else stored
            errors = validate(pr, player, cid)
            problems.extend(f'{cid}: {error}' for error in errors)
            if source.exists() and not errors:
                existing_mode = stored.get('valuation_mode') if isinstance(stored, dict) else None
                mode = pr.get('valuation_mode', existing_mode)
                presentation = {k: pr[k] for k in ('intro', 'groups', 'metrics', 'valuation_context')}
                if mode is not None:
                    presentation['valuation_mode'] = mode
                player['financial_snapshot']['presentation'] = presentation
                ready.append((source, pj, player, original_text))
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            problems.append(f'{cid}: invalid input: {exc}')
    if problems or check_only or not ready:
        return problems, 0
    try:
        commit_batch(ready)
    except OSError as exc:
        return [f'save failed; writer inputs retained: {exc}'], 0
    for source, _, _, _ in ready:
        try:
            source.unlink()
        except OSError as exc:
            problems.append(f'{source}: merged successfully, cleanup failed; rerun safely: {exc}')
    return problems, len(ready)


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
