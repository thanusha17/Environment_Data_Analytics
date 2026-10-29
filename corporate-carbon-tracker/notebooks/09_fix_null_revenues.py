"""
09_fix_null_revenues.py
========================
Patches null revenue_usd_m values in company_emissions.csv for companies
where SEC EDGAR only returned 1 year (blocking the manual fallback logic):
  - AERO_BA  (Boeing)         -- 2020-2023
  - AERO_RTX (RTX)            -- 2020-2023
  - FIN_WFC  (Wells Fargo)    -- 2020-2023
  - MAT_STLD (Steel Dynamics) -- 2019-2021
  - MEDIA_DIS (Walt Disney)   -- 2019-2023
Also patches raw_sec_financials.csv so it is consistent.
Run from corporate-carbon-tracker/ root.
"""

import pandas as pd
from pathlib import Path

ROOT          = Path(__file__).parent.parent
PROCESSED_DIR = ROOT / "data" / "processed"
INTERIM_DIR   = ROOT / "data" / "interim"
FINAL_CSV     = PROCESSED_DIR / "company_emissions.csv"
FIN_CSV       = INTERIM_DIR   / "raw_sec_financials.csv"

# Manual revenue data (USD, from annual reports / IR pages)
MANUAL_REV = {
    # Boeing -- revenues collapsed 2020 due to 737 MAX + COVID; recovered gradually
    "AERO_BA": {
        2020: 58_158_000_000,   # FY2020 10-K
        2021: 62_286_000_000,   # FY2021 10-K
        2022: 66_608_000_000,   # FY2022 10-K
        2023: 77_794_000_000,   # FY2023 10-K
    },
    # RTX (Raytheon Technologies) -- CIK maps to legacy Raytheon; merged entity
    "AERO_RTX": {
        2020: 56_587_000_000,   # FY2020 (post-merger year)
        2021: 64_388_000_000,
        2022: 67_074_000_000,
        2023: 68_920_000_000,
    },
    # Wells Fargo -- net revenue (interest income + non-interest income)
    "FIN_WFC": {
        2020: 58_490_000_000,
        2021: 78_492_000_000,
        2022: 73_786_000_000,
        2023: 82_597_000_000,
    },
    # Steel Dynamics -- EDGAR only had 2022-2023; backfill 2019-2021
    "MAT_STLD": {
        2019: 10_541_000_000,
        2020:  8_816_000_000,
        2021: 15_304_000_000,
    },
    # Walt Disney -- fiscal year ends in late September/October
    "MEDIA_DIS": {
        2019: 69_607_000_000,   # FY2019 (ended 28 Sep 2019)
        2020: 65_388_000_000,   # FY2020 (ended 3 Oct 2020, COVID impact)
        2021: 67_418_000_000,   # FY2021 (ended 2 Oct 2021, parks reopened)
        2022: 82_722_000_000,   # FY2022 (ended 1 Oct 2022)
        2023: 88_898_000_000,   # FY2023 (ended 30 Sep 2023)
    },
}

def patch_csv():
    df = pd.read_csv(FINAL_CSV)
    patched = 0

    for cid, yr_map in MANUAL_REV.items():
        for yr, val in yr_map.items():
            mask = (df["company_id"] == cid) & (df["reporting_year"] == yr) & df["revenue_usd_m"].isna()
            if not mask.any():
                continue
            rev_m = round(val / 1e6, 1)
            df.loc[mask, "revenue_value"]  = val
            df.loc[mask, "revenue_currency"] = "USD"
            df.loc[mask, "revenue_usd_m"]  = rev_m

            # Recompute total_emissions and carbon_intensity for those rows
            for idx in df[mask].index:
                s1  = df.at[idx, "scope_1_tco2e"]
                s2m = df.at[idx, "scope_2_market_tco2e"]
                s2l = df.at[idx, "scope_2_location_tco2e"]
                s2  = s2m if pd.notna(s2m) else s2l
                if pd.notna(s1) and pd.notna(s2):
                    total = s1 + s2
                    df.at[idx, "total_emissions_tco2e"] = total
                    df.at[idx, "carbon_intensity_tco2e_per_usd_m"] = round(total / rev_m, 4)
            patched += mask.sum()
            print(f"  Patched {cid} {yr}: rev=${val/1e9:.1f}B  rows={mask.sum()}")

    df.sort_values(["sector","company_name","reporting_year"], inplace=True)
    df.to_csv(FINAL_CSV, index=False)
    print(f"\n  Total rows patched: {patched}")
    nulls_after = df["revenue_usd_m"].isna().sum()
    print(f"  Remaining null revenues: {nulls_after}")

    # Also patch raw_sec_financials.csv for consistency
    fin = pd.read_csv(FIN_CSV)
    new_rows = []
    for cid, yr_map in MANUAL_REV.items():
        for yr, val in yr_map.items():
            exists = ((fin["company_id"] == cid) & (fin["reporting_year"] == yr)).any()
            if not exists:
                new_rows.append({
                    "company_id": cid, "reporting_year": yr,
                    "revenue_value": val, "revenue_currency": "USD",
                    "revenue_usd_m": round(val/1e6, 1),
                    "company_name": "PATCH", "ticker": "PATCH", "cik": 0,
                    "sec_accession_number": "MANUAL_PATCH",
                    "sec_filing_date": "MANUAL_PATCH", "xbrl_tag": "MANUAL_PATCH",
                })
    if new_rows:
        fin = pd.concat([fin, pd.DataFrame(new_rows)], ignore_index=True)
        fin.drop_duplicates(subset=["company_id","reporting_year"], keep="last", inplace=True)
        fin.to_csv(FIN_CSV, index=False)
        print(f"  raw_sec_financials.csv: added {len(new_rows)} manual rows")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("NULL REVENUE PATCH")
    print("="*60)
    patch_csv()
    print("="*60)
    print("PATCH COMPLETE")
    print("="*60)
