"""Cache public Yahoo historical bars for research screening, not live trading."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'research' / 'prices'

def fetch(ticker):
    if not re.fullmatch(r'[A-Z0-9.^-]{1,12}', ticker):
        raise ValueError('Invalid ticker')
    CACHE.mkdir(parents=True, exist_ok=True)
    target = CACHE / f'{ticker}.json'
    if target.exists():
        return {'ticker': ticker, 'status': 'cached'}
    params = {
        'period1': int(datetime(2015, 1, 1, tzinfo=timezone.utc).timestamp()),
        'period2': int(datetime(2026, 9, 10, tzinfo=timezone.utc).timestamp()),
        'interval': '1d', 'events': 'div,splits',
    }
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + ticker + '?' + urlencode(params)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=40) as response:
            raw = response.read()
        data = json.loads(raw)
        result = data.get('chart', {}).get('result')
        if not result or not result[0].get('timestamp'):
            raise ValueError('No chart data: ' + str(data.get('chart', {}).get('error')))
        target.write_bytes(raw)
        meta = {'ticker': ticker, 'source_url': url,
                'retrieved_at': datetime.now(timezone.utc).isoformat(),
                'sha256': hashlib.sha256(raw).hexdigest(),
                'bars': len(result[0]['timestamp']),
                'purpose': 'Outcome screening; adjusted-close return is a vendor proxy, not a verified holdings ledger.'}
        (CACHE / f'{ticker}.meta.json').write_text(json.dumps(meta, indent=2) + '\n')
        return {**meta, 'status': 'downloaded'}
    except Exception as exc:
        return {'ticker': ticker, 'status': 'error', 'error': str(exc)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tickers', nargs='+')
    args = parser.parse_args()
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(fetch, args.tickers):
            results.append(result)
            print(json.dumps(result), flush=True)
    (CACHE / 'download-report.json').write_text(json.dumps(results, indent=2) + '\n')

if __name__ == '__main__':
    main()
