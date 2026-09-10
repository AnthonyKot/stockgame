"""Build per-case site bundles from cached prices and the writers' player/evidence files.

Outputs under site/data/<opaque_id>/:
  market.json   pre-cutoff bars (levels un-adjusted for later splits), returns, SPY comparison  [player]
  sheet.json    masked player sheet: player.json minus the transparent block and minus URLs    [player]
  reveal.json   transparent block, source URLs, evidence excerpts                              [after commit]
  outcome.json  fills under the game contract, daily path, dividends, per-action results       [after commit]
site/data/index.json lists the cases with opaque ids only.
Run: python3 scripts/build_bundles.py
"""
import hashlib, json, copy, re, sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site' / 'data'
SALT = 'stockgame-mvp-1'
SLIPPAGE = 0.001          # 10 bp per transaction, game assumption
BORROW_ANNUAL = 0.05      # simulated short borrow fee, game assumption
START_EQUITY = 100_000.0
SIZES = [0.05, 0.10, 0.20]
CHART_YEARS = 3           # bars shipped before the cutoff

def opaque(cid):
    return hashlib.sha1((SALT + cid).encode()).hexdigest()[:10]

def load_bars(ticker):
    r = json.loads((ROOT / 'research' / 'prices' / f'{ticker}.json').read_text())['chart']['result'][0]
    z = ZoneInfo(r['meta'].get('exchangeTimezoneName', 'America/New_York'))
    q = r['indicators']['quote'][0]
    adj = r['indicators']['adjclose'][0]['adjclose']
    ev = r.get('events', {})
    splits = sorted([(datetime.fromtimestamp(v['date'], z).date(), v['numerator'] / v['denominator'], v['splitRatio'])
                     for v in ev.get('splits', {}).values()])
    divs = sorted([(datetime.fromtimestamp(v['date'], z).date(), v['amount']) for v in ev.get('dividends', {}).values()])
    bars = []
    for t, o, h, l, c, v, a in zip(r['timestamp'], q['open'], q['high'], q['low'], q['close'], q['volume'], adj):
        if None in (o, c) or c <= 0 or o <= 0:
            continue
        d = datetime.fromtimestamp(t, z).date()
        # Yahoo levels are adjusted for every later split; undo splits that happened after this bar
        f = 1.0
        for sd, ratio, _ in splits:
            if sd > d:
                f *= ratio
        bars.append({'date': d, 'open': o * f, 'high': (h or c) * f, 'low': (l or c) * f, 'close': c * f,
                     'volume': v, 'adjclose': a, 'unadjust_factor': f})
    return bars, splits, divs

def first_on_or_after(bars, day):
    for i, b in enumerate(bars):
        if b['date'] >= day:
            return i
    return None

def anniversary(day, years):
    try:
        return day.replace(year=day.year + years)
    except ValueError:
        return day.replace(year=day.year + years, day=28)

def market_view(bars, spy, cutoff_day):
    last = max(i for i, b in enumerate(bars) if b['date'] < cutoff_day)  # last complete session before the 09:00 cutoff
    start = cutoff_day - timedelta(days=365 * CHART_YEARS + 5)
    window = [b for b in bars[:last + 1] if b['date'] >= start]
    closes = {b['date']: b['close'] for b in bars[:last + 1]}
    ref = bars[last]
    def ret(days):
        target = ref['date'] - timedelta(days=days)
        prior = [b for b in bars[:last + 1] if b['date'] <= target]
        return round(ref['close'] / prior[-1]['close'] - 1, 4) if prior else None
    hi = max(b['close'] for b in bars[max(0, last - 251):last + 1])
    spy_map = {b['date']: b['close'] for b in spy}
    spy_win = [(b['date'], spy_map.get(b['date'])) for b in window]
    return {
        'last_eligible_session': str(ref['date']), 'last_close': round(ref['close'], 4), 'last_volume': ref['volume'],
        'returns': {'1m': ret(30), '3m': ret(91), '12m': ret(365)},
        'distance_from_trailing_252_high': round(ref['close'] / hi - 1, 4),
        'spy_returns': {k: (round(spy_map[ref['date']] / [s for d_, s in spy_win if d_ <= ref['date'] - timedelta(days=n)][-1] - 1, 4)
                             if [s for d_, s in spy_win if d_ <= ref['date'] - timedelta(days=n)] and spy_map.get(ref['date']) else None)
                        for k, n in (('1m', 30), ('3m', 91), ('12m', 365))},
        'bars': [{'d': str(b['date']), 'o': round(b['open'], 4), 'c': round(b['close'], 4), 'v': b['volume']} for b in window],
        'spy': [{'d': str(d_), 'c': round(s, 4)} for d_, s in spy_win if s],
        'level_note': 'Levels are historical trading prices: vendor closes un-adjusted for splits after each bar. No dividend adjustment. Chart ends at the last complete session before the cutoff.',
        'coverage_note': f'{len(window)} sessions shown, from {window[0]["date"]} to {ref["date"]}.'
    }

def outcome(bars, spy, divs, cutoff_day, years, ticker, spy_divs=()):
    ei = first_on_or_after(bars, cutoff_day)
    entry = bars[ei]
    if (entry['date'] - cutoff_day).days > 7:
        raise ValueError('no entry session within 7 days of cutoff')
    target = anniversary(entry['date'], years)
    xi = first_on_or_after(bars, target)
    if xi is None or (bars[xi]['date'] - target).days > 7:
        raise ValueError('no exit session near anniversary')
    exit_ = bars[xi]
    path = bars[ei:xi + 1]
    window_divs = [(d_, a) for d_, a in divs if entry['date'] < d_ <= exit_['date']]
    div_total = sum(a for _, a in window_divs)
    spy_map = {b['date']: b for b in spy}
    spy_entry, spy_exit = spy_map[entry['date']]['open'], spy_map[exit_['date']]['open']
    spy_div_total = sum(a for d_, a in spy_divs if entry['date'] < d_ <= exit_['date'])
    spy_price_ret = spy_exit / spy_entry - 1
    spy_ret = (spy_exit + spy_div_total) / spy_entry - 1   # total return, fixed shares, dividends held as cash, no costs
    days = (exit_['date'] - entry['date']).days
    # long: buy at open*(1+s), sell at open*(1-s), receive dividends
    long_ret = (exit_['open'] * (1 - SLIPPAGE) + div_total) / (entry['open'] * (1 + SLIPPAGE)) - 1
    # short: sell at open*(1-s), cover at open*(1+s), pay dividends, pay borrow fee on daily short market value
    borrow = sum(b['close'] * BORROW_ANNUAL / 365 * ((path[i + 1]['date'] - b['date']).days if i + 1 < len(path) else 0)
                 for i, b in enumerate(path))
    short_pnl_per_share = entry['open'] * (1 - SLIPPAGE) - exit_['open'] * (1 + SLIPPAGE) - div_total - borrow
    short_ret = short_pnl_per_share / entry['open']
    peak, dd = path[0]['close'], 0.0
    for b in path:
        peak = max(peak, b['close']); dd = min(dd, b['close'] / peak - 1)
    trough, ru = path[0]['close'], 0.0
    for b in path:
        trough = min(trough, b['close']); ru = max(ru, b['close'] / trough - 1)
    results = {'skip': {'size': 0, 'portfolio_return': 0.0, 'end_equity': START_EQUITY}}
    for s in SIZES:
        results[f'buy_{int(s*100)}'] = {'size': s, 'position_return': round(long_ret, 4), 'portfolio_return': round(s * long_ret, 4), 'end_equity': round(START_EQUITY * (1 + s * long_ret), 2)}
        results[f'short_{int(s*100)}'] = {'size': s, 'position_return': round(short_ret, 4), 'portfolio_return': round(s * short_ret, 4), 'end_equity': round(START_EQUITY * (1 + s * short_ret), 2)}
    def sess(n):
        return round(path[n]['close'] / entry['open'] - 1, 4) if n < len(path) else None
    return {
        'contract': {'decision': 'at the cutoff, 09:00 America/New_York', 'entry': 'next regular-session open on/after the cutoff', 'exit': 'first regular-session open on/after the calendar anniversary of the entry date; leap day clamps to Feb 28',
                     'slippage_bp_per_side': 10, 'short_borrow_fee_annual': BORROW_ANNUAL, 'idle_cash_yield': 0.0, 'start_equity': START_EQUITY, 'sizes': SIZES,
                     'note': 'Game assumptions, not a reconstruction of any historical broker. Short is a simulated exposure; no recall or margin call modelled in the MVP.'},
        'entry': {'date': str(entry['date']), 'open': round(entry['open'], 4)}, 'exit': {'date': str(exit_['date']), 'open': round(exit_['open'], 4)},
        'calendar_days': days, 'dividends_per_share': [{'ex_date': str(d_), 'amount': a} for d_, a in window_divs], 'dividend_total_per_share': round(div_total, 4),
        'borrow_fee_per_share': round(borrow, 4), 'split_or_spinoff_in_window': [],
        'price_return_open_to_open': round(exit_['open'] / entry['open'] - 1, 4), 'long_total_return_after_costs': round(long_ret, 4), 'short_total_return_after_costs': round(short_ret, 4),
        'spy_open_to_open_return': round(spy_ret, 4), 'spy_price_return': round(spy_price_ret, 4), 'spy_dividend_total_per_share': round(spy_div_total, 4),
        'benchmark_convention': 'SPY bought at the same entry open and sold at the same exit open, fixed shares, cash dividends in (entry, exit] added, no costs. Stock long return uses the same dates and dividend rule plus slippage.', 'max_drawdown_from_entry_path': round(dd, 4), 'max_runup_from_entry_path': round(ru, 4),
        'session_returns_vs_entry_open': {'5': sess(5), '21': sess(21), '63': sess(63), '126': sess(126)},
        'results': results,
        'path': [{'d': str(b['date']), 'c': round(b['close'], 4)} for b in path],
        'spy_path': [{'d': str(b['date']), 'c': round(spy_map[b['date']]['close'], 4)} for b in path if b['date'] in spy_map],
        'data_note': 'Vendor daily bars (Yahoo chart API, cached 2026-09-09). Dividends and splits from vendor events. Not a verified corporate-action ledger.'
    }

REPL = {}   # term -> replacement, filled per case from selected.json mask_terms dicts

def mask_names(obj, names, alias):
    """Replace issuer names, ticker and per-case mask terms in every string; partial masking, other brand names stay."""
    if not names:
        return obj
    pat = re.compile(r'\b(' + '|'.join(re.escape(n) for n in sorted(names, key=len, reverse=True)) + r')(\'s)?\b')
    def rep(m):
        base = REPL.get(m.group(1), 'the company')
        return base if not m.group(2) else (base + "'s" if not base.endswith('s') else base + "'")
    if isinstance(obj, dict):
        return {k: mask_names(v, names, alias) for k, v in obj.items()}
    if isinstance(obj, list):
        return [mask_names(x, names, alias) for x in obj]
    if isinstance(obj, str):
        s = obj
        for n in names:
            if n.isupper() and 2 <= len(n) <= 5:   # ticker inside a drug code, e.g. NKTR-214 -> candidate-214
                s = re.sub(r'\b' + re.escape(n) + r'-(\d)', r'candidate-\1', s)
        return pat.sub(rep, s)
    return obj

def issuer_names(issuer, ticker):
    base = re.sub(r',?\s*(Inc\.?|Corp\.?|Corporation|Co\.?|Company|& Co\.?|Ltd\.?|plc)\s*$', '', issuer, flags=re.I).strip()
    base = re.sub(r'^The\s+', '', base, flags=re.I).strip()
    names = {issuer, base, ticker}
    first = base.split(' ')[0]
    if len(first) > 4 and first.lower() not in ('first', 'target', 'general', 'the'):
        names.add(first)
    if base.lower().startswith('first solar'):
        names.add('First Solar')
    if base.lower().startswith('jpmorgan'):
        names.update({'JPMorgan', 'JPMorgan Chase', 'J.P. Morgan', 'Chase'})
    if base.lower().startswith('target'):
        names.add('Target Corporation'); names.add('Target')
    return {n for n in names if n}


def to_millions(v, unit):
    u = str(unit or '')
    if v is None: return None
    if 'billion' in u.lower(): return v * 1000
    if 'thousand' in u.lower(): return v / 1000
    if u == 'USD': return v / 1e6
    return v

def valuation(cid, p, mv, cutoff_day):
    """Derived valuation at the cutoff: shares (XBRL, latest filed on/before cutoff) x last eligible close,
    net cash/debt and revenue from the writer's headline tiles or XBRL annual revenue. Every input carries its date."""
    x = json.loads((ROOT / 'cases' / cid / 'xbrl-facts.json').read_text())['facts']
    cut = str(cutoff_day)
    def latest(tag, instant=True):
        rows = [r for r in x.get(tag, {}).get('rows', []) if r['filed'] <= cut and (not r.get('start') if instant else r.get('start'))]
        return rows[-1] if rows else None
    inputs, caveats = [], []
    sh = latest('CommonStockSharesOutstanding'); basis = 'shares outstanding'
    if not sh:
        sh = latest('WeightedAverageNumberOfDilutedSharesOutstanding', instant=False); basis = 'weighted-average diluted shares (proxy)'
    out = {'status': 'derived', 'as_of_price_date': mv['last_eligible_session'], 'last_close': mv['last_close']}
    if not sh:
        return {'status': 'missing', 'reason': 'no share count in the XBRL facts filed before the cutoff'}
    stale = (cutoff_day - date.fromisoformat(sh['end'])).days > 400
    shares_m = sh['value'] / 1e6
    inputs.append({'name': 'shares', 'value_millions': round(shares_m, 2), 'basis': basis, 'as_of': sh['end'], 'filed': sh['filed'], 'source': sh['accn']})
    if stale: caveats.append(f"share count is from {sh['end']}, more than a year before the cutoff; later issuance or buybacks are not reflected")
    mcap = shares_m * mv['last_close']
    out['market_cap_musd'] = round(mcap, 1)
    out['market_cap_formula'] = f"{round(shares_m,1)}m shares ({sh['end']}) x ${mv['last_close']} close ({mv['last_eligible_session']})"
    # cash and debt: prefer the writer's curated tiles
    tiles = p.get('financial_snapshot', {}).get('headline', [])
    def tile(pred):
        for h in tiles:
            if pred(h['label'].lower()) and isinstance(h.get('value'), (int, float)): return h
    is_bank = 'bank' in p.get('masked', {}).get('sector', '').lower() or tile(lambda l: 'deposits' in l) is not None
    net = tile(lambda l: 'net cash' in l or 'net debt' in l or ('cash' in l and 'debt' in l and 'securities' not in l))
    cash = tile(lambda l: 'cash' in l and 'net' not in l and 'flow' not in l and 'outflow' not in l and 'burn' not in l and not ('debt' in l and 'securities' not in l))
    debt = tile(lambda l: ('debt' in l or 'borrowing' in l) and 'net' not in l and 'securities' not in l and 'cash' not in l)
    net_cash = None
    if is_bank:
        caveats.append('bank: enterprise value and net cash are not meaningful measures; deposits and loans are the balance-sheet view')
    elif net:
        net_cash = to_millions(net['value'], net['unit']); inputs.append({'name': 'net cash (writer tile: ' + net['label'] + ')', 'value_millions': round(net_cash, 1), 'as_of': net.get('period'), 'source': net.get('source_ids')})
        if 'net debt' in net['label'].lower(): net_cash = -net_cash
    elif cash:
        c = to_millions(cash['value'], cash['unit']); inputs.append({'name': 'cash and investments (writer tile)', 'value_millions': round(c, 1), 'as_of': cash.get('period'), 'source': cash.get('source_ids')})
        if debt:
            d = to_millions(debt['value'], debt['unit']); inputs.append({'name': 'debt (writer tile)', 'value_millions': round(d, 1), 'as_of': debt.get('period'), 'source': debt.get('source_ids')})
        else:
            xd = latest('LongTermDebt')
            if not xd:
                parts = [latest(tg) for tg in ('LongTermDebtNoncurrent', 'LongTermDebtCurrent', 'DebtCurrent')]
                parts = [q for q in parts if q]
                xd = {'value': sum(q['value'] for q in parts), 'end': max(q['end'] for q in parts), 'accn': ','.join(sorted({q['accn'] for q in parts}))} if parts else None
            if xd:
                d = xd['value'] / 1e6; inputs.append({'name': 'debt (XBRL)', 'value_millions': round(d, 1), 'as_of': xd['end'], 'source': xd['accn']})
            else:
                d = 0.0; caveats.append('no debt figure in the packet tiles or XBRL facts; debt treated as zero, check the balance sheet rows')
        net_cash = c - d
    if net_cash is not None:
        out['net_cash_musd'] = round(net_cash, 1); out['enterprise_value_musd'] = round(mcap - net_cash, 1)
    else:
        caveats.append('no cash/debt figures in the packet tiles; enterprise value not derived')
    # trailing annual revenue from XBRL (duration ~ 1 year)
    rev = None
    for tag in ('Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet'):
        rows = [r for r in x.get(tag, {}).get('rows', []) if r['filed'] <= cut and r.get('start') and 330 <= (date.fromisoformat(r['end']) - date.fromisoformat(r['start'])).days <= 380]
        if rows and (rev is None or rows[-1]['end'] > rev['end']): rev = rows[-1]
    if is_bank:
        out['annual_revenue_musd'] = None; caveats.append('revenue multiples not applied to a bank')
    elif rev and rev['value'] > 0:
        rv = rev['value'] / 1e6; inputs.append({'name': 'annual revenue (XBRL)', 'value_millions': round(rv, 1), 'period': f"{rev['start']} to {rev['end']}", 'filed': rev['filed'], 'source': rev['accn']})
        out['annual_revenue_musd'] = round(rv, 1)
        if 'enterprise_value_musd' in out: out['ev_to_revenue'] = round(out['enterprise_value_musd'] / rv, 2)
        out['market_cap_to_revenue'] = round(mcap / rv, 2)
        if (cutoff_day - date.fromisoformat(rev['end'])).days > 300: caveats.append(f"revenue is the last full fiscal year ending {rev['end']}, not a trailing twelve months")
    else:
        out['annual_revenue_musd'] = None; caveats.append('no positive annual revenue in the XBRL facts; revenue multiples not applicable')
    out['inputs'] = inputs; out['caveats'] = caveats
    out['note'] = 'Derived by the game from eligible inputs; share count and balance-sheet dates differ from the price date. Not a vendor market cap.'
    return out

def strip_urls(obj):
    if isinstance(obj, dict):
        return {k: strip_urls(v) for k, v in obj.items() if k not in ('url', 'local_copy')}
    if isinstance(obj, list):
        return [strip_urls(x) for x in obj]
    return obj

def main():
    sel = json.loads((ROOT / 'research' / 'selected.json').read_text())
    spy, _, spy_divs = load_bars('SPY')
    index = []
    for r in sel['selected']:
        cid, ticker, years = r['id'], r['ticker'], int(r['horizon_years'])
        cutoff_day = date.fromisoformat(r['proposed_cutoff'][:10])
        bars, splits, divs = load_bars(ticker)
        oid = opaque(cid)
        out = SITE / oid; out.mkdir(parents=True, exist_ok=True)
        mv = market_view(bars, spy, cutoff_day)
        oc = outcome(bars, spy, divs, cutoff_day, years, ticker, spy_divs)
        # Alternative horizons: same contract, context only, never the scored horizon
        alts = {}; longest = None
        for y in (1, 3, 5):
            if y == years:
                continue
            try:
                a = outcome(bars, spy, divs, cutoff_day, y, ticker, spy_divs)
            except (ValueError, KeyError, IndexError):
                alts[str(y)] = {'status': 'unavailable', 'reason': 'exit date beyond the cached price history'}
                continue
            alts[str(y)] = {k: a[k] for k in ('entry', 'exit', 'calendar_days', 'dividend_total_per_share', 'price_return_open_to_open',
                                              'long_total_return_after_costs', 'short_total_return_after_costs', 'spy_open_to_open_return',
                                              'max_drawdown_from_entry_path', 'results')}
            if longest is None or y > longest[0]:
                longest = (y, a)
        oc['alternative_horizons'] = alts
        # simulation block: opens and closes to the longest available anniversary, dividends for stock and SPY, horizon exit dates
        far = max([oc['exit']['date']] + [v['exit']['date'] for v in alts.values() if v.get('exit')])
        ei = first_on_or_after(bars, cutoff_day); xi = next(i for i, b in enumerate(bars) if str(b['date']) == far)
        spy_map_o = {str(b['date']): b for b in spy}
        oc['sim'] = {
            'path': [{'d': str(b['date']), 'o': round(b['open'], 4), 'c': round(b['close'], 4)} for b in bars[ei:xi + 1]],
            'spy_path': [{'d': str(b['date']), 'o': round(spy_map_o[str(b['date'])]['open'], 4), 'c': round(spy_map_o[str(b['date'])]['close'], 4)} for b in bars[ei:xi + 1] if str(b['date']) in spy_map_o],
            'dividends': [{'d': str(d_), 'a': a} for d_, a in divs if bars[ei]['date'] < d_ <= bars[xi]['date']],
            'spy_dividends': [{'d': str(d_), 'a': a} for d_, a in spy_divs if bars[ei]['date'] < d_ <= bars[xi]['date']],
            'horizons': {str(years): oc['exit']['date'], **{k: (v['exit']['date'] if v.get('exit') else None) for k, v in alts.items()}},
            'params': {'slippage': SLIPPAGE, 'borrow_annual': BORROW_ANNUAL, 'start_equity': START_EQUITY},
            'note': 'Client-side simulation input: fills at opens, dividends in (entry, exit], borrow on daily close. Stops and targets trigger on a close and fill at the next open.'}
        if longest and longest[0] > years:
            oc['extended_path'] = longest[1]['path']; oc['extended_spy_path'] = longest[1]['spy_path']
            oc['horizon_markers'] = [{'years': years, 'date': oc['exit']['date'], 'scored': True}] + \
                [{'years': int(k), 'date': v['exit']['date'], 'scored': False} for k, v in alts.items() if v.get('exit')]
        oc['split_or_spinoff_in_window'] = [{'date': str(d_), 'ratio': s} for d_, _, s in splits if oc['entry']['date'] <= str(d_) <= oc['exit']['date']]
        oc['candidate_id'] = cid; oc['ticker'] = ticker; oc['issuer'] = r['issuer']
        af = ROOT / 'cases' / cid / 'aftermath.json'
        if af.exists():
            try:
                oc['aftermath'] = json.loads(af.read_text())
            except ValueError:
                oc['aftermath'] = {'status': 'invalid json'}
        oc['editor_screen'] = r['screen']
        (out / 'market.json').write_text(json.dumps(mv))
        (out / 'outcome.json').write_text(json.dumps(oc))
        pj = ROOT / 'cases' / cid / 'player.json'; ej = ROOT / 'cases' / cid / 'evidence.json'
        status = 'market_only'
        entry = {'id': oid, 'cutoff': r['proposed_cutoff'], 'horizon': {'unit': 'calendar_years', 'count': years}, 'sector_hint': r['sector'].split(' (')[0], 'status': status}
        if pj.exists():
            p = json.loads(pj.read_text())
            sheet = copy.deepcopy(p); transparent = sheet.pop('transparent', {})
            sheet = strip_urls(sheet); sheet['case_id'] = oid; sheet.pop('candidate_id', None)
            sheet['horizon']['count'] = years
            sheet['horizons_available'] = sorted([k for k, v in oc['sim']['horizons'].items() if v], key=int)
            REPL.clear(); extra = set()
            for mt in r.get('mask_terms', []):
                if isinstance(mt, dict): extra.add(mt['term']); REPL[mt['term']] = mt['with']
                else: extra.add(mt)
            names = issuer_names(transparent.get('issuer', r['issuer']), transparent.get('ticker', ticker)) | extra
            sheet = mask_names(sheet, names, p.get('masked', {}).get('alias', 'the company'))
            sheet['masking_note'] = 'Issuer name and ticker replaced by "the company"; product and brand names are not masked in the MVP.'
            scenes = json.loads((ROOT / 'cases' / 'scenes.json').read_text())
            sc = scenes['scenes'].get(cid)
            if sc:
                sheet['scene'] = mask_names({'setup': sc['setup'], 'setup_label': scenes['setups'].get(sc['setup'], ''), 'voice': sc['voice'], 'claims': sc['claims'], 'question': sc['question'],
                                             'ask_friend': sc.get('ask_friend', []), 'ask_label': sc.get('ask_label'), 'assumptions': sc.get('assumptions', [])}, names, '')
                wt = []
                for w in sc.get('walkthrough', []):
                    ev = next((e for e in oc.get('aftermath', {}).get('events', []) if e['id'] == w['event_id']), None)
                    if ev:
                        masked_ev = mask_names({k: v for k, v in ev.items() if k != 'source'}, names, '')
                        masked_ev['source_withheld'] = 'shown in the debrief'
                        wt.append({'event': masked_ev, 'stage_text': mask_names(w['stage_text'], names, '')})
                oc['scene_check'] = {'setup': sc['setup'], 'voice': sc['voice'], 'claims': sc['claims'], 'debrief_check': sc.get('debrief_check'),
                                     'assumptions': sc.get('assumptions', []), 'thesis_check': sc.get('thesis_check'), 'walkthrough': wt}
                if sc.get('dated_debrief'):
                    oc['scene_check']['dated_debrief'] = sc['dated_debrief']
                (out / 'outcome.json').write_text(json.dumps(oc))
            sheet['neutral_title'] = mask_names(r.get('neutral_title', ''), names, '')
            sheet['player_question'] = mask_names(r.get('player_question', ''), names, '')
            sheet['valuation'] = valuation(cid, p, mv, cutoff_day)
            if sheet['valuation'].get('market_cap_musd'):   # the valuation block covers it: drop the writer's placeholder tile rather than repeat it
                hl = sheet.get('financial_snapshot', {}).get('headline', [])
                sheet['financial_snapshot']['headline'] = [h for h in hl if not (h.get('status') == 'missing' and ('enterprise value' in h['label'].lower() or 'market cap' in h['label'].lower()))]
            reveal = {'case_id': oid, 'candidate_id': cid, 'transparent': transparent, 'sources': [], 'claims': []}
            if ej.exists():
                e = json.loads(ej.read_text()); reveal['sources'] = e.get('sources', []); reveal['claims'] = e.get('claims', []); reveal['repairs_needed'] = e.get('repairs_needed', [])
                sheet['claims'] = mask_names([{k: c.get(k) for k in ('id', 'text', 'source_ids', 'status', 'formula', 'input_ids')} for c in e.get('claims', [])], names, '')
                sheet['source_handles'] = mask_names([{'id': s['id'], 'kind': s.get('kind'), 'title': s.get('title'), 'available_at': s.get('available_at'), 'availability_basis': s.get('availability_basis'), 'masked_title': s.get('kind', 'document') + ', public ' + str(s.get('available_at', ''))[:10], 'masked_headline': s.get('title', ''),
                                                       'excerpts': [{'claim_ids': x.get('claim_ids', []), 'text': x.get('text', ''), 'location': x.get('location')} for x in s.get('excerpts', [])]} for s in e.get('sources', [])], names, '')
            (out / 'reveal.json').write_text(json.dumps(reveal))
            (out / 'sheet.json').write_text(json.dumps(sheet))
            entry['status'] = 'sheet_ready'; entry['alias'] = p.get('masked', {}).get('alias'); entry['sector'] = p.get('masked', {}).get('sector')
            entry['title'] = sheet.get('neutral_title'); entry['setup'] = (sheet.get('scene') or {}).get('setup_label')
        index.append(entry)
        print(cid, '->', oid, entry['status'], 'entry', oc['entry'], 'exit', oc['exit'], 'long', oc['long_total_return_after_costs'], 'short', oc['short_total_return_after_costs'], 'spy', oc['spy_open_to_open_return'])
    (SITE / 'index.json').write_text(json.dumps({'built_at': datetime.now(timezone.utc).isoformat(), 'cases': index}, indent=1))
    payload_checks()


def payload_checks():
    """The build is the moment outcome text could reach a pre-decision file, so run scripts/test_payloads.js here.
    A leak fails the build (exit 1) after the files are written, so the offending sheet can be inspected."""
    import shutil, subprocess
    if not shutil.which('node'):
        print('WARNING: node not found; payload checks (scripts/test_payloads.js) not run'); return
    r = subprocess.run(['node', str(ROOT / 'scripts' / 'test_payloads.js')], capture_output=True, text=True)
    print((r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr).strip() else 'payload checks: no output')
    if r.returncode != 0:
        print('BUILD FAILED: outcome text or fields found in a pre-decision payload; see above'); sys.exit(1)


if __name__ == '__main__':
    main()
