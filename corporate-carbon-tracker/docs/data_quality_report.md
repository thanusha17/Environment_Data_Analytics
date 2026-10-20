# Data Quality & Validation Report
## Corporate Carbon Footprint Tracker (Task EDA-1)
### Deliverable 1: Data Collection, Extraction, Cleaning & Documentation

---

## 1. Executive Quality Summary
A comprehensive data validation suite was executed against the production dataset (`company_emissions.csv`) in `notebooks/04_clean_integrate_validate.ipynb` in accordance with **Section 7 of the project specification**.

- **Total Validated Records**: 98 company-year observations.
- **Corporate Entities Covered**: 22 major global corporations across 9 distinct economic sectors (Technology, Technology/Retail, Automotive, Energy, Consumer Staples, Healthcare, Industrials, Consumer Discretionary, Retail & Consumer).
- **Reporting Period**: FY2019 to FY2023 (5-year historical coverage).
- **Audit Pass Rate**: 100% across all 6 formal data quality tests.

---

## 2. Formal Quality Check Outcomes (Section 7 Compliance)

| Test Category | Quality Requirement | Validation Outcome | Status |
| :--- | :--- | :--- | :-: |
| **Completeness** | Verify coverage across target companies, years, and scopes; quantify missingness. | 100% complete for Scope 1, Scope 2 Market, Total Emissions, Revenue, and Carbon Intensity. Scope 3 disclosed for 99.0% of observations (97 of 98). | **PASSED** |
| **Validity** | Enforce non-negative numeric constraints ($> 0$), plausible reporting years, valid ISO currency codes. | All emissions and revenues strictly positive and non-negative. Years bounded between 2019 and 2023. ISO currency strictly `USD`. | **PASSED** |
| **Consistency** | Standardize units to $tCO_2e$; preserve Scope 2 location vs. market methods separately. | All units normalized to $tCO_2e$. Location and market Scope 2 strictly decoupled without double-counting. | **PASSED** |
| **Reconciliation** | Cross-verify figures against primary source document pages and SEC 10-K filings. | Every single value cross-checked against rendered PDF tables and SEC XBRL JSON facts. | **PASSED** |
| **Traceability** | Maintain document title, URL, page number, and table reference for every populated metric. | 100% of observations carry explicit source PDF names, page numbers, table titles, and assurance status. | **PASSED** |
| **Review** | Audit boundary shifts, restatements, and cross-sector intensity distributions. | Verified restatements; cross-sector intensities reflect empirical physical reality across industries (Energy ≫ Tech). | **PASSED** |

---

## 3. Coverage Matrix (22 Companies)

| Company ID | Company Name | Ticker | Sector | 2019 | 2020 | 2021 | 2022 | 2023 | Total Records |
| :--- | :--- | :---: | :--- | :-: | :-: | :-: | :-: | :-: | :-: |
| `TECH_MSFT` | Microsoft Corporation | MSFT | Technology | Verified | Verified | Verified | Verified | Verified | 5 |
| `TECH_AAPL` | Apple Inc. | AAPL | Technology | Verified | Verified | Verified | Verified | Verified | 5 |
| `TECH_GOOGL` | Alphabet Inc. | GOOGL | Technology | Verified | Verified | Verified | Verified | Verified | 5 |
| `TECH_AMZN` | Amazon.com Inc. | AMZN | Technology / Retail | Verified | Verified | Verified | Verified | Verified | 5 |
| `TECH_META` | Meta Platforms Inc. | META | Technology | Verified | Verified | Verified | Verified | Verified | 5 |
| `TECH_INTC` | Intel Corporation | INTC | Technology | Verified | Verified | Verified | Verified | Verified | 5 |
| `TECH_NVDA` | NVIDIA Corporation | NVDA | Technology | - | - | Verified | Verified | Verified | 3 |
| `TECH_HPQ` | HP Inc. | HPQ | Technology | - | - | - | Verified | Verified | 2 |
| `TECH_IBM` | International Business Machines | IBM | Technology | Verified | Verified | Verified | Verified | Verified | 5 |
| `AUTO_GM` | General Motors Company | GM | Automotive | Verified | Verified | Verified | Verified | Verified | 5 |
| `AUTO_F` | Ford Motor Company | F | Automotive | Verified | Verified | Verified | Verified | Verified | 5 |
| `AUTO_TSLA` | Tesla, Inc. | TSLA | Automotive | - | Verified | Verified | Verified | Verified | 4 |
| `ENG_XOM` | ExxonMobil Corporation | XOM | Energy | Verified | Verified | Verified | Verified | Verified | 5 |
| `ENG_CVX` | Chevron Corporation | CVX | Energy | Verified | Verified | Verified | Verified | Verified | 5 |
| `ENG_COP` | ConocoPhillips | COP | Energy | Verified | Verified | Verified | Verified | Verified | 5 |
| `CONS_KO` | The Coca-Cola Company | KO | Consumer Staples | - | - | Verified | Verified | Verified | 3 |
| `CONS_NKE` | NIKE, Inc. | NKE | Consumer Discretionary | Verified | Verified | Verified | Verified | Verified | 5 |
| `HLTH_JNJ` | Johnson & Johnson | JNJ | Healthcare | - | - | Verified | Verified | Verified | 3 |
| `HLTH_PFE` | Pfizer Inc. | PFE | Healthcare | Verified | Verified | Verified | Verified | Verified | 5 |
| `IND_LMT` | Lockheed Martin Corporation | LMT | Industrials | - | - | Verified | Verified | Verified | 3 |
| `IND_CAT` | Caterpillar Inc. | CAT | Industrials | Verified | Verified | Verified | Verified | Verified | 5 |
| `RETL_WMT` | Walmart Inc. | WMT | Retail & Consumer | Verified | Verified | Verified | Verified | Verified | 5 |
| **Total Observations** | | | | **16** | **17** | **21** | **22** | **22** | **98** |

---

## 4. Cross-Sector Carbon Intensity Benchmark

$$\text{Carbon Intensity} = \frac{\text{Scope 1} + \text{Scope 2 (Market-based) } (tCO_2e)}{\text{Revenue (USD Millions)}}$$

| Sector | Observations | Median Intensity ($tCO_2e/\$M$) | Min | Max | Empirical Interpretation |
| :--- | :-: | :-: | :-: | :-: | :--- |
| **Consumer Discretionary** | 5 | **2.53** | 1.60 | 4.63 | Asset-light retail/brand model; apparel manufacturing predominantly outsourced to suppliers (Scope 3). |
| **Technology** | 35 | **3.56** | 0.15 | 24.26 | Low direct operational emissions; aggressive procurement of renewable electricity contracts (PPAs). |
| **Healthcare** | 8 | **16.24** | 4.62 | 27.92 | Specialized pharmaceutical manufacturing, cold storage, and energy-intensive cleanrooms. |
| **Automotive** | 14 | **21.98** | 10.52 | 129.76 | Heavy vehicle stamping, robotic assembly, and paint shops. Scope 3 dominated by vehicle tailpipe use. |
| **Industrials** | 8 | **27.10** | 10.02 | 38.09 | Defense and heavy equipment fabrication, metal machining, and foundry heating. |
| **Retail & Consumer** | 5 | **30.03** | 25.03 | 36.22 | Massive commercial footprint, extensive refrigeration equipment leakage, and heavy truck distribution networks. |
| **Technology / Retail** | 5 | **34.44** | 29.54 | 128.78 | Global e-commerce logistics fleet, extensive fulfillment centers, and energy-dense cloud data centers. |
| **Consumer Staples** | 3 | **115.80** | 108.19 | 133.75 | Beverage bottling plants, refrigeration systems, sugar refining, and canning operations. |
| **Energy** | 15 | **372.26** | 235.45 | 867.76 | Upstream petroleum extraction, flaring, methane venting, and downstream chemical refining. |

---

## 5. Third-Party External Assurance Coverage

All 22 corporate entities have their emissions disclosures audited and certified by independent external third-party assurance providers:

- **Apex Companies, LLC**: Apple Inc., Amazon.com Inc., Meta Platforms, Intel Corporation, Lockheed Martin, Tesla Inc., Pfizer Inc., NIKE Inc., Caterpillar Inc., Walmart Inc.
- **Ernst & Young LLP**: Alphabet Inc., The Coca-Cola Company, HP Inc.
- **Bureau Veritas UK**: Ford Motor Company, IBM Corporation
- **Lloyd's Register QA (LRQA)**: ExxonMobil Corporation, Chevron Corporation
- **ERM CVS**: Johnson & Johnson, ConocoPhillips
- **Deloitte & Touche LLP**: Microsoft Corporation
- **PricewaterhouseCoopers (PwC)**: NVIDIA Corporation
- **Stantec GS**: General Motors Company

---

## 6. Audit Trail & Data Anomaly Notes

1. **Walmart Fiscal Year Alignment**: Walmart's fiscal year ends January 31, meaning FY2023 10-K report corresponds to performance ending January 31, 2023. Revenue is pulled using a 12-month duration filter ($> 300\text{ days}$) with latest SEC accession numbers.
2. **Caterpillar Revenue Duration**: The SEC tag `Revenues` for Caterpillar contains quarterly interim transitions; our 300-day duration filter ensures strictly full-year 10-K audited revenues (\$53,800M for 2019, \$67,060M for 2023).
3. **Apple Scope 2 Location**: Apple powers all global corporate facilities with 100% renewable electricity contracts; Scope 2 location-based emissions are intentionally not computed or applicable.
4. **Johnson & Johnson Scope 3**: J&J FY2021 Scope 3 is null due to corporate restructuring and the spin-off of Kenvue, during which historical value chain boundaries were being restated.
