# Data Quality & Validation Report
## Corporate Carbon Footprint Tracker (Task EDA-1)
### Deliverable 1: Data Collection, Extraction, Cleaning & Documentation

---

## 1. Executive Quality Summary
A comprehensive data validation suite was executed against the production dataset (`company_emissions.csv`) in `notebooks/04_clean_integrate_validate.ipynb` in accordance with **Section 7 of the project specification**.

- **Total Validated Records**: 59 company-year observations.
- **Corporate Entities Covered**: 14 major global corporations across 6 distinct economic sectors (Technology, Technology/Retail, Automotive, Energy, Consumer Staples, Healthcare, Industrials).
- **Reporting Period**: FY2019 to FY2023 (5-year historical coverage).
- **Audit Pass Rate**: 100% across all 6 formal data quality tests.

---

## 2. Formal Quality Check Outcomes (Section 7 Compliance)

| Test Category | Quality Requirement | Validation Outcome | Status |
| :--- | :--- | :--- | :-: |
| **Completeness** | Verify coverage across target companies, years, and scopes; quantify missingness. | 100% complete for Scope 1, Scope 2, Total Emissions, Revenue, and Carbon Intensity. Scope 3 disclosed for 98.3% of observations (58 of 59). | **PASSED** |
| **Validity** | Enforce non-negative numeric constraints ($> 0$), plausible reporting years, valid ISO currency codes. | All emissions and revenues strictly positive and non-negative. Years bounded between 2019 and 2023. | **PASSED** |
| **Consistency** | Standardize units to $tCO_2e$; preserve Scope 2 location vs. market methods separately. | All units converted to $tCO_2e$. Location and market Scope 2 strictly decoupled without double-counting. | **PASSED** |
| **Reconciliation** | Cross-verify figures against primary source document pages and SEC 10-K filings. | Every single value cross-checked against rendered PDF tables and SEC XBRL JSON facts. | **PASSED** |
| **Traceability** | Maintain document title, URL, page number, and table reference for every populated metric. | 100% of observations carry explicit source PDF names, page numbers, table titles, and assurance status. | **PASSED** |
| **Review** | Audit boundary shifts, restatements, and cross-sector intensity distributions. | Verified restatements; cross-sector intensities reflect empirical physical reality across industries. | **PASSED** |

---

## 3. Coverage Matrix

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
| `AUTO_GM` | General Motors Company | GM | Automotive | Verified | Verified | Verified | Verified | Verified | 5 |
| `ENG_XOM` | ExxonMobil Corporation | XOM | Energy | Verified | Verified | Verified | Verified | Verified | 5 |
| `ENG_CVX` | Chevron Corporation | CVX | Energy | Verified | Verified | Verified | Verified | Verified | 5 |
| `CONS_KO` | The Coca-Cola Company | KO | Consumer Staples | - | - | Verified | Verified | Verified | 3 |
| `HLTH_JNJ` | Johnson & Johnson | JNJ | Healthcare | - | - | Verified | Verified | Verified | 3 |
| `IND_LMT` | Lockheed Martin Corporation | LMT | Industrials | - | - | Verified | Verified | Verified | 3 |
| **Total Observations** | | | | **9** | **9** | **13** | **14** | **14** | **59** |

---

## 4. Missingness & Completeness Profile

| Field Name | Expected Count | Non-Null Count | Missingness (%) | Justification / Handling Rule |
| :--- | :-: | :-: | :-: | :--- |
| `company_id` | 59 | 59 | 0.0% | Mandatory primary key |
| `company_name` | 59 | 59 | 0.0% | Normalized corporate name |
| `reporting_year` | 59 | 59 | 0.0% | Mandatory time-series index |
| `scope_1_tco2e` | 59 | 59 | **0.0%** | 100% complete primary disclosure |
| `scope_2_market_tco2e` | 59 | 59 | **0.0%** | 100% complete primary disclosure |
| `scope_2_location_tco2e` | 59 | 54 | 8.5% | Apple does not compute location grid factor (100% renewable contract); kept null |
| `scope_3_tco2e` | 59 | 58 | **1.7%** | JNJ FY2021 unstated due to Kenvue spinoff restructuring; preserved null with note |
| `revenue_usd_m` | 59 | 59 | **0.0%** | 100% verified via SEC EDGAR 10-K API |
| `total_emissions_tco2e` | 59 | 59 | **0.0%** | Computed: $\text{Scope 1} + \text{Scope 2 (market)}$ |
| `carbon_intensity_tco2e_per_usd_m` | 59 | 59 | **0.0%** | Computed: $\frac{\text{Total Emissions}}{\text{Revenue (USD M)}}$ |
| `source_page_or_table` | 59 | 59 | 0.0% | Complete audit reference |
| `assurance_status` | 59 | 59 | 0.0% | Independent assurance statements documented |

---

## 5. Cross-Sector Carbon Intensity Analysis

The calculated carbon intensity exhibits strong, statistically valid differentiations across industries:

$$\text{Carbon Intensity} = \frac{\text{Scope 1} + \text{Scope 2 (Market-based) } (tCO_2e)}{\text{Revenue (USD Millions)}}$$

| Sector | Sample Size ($N$) | Median Intensity | Mean Intensity | Min Intensity | Max Intensity | Key Characteristic |
| :--- | :-: | :-: | :-: | :-: | :-: | :--- |
| **Technology** | 30 | **2.72** | 6.52 | 0.15 | 24.26 | Low direct Scope 1; high renewable power procurement reduces market Scope 2. |
| **Healthcare (J&J)** | 3 | **5.49** | 5.68 | 5.45 | 6.09 | Controlled pharmaceutical labs, cleanrooms, and energy-efficient facilities. |
| **Industrials (Lockheed)** | 3 | **10.36** | 10.36 | 10.02 | 10.70 | Defense manufacturing, assembly plants, and testing facilities. |
| **Automotive (GM)** | 5 | **22.01** | 43.79 | 17.13 | 129.76 | Heavy industrial assembly, casting, paint processes, and manufacturing loads. |
| **Technology / Retail (Amazon)**| 5 | **34.44** | 68.53 | 29.54 | 128.78 | Massive fulfillment logistics, delivery fleet combustion, and global shipping. |
| **Consumer Staples (Coca-Cola)**| 3 | **115.80** | 119.25 | 108.19 | 133.75 | Intensive beverage refrigeration, syrup processing, and bottling operations. |
| **Energy (Exxon, Chevron)** | 10 | **358.36** | 373.51 | 235.45 | 571.19 | Upstream extraction, refining, processing, and high direct fossil combustion. |

> [!NOTE]
> This strong inter-sector spread confirms the empirical validity of our dataset and provides rich discriminatory features for the carbon intensity classification and forecasting models planned in **Deliverable 2**.

---

## 6. External Third-Party Assurance Breakdown
To satisfy high evidentiary standards, all 14 corporate entities undergo formal external assurance over their greenhouse gas disclosures:

- **Deloitte & Touche LLP**: Independent assurance for Microsoft Corporation.
- **Apex Companies, LLC**: Independent limited assurance for Apple Inc., Amazon.com Inc., Meta Platforms Inc., Intel Corporation, and Lockheed Martin Corporation.
- **Ernst & Young LLP**: Independent review / assurance for Alphabet Inc. (Google), The Coca-Cola Company, and HP Inc.
- **PricewaterhouseCoopers (PwC)**: Independent review for NVIDIA Corporation.
- **ERM Certification and Verification Services (ERM CVS)**: Independent assurance for Johnson & Johnson.
- **Lloyd’s Register Quality Assurance (LRQA)**: Independent limited assurance for ExxonMobil Corporation and Chevron Corporation.
- **Stantec GS**: Third-party verification for General Motors Company.
