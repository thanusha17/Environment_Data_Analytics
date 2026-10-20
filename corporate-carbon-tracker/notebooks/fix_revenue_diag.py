import json
from pathlib import Path

# Goldman Sachs — uses 'RevenuesNetOfInterestExpense'
gs_path = Path('data/raw/sec_edgar/CIK0000886982.json')
with open(gs_path) as f:
    data = json.load(f)
us_gaap = data.get('facts', {}).get('us-gaap', {})
tag = 'RevenuesNetOfInterestExpense'
if tag in us_gaap:
    units = us_gaap[tag].get('units', {}).get('USD', [])
    forms = set(e.get('form') for e in units)
    fps   = set(e.get('fp')   for e in units)
    print(f"GS {tag}: forms={forms}, fps={fps}")
    fy_entries = [e for e in units if e.get('form') == '10-K' and e.get('fp') == 'FY']
    print("FY entries:")
    for e in sorted(fy_entries, key=lambda x: x.get('end', '')):
        end = e['end']
        val = e['val']
        filed = e['filed']
        print(f"  end={end}  val={val:,}  filed={filed}")
else:
    print(f"Tag '{tag}' not found")

# Unilever — why only 2019?
ul_path = Path('data/raw/sec_edgar/CIK0000101830.json')
with open(ul_path) as f:
    data2 = json.load(f)
us_gaap2 = data2.get('facts', {}).get('us-gaap', {})
tag2 = 'Revenues'
units2 = us_gaap2[tag2].get('units', {}).get('USD', [])
fy_entries2 = [e for e in units2 if e.get('form') == '10-K' and e.get('fp') == 'FY']
print()
print("UL Revenues FY 10-K entries:")
for e in sorted(fy_entries2, key=lambda x: x.get('end', '')):
    end = e['end']
    val = e['val']
    filed = e.get('filed', '')
    print(f"  end={end}  val={val:,}  filed={filed}")
