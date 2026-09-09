"""Compute reproducible candidate outcome screens from cached adjusted closes."""
from datetime import date, datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]

def bars(ticker):
    source = ROOT / 'research' / 'prices' / f'{ticker}.json'
    if not source.exists():
        raise ValueError('Price history unavailable for ' + ticker)
    r = json.loads(source.read_text())['chart']['result'][0]
    zone = ZoneInfo(r['meta'].get('exchangeTimezoneName', 'America/New_York'))
    adjusted = r['indicators']['adjclose'][0]['adjclose']
    raw = r['indicators']['quote'][0]['close']
    return [(datetime.fromtimestamp(t, zone).date(), a, c)
            for t, a, c in zip(r['timestamp'], adjusted, raw)
            if a is not None and c is not None and a > 0 and c > 0]

def anniversary(day, years):
    try:
        return day.replace(year=day.year + years)
    except ValueError:
        return day.replace(year=day.year + years, day=28)

def screen(ticker, start, years):
    series = bars(ticker)
    first = next((b for b in series if b[0] >= start), None)
    if first is None or (first[0] - start).days > 7:
        raise ValueError('No entry session within seven calendar days')
    target = anniversary(first[0], years)
    last = next((b for b in series if b[0] >= target), None)
    if last is None or (last[0] - target).days > 7:
        raise ValueError('No complete exit session near anniversary')
    path = [b for b in series if first[0] <= b[0] <= last[0]]
    total = last[1] / first[1] - 1
    elapsed = (last[0] - first[0]).days / 365.2425
    cagr = (1 + total) ** (1 / elapsed) - 1
    peak, drawdown = first[1], 0
    for _, value, _ in path:
        peak = max(peak, value)
        drawdown = min(drawdown, value / peak - 1)
    spy = {d: a for d, a, _ in bars('SPY')}
    benchmark = spy[last[0]] / spy[first[0]] - 1
    return {'entry_date': str(first[0]), 'exit_date': str(last[0]),
            'entry_adjusted_close': first[1], 'exit_adjusted_close': last[1],
            'cumulative_return_pct': round(total * 100, 2),
            'cagr_pct': round(cagr * 100, 2),
            'max_drawdown_pct': round(drawdown * 100, 2),
            'spy_return_pct': round(benchmark * 100, 2),
            'screen_group': 'up' if cagr > .05 else 'down' if cagr < -.05 else 'roughly_flat',
            'method': 'vendor_adjusted_close_proxy_no_costs',
            'status': 'screened_not_final_game_scoring'}

def main():
    source = ROOT / 'research' / 'candidates.json'
    data = json.loads(source.read_text())
    candidates = data['candidates'] if isinstance(data, dict) else data
    for candidate in candidates:
        try:
            candidate['price_screen'] = screen(
                candidate['historical_ticker'],
                date.fromisoformat(candidate['proposed_cutoff'][:10]),
                int(candidate['horizon_years']))
        except (ValueError, KeyError, StopIteration) as exc:
            candidate['price_screen'] = {'status': 'unavailable', 'reason': str(exc)}
    target = ROOT / 'research' / 'candidates-screened.json'
    target.write_text(json.dumps({'candidates': candidates}, indent=2) + '\n')
    for c in candidates:
        p = c['price_screen']
        print(c['id'], c['historical_ticker'], c['horizon_years'], p.get('cagr_pct'), p.get('screen_group', p['status']))

if __name__ == '__main__':
    main()
