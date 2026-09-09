"""Arithmetic tests for the execution contract in build_bundles.py. Run: python3 scripts/test_returns.py"""
import sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_bundles as bb

def bars(seq):  # seq: [(date, open, close)]
    return [{'date': d, 'open': o, 'high': max(o, c), 'low': min(o, c), 'close': c, 'volume': 1, 'adjclose': c, 'unadjust_factor': 1.0} for d, o, c in seq]

def approx(a, b, tol=2e-4):  # builder rounds to 4 decimals
    assert abs(a - b) < tol, (a, b)

# one calendar year, no dividends: long = exit_open*(1-s)/(entry_open*(1+s)) - 1
stock = bars([(date(2020, 1, 2), 100.0, 101.0), (date(2020, 7, 1), 110.0, 110.0), (date(2021, 1, 4), 120.0, 121.0)])
spy = bars([(date(2020, 1, 2), 300.0, 301.0), (date(2020, 7, 1), 310.0, 310.0), (date(2021, 1, 4), 330.0, 331.0)])
oc = bb.outcome(stock, spy, [], date(2020, 1, 2), 1, 'T')
assert oc['entry']['date'] == '2020-01-02' and oc['exit']['date'] == '2021-01-04', (oc['entry'], oc['exit'])
approx(oc['price_return_open_to_open'], 0.2)
approx(oc['long_total_return_after_costs'], 120 * 0.999 / (100 * 1.001) - 1)
approx(oc['spy_open_to_open_return'], 0.1)
approx(oc['spy_price_return'], 0.1)

# dividends: stock pays 2.0 inside the window, SPY pays 3.0 inside and 5.0 on the entry date (excluded: entry < ex_date)
oc = bb.outcome(stock, spy, [(date(2020, 7, 1), 2.0)], date(2020, 1, 2), 1, 'T', spy_divs=[(date(2020, 1, 2), 5.0), (date(2020, 7, 1), 3.0)])
approx(oc['dividend_total_per_share'], 2.0)
approx(oc['long_total_return_after_costs'], (120 * 0.999 + 2.0) / (100 * 1.001) - 1)
approx(oc['spy_dividend_total_per_share'], 3.0)
approx(oc['spy_open_to_open_return'], (330 + 3.0) / 300 - 1)

# short: sell at open*(1-s), cover at open*(1+s), pay dividends and borrow on daily close
short_expected = (100 * 0.999 - 120 * 1.001 - 2.0 - oc['borrow_fee_per_share']) / 100
approx(oc['short_total_return_after_costs'], short_expected)
days1 = (date(2020, 7, 1) - date(2020, 1, 2)).days; days2 = (date(2021, 1, 4) - date(2020, 7, 1)).days
approx(oc['borrow_fee_per_share'], 101.0 * 0.05 / 365 * days1 + 110.0 * 0.05 / 365 * days2)

# leap day anniversary clamps to 28 Feb
assert bb.anniversary(date(2020, 2, 29), 1) == date(2021, 2, 28)
assert bb.anniversary(date(2020, 2, 29), 4) == date(2024, 2, 29)

# sizes: portfolio return = size x position return
approx(oc['results']['buy_20']['portfolio_return'], round(0.2 * oc['long_total_return_after_costs'], 4), 1e-4)
approx(oc['results']['short_5']['portfolio_return'], round(0.05 * oc['short_total_return_after_costs'], 4), 1e-4)
print('test_returns: all assertions passed')
