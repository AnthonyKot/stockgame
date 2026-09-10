#!/usr/bin/env python3
"""Build a campaign manifest and dated price slices (idea 1, first milestone: three stories, long and skip).

Reads research/selected.json, research/prices/<ticker>.json (raw Yahoo caches), research/prices/SPY.json (the session
calendar: SPY trades every New York session) and research/prices/BTC-USD.json (UTC daily bars).
Writes site/data/campaigns/<campaign_id>/manifest.json and prices/<instrument>/<year>.json.

Conventions written into the manifest (the five long/skip decisions, settled by default on 2026-09-10):
  start 2018-02-15 09:00 New York; end = first session on or after the last offered exit; Bitcoin marked at the last
  completed UTC daily close before the timestamp; same-timestamp order = exits, then entries, then dividends, then close
  marks; dividends as ex-date cash (versioned convention 'exdate-cash-v1'); baseline = same cash plus the same Bitcoin.
Instruments are referred to by the case's opaque id, never by ticker, because the campaign page is masked until a
position closes. Price levels are un-adjusted for later splits exactly as scripts/build_bundles.py does.
Run: python3 scripts/build_campaign.py [--campaign proto-3]
"""
import argparse, hashlib, json, sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
SALT = 'stockgame-mvp-1'
NY = ZoneInfo('America/New_York')

CAMPAIGNS = {
    'proto-3': {
        'title': 'Three stories, one account',
        'scenes': ['clinical-nktr-2018', 'clinical-mdgl-2018', 'growth-008'],   # Nektar, Madrigal, JPMorgan, in cutoff order
        'actions': ['buy', 'skip'],
    },
}
RULES = {
    'rules_version': 'long-skip-r1',
    'starting_cash_usd': 100000, 'starting_btc': 1,
    'sizes_pct': [5, 10, 20], 'horizons_years': [1, 3, 5],
    'slippage_per_side': 0.001, 'cash_yield': 0.0,
    'allocation': 'percentage of marked equity at commitment, frozen as a dollar budget; a long buys fractional shares within the budget at the entry open including slippage',
    'entry': 'first session open on or after the cutoff date (cutoffs are 09:00 New York, before the open)',
    'exit': 'first session open on or after the calendar anniversary of the entry session; 29 February maps to 28 February',
    'dividends': 'exdate-cash-v1: cash credited on the ex-date for shares held, at the session close phase; no payment-date lag',
    'btc_mark': 'last completed UTC daily close strictly before the timestamp date',
    'stock_mark': 'last session close before the timestamp (pre-open phase) or on it (closed phase)',
    'same_timestamp_order': ['scheduled exits at the open', 'pending entries at the open', 'ex-date dividends', 'close marks'],
    'baseline': 'the same starting cash and Bitcoin held untouched, valued at the same ending timestamp',
    'not_in_this_version': ['short', 'stop loss', 'take profit', 'manual exits', 'Bitcoin trading', 'payment-date dividends', 'borrow'],
}


def opaque(cid):
    return hashlib.sha1((SALT + cid).encode()).hexdigest()[:10]


def load_yahoo(ticker):
    r = json.loads((ROOT / 'research' / 'prices' / f'{ticker}.json').read_text())['chart']['result'][0]
    z = ZoneInfo(r['meta'].get('exchangeTimezoneName', 'America/New_York'))
    q = r['indicators']['quote'][0]; ev = r.get('events', {})
    splits = sorted([(datetime.fromtimestamp(v['date'], z).date(), v['numerator'] / v['denominator'], v['splitRatio']) for v in ev.get('splits', {}).values()])
    divs = sorted([(datetime.fromtimestamp(v['date'], z).date(), v['amount']) for v in ev.get('dividends', {}).values()])
    bars = []
    for t, o, c in zip(r['timestamp'], q['open'], q['close']):
        if None in (o, c) or c <= 0 or o <= 0:
            continue
        d = datetime.fromtimestamp(t, z).date()
        f = 1.0
        for sd, ratio, _ in splits:
            if sd > d:
                f *= ratio          # undo splits that happened after this bar, as build_bundles.py does
        bars.append({'d': d, 'o': round(o * f, 4), 'c': round(c * f, 4)})
    return bars, splits, divs, z.key


def anniversary(d, years):
    try:
        return d.replace(year=d.year + years)
    except ValueError:            # 29 February
        return d.replace(year=d.year + years, day=28)


def first_session_on_or_after(sessions, d):
    for s in sessions:
        if s >= d:
            return s
    return None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--campaign', default='proto-3'); args = ap.parse_args()
    spec = CAMPAIGNS[args.campaign]
    sel = {r['id']: r for r in json.loads((ROOT / 'research' / 'selected.json').read_text())['selected']}
    spy_bars, _, _, _ = load_yahoo('SPY')
    sessions = [b['d'] for b in spy_bars]
    coverage_end = sessions[-1]
    btc = json.loads((ROOT / 'research' / 'prices' / 'BTC-USD.json').read_text())['chart']['result'][0]
    btc_bars = [{'d': datetime.fromtimestamp(t, timezone.utc).date(), 'c': round(c, 2)} for t, c in zip(btc['timestamp'], btc['indicators']['quote'][0]['close']) if c]

    scenes, instruments, problems = [], {}, []
    for i, cid in enumerate(spec['scenes']):
        r = sel[cid]; oid = opaque(cid); ticker = r['ticker']
        cutoff_dt = datetime.fromisoformat(r['proposed_cutoff']).astimezone(NY)
        cutoff_date = cutoff_dt.date()
        bars, splits, divs, tz = load_yahoo(ticker)
        entry = first_session_on_or_after(sessions, cutoff_date)
        if cutoff_dt.time() >= datetime.strptime('09:30', '%H:%M').time():
            problems.append(f'{cid}: cutoff {cutoff_dt} is not before the open; entry convention assumes a pre-open cutoff')
        bar_dates = {b['d'] for b in bars}
        if entry not in bar_dates:
            problems.append(f'{cid}: no {ticker} bar on entry session {entry}')
        horizons = {}
        for y in RULES['horizons_years']:
            x = first_session_on_or_after(sessions, anniversary(entry, y))
            if x is None or x > coverage_end or x not in bar_dates:
                continue                       # not offered: exit beyond coverage or no bar
            horizons[str(y)] = str(x)
        if str(r.get('horizon_years') or r.get('horizon')) not in horizons:
            problems.append(f'{cid}: default horizon {r.get("horizon_years") or r.get("horizon")}y is not offerable')
        scenes.append({'index': i, 'opaque_id': oid, 'cutoff': cutoff_dt.isoformat(), 'cutoff_date': str(cutoff_date),
                       'entry_session': str(entry), 'horizons': horizons, 'default_horizon': str(r.get('horizon_years') or r.get('horizon')),
                       'data': f'../{oid}/'})
        instruments[oid] = {'kind': 'stock', 'timezone': tz, 'bars': bars, 'divs': divs,
                            'splits_in_coverage': [{'date': str(d), 'ratio': s} for d, _, s in splits if d >= cutoff_date],
                            'first_bar': str(bars[0]['d']), 'last_bar': str(bars[-1]['d'])}
    last_exit = max(date.fromisoformat(x) for s in scenes for x in s['horizons'].values())
    end = first_session_on_or_after(sessions, last_exit)
    start = datetime.fromisoformat(scenes[0]['cutoff'])
    if problems:
        print('\n'.join('AUDIT: ' + p for p in problems)); sys.exit(1)

    out = ROOT / 'site' / 'data' / 'campaigns' / args.campaign
    (out / 'prices').mkdir(parents=True, exist_ok=True)
    # dated slices: one file per instrument per calendar year (a coarse slice; the page loads only years up to its clock)
    window_start = start.date() - timedelta(days=400)     # a year of pre-cutoff history for the first scene's chart context
    for oid, ins in instruments.items():
        years = {}
        for b in ins['bars']:
            if window_start <= b['d'] <= end:
                years.setdefault(b['d'].year, {'bars': [], 'dividends': []})['bars'].append({'d': str(b['d']), 'o': b['o'], 'c': b['c']})
        for d, a in ins['divs']:
            if window_start <= d <= end and d.year in years:
                years[d.year]['dividends'].append({'d': str(d), 'a': a})
        (out / 'prices' / oid).mkdir(exist_ok=True)
        for y, payload in years.items():
            (out / 'prices' / oid / f'{y}.json').write_text(json.dumps(payload, separators=(',', ':')))
        ins['years'] = sorted(years)
    years = {}
    for b in btc_bars:
        if window_start <= b['d'] <= end + timedelta(days=1):
            years.setdefault(b['d'].year, []).append({'d': str(b['d']), 'c': b['c']})
    (out / 'prices' / 'BTC').mkdir(exist_ok=True)
    for y, payload in years.items():
        (out / 'prices' / 'BTC' / f'{y}.json').write_text(json.dumps({'bars': payload}, separators=(',', ':')))

    content_hash = hashlib.sha1(json.dumps({'scenes': scenes, 'rules': RULES}, sort_keys=True).encode()).hexdigest()[:10]
    manifest = {
        'campaign_id': args.campaign, 'title': spec['title'], 'content_version': content_hash, 'built_at': datetime.now(timezone.utc).isoformat(),
        'start_at': start.isoformat(), 'start_date': str(start.date()), 'end_session': str(end), 'coverage_end': str(coverage_end),
        'actions': spec['actions'], 'rules': RULES,
        'calendar': [str(s) for s in sessions if window_start <= s <= end],
        'calendar_source': 'SPY session dates from research/prices/SPY.json (SPY trades every New York session)',
        'btc': {'instrument': 'BTC', 'source': 'research/prices/BTC-USD.json, Yahoo BTC-USD, UTC daily bars', 'years': sorted(years), 'first_bar': str(btc_bars[0]['d']), 'last_bar': str(btc_bars[-1]['d'])},
        'instruments': {oid: {k: v for k, v in ins.items() if k not in ('bars', 'divs')} for oid, ins in instruments.items()},
        'scenes': scenes,
        'limits': ['Static files: price slices are per calendar year, so the current year is readable ahead of the clock. Outcome and reveal files for a scene are fetched only when its position closes; they are not access-controlled.',
                   'Vendor daily bars; dividends from vendor events on ex-dates; not a verified corporate-action ledger.'],
    }
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    print(f"{args.campaign}: start {manifest['start_date']} end {manifest['end_session']} coverage {coverage_end}; scenes:")
    for s in scenes:
        print(f"  {s['index']} {s['opaque_id']} cutoff {s['cutoff_date']} entry {s['entry_session']} horizons {s['horizons']} default {s['default_horizon']}y")
    print(f"  BTC bars {len(btc_bars)} ({manifest['btc']['first_bar']} to {manifest['btc']['last_bar']}); calendar sessions in window {len(manifest['calendar'])}")


if __name__ == '__main__':
    main()
