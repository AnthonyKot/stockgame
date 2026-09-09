"""Pull point-in-time XBRL facts from SEC companyfacts for each selected case.
Keeps only facts whose filing date is on/before the cutoff date and whose period ends within
five years before the cutoff. 'filed' is the public availability anchor (conservatively eligible
from the next session). Output: cases/<candidate_id>/xbrl-facts.json"""
import json, sys, urllib.request, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
UA = 'stockgame research olhakot.ux@gmail.com'
CIK = {'FSLR':'0001274494','HSY':'0000047111','AXSM':'0001579428','DE':'0000315189','TGT':'0000027419',
       'SRPT':'0000873303','JPM':'0000019617','GILD':'0000882095','MDGL':'0001157601','NKTR':'0000906709'}
TAGS = ['Revenues','RevenueFromContractWithCustomerExcludingAssessedTax','SalesRevenueNet','SalesRevenueGoodsNet',
 'CostOfRevenue','CostOfGoodsAndServicesSold','GrossProfit','ResearchAndDevelopmentExpense','SellingGeneralAndAdministrativeExpense',
 'OperatingIncomeLoss','NetIncomeLoss','EarningsPerShareDiluted','EarningsPerShareBasic',
 'CashAndCashEquivalentsAtCarryingValue','ShortTermInvestments','MarketableSecuritiesCurrent','AvailableForSaleSecuritiesDebtSecuritiesCurrent',
 'LongTermDebt','LongTermDebtNoncurrent','DebtCurrent','LongTermDebtCurrent','ConvertibleNotesPayable',
 'NetCashProvidedByUsedInOperatingActivities','PaymentsToAcquirePropertyPlantAndEquipment','NetCashProvidedByUsedInInvestingActivities','NetCashProvidedByUsedInFinancingActivities',
 'StockholdersEquity','Assets','Liabilities','CommonStockSharesOutstanding','WeightedAverageNumberOfDilutedSharesOutstanding',
 'PaymentsOfDividendsCommonStock','PaymentsForRepurchaseOfCommonStock','InterestExpense','IncomeTaxExpenseBenefit',
 'InterestAndDividendIncomeOperating','NoninterestIncome','NoninterestExpense','ProvisionForLoanLeaseAndOtherLosses','InterestIncomeExpenseNet','Deposits','LoansAndLeasesReceivableNetReportedAmount']
def main():
    sel = json.loads((ROOT/'research'/'selected.json').read_text())
    for r in sel['selected']:
        t = r['ticker']; cutoff = r['proposed_cutoff'][:10]
        y = int(cutoff[:4]) - 5; floor = f'{y}{cutoff[4:]}'
        url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK[t]}.json'
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        data = json.load(urllib.request.urlopen(req, timeout=60))
        out = {'candidate_id': r['id'], 'ticker': t, 'cik': CIK[t], 'entity': data.get('entityName'), 'cutoff': r['proposed_cutoff'],
               'rule': 'facts filed on/before cutoff date; period end within 5y before cutoff; filed date = availability anchor; values in USD unless unit says otherwise',
               'retrieved_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'source_url': url, 'facts': {}}
        gaap = data.get('facts', {}).get('us-gaap', {})
        n = 0
        for tag in TAGS:
            if tag not in gaap: continue
            rows = []
            for unit, items in gaap[tag]['units'].items():
                for it in items:
                    if it['filed'] <= cutoff and it['end'] >= floor:
                        rows.append({'value': it['val'], 'unit': unit, 'start': it.get('start'), 'end': it['end'], 'fy': it.get('fy'), 'fp': it.get('fp'),
                                     'form': it['form'], 'filed': it['filed'], 'accn': it['accn'], 'frame': it.get('frame')})
            if rows:
                rows.sort(key=lambda x: (x['end'], x['filed']))
                out['facts'][tag] = {'label': gaap[tag].get('label'), 'description': (gaap[tag].get('description') or '')[:300], 'rows': rows}; n += len(rows)
        d = ROOT/'cases'/r['id']; d.mkdir(parents=True, exist_ok=True)
        (d/'xbrl-facts.json').write_text(json.dumps(out, indent=1))
        print(r['id'], t, 'tags', len(out['facts']), 'rows', n, flush=True)
        time.sleep(0.4)
if __name__ == '__main__': main()
