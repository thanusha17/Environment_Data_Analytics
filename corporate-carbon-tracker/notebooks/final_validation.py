import pandas as pd

df = pd.read_csv('data/processed/company_emissions.csv')
print('=== FINAL DATASET SUMMARY ===')
print('Total rows: ', len(df))
print('Companies:  ', df['company_name'].nunique())
print('Years:      ', sorted(df['reporting_year'].unique()))

print()
print('=== SECTOR BREAKDOWN ===')
for sector, grp in df.groupby('sector'):
    n_co  = grp['company_name'].nunique()
    n_row = len(grp)
    print(f'  {sector:<25} {n_co} companies | {n_row} rows')

print()
print('=== NULL COUNTS (key fields) ===')
key_cols = [
    'scope_1_tco2e', 'scope_2_location_tco2e', 'scope_2_market_tco2e',
    'scope_3_tco2e', 'revenue_usd_m', 'total_emissions_tco2e',
    'carbon_intensity_tco2e_per_usd_m'
]
for col in key_cols:
    n = df[col].isnull().sum()
    print(f'  {col:<45} {n}')

print()
print('=== CARBON INTENSITY STATS ===')
print(df['carbon_intensity_tco2e_per_usd_m'].describe().round(3).to_string())

print()
print('=== COMPANIES WITH <5 YEAR RECORDS ===')
yr_cnt = df.groupby('company_name')['reporting_year'].count()
under5 = yr_cnt[yr_cnt < 5]
if len(under5) == 0:
    print('  None - all companies have 5 years')
else:
    print(under5.to_string())
