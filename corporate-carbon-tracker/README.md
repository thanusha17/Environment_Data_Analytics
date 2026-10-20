# Corporate Carbon Footprint Tracker
## Theme 2: Environment Data Analytics (EDA) | Task ID: EDA-1
### Deliverable 1: Data Collection, Extraction, Cleaning & Documentation

---

## 1. Executive Summary
The **Corporate Carbon Footprint Tracker** is a Big Data Analytics project focused on tracking, analyzing, and forecasting corporate greenhouse gas (GHG) emissions. 

**Deliverable 1** implements the data engineering foundation:
- Sourcing real-world public disclosures across **22 global corporations** and **9 key economic sectors** over **FY2019–FY2023** (98 company-year observations).
- Sectors covered: **Technology**, **Technology / Retail**, **Automotive**, **Energy**, **Consumer Staples**, **Healthcare**, **Industrials**, **Consumer Discretionary**, and **Retail & Consumer**.
- Collecting audited financial revenues via the official **SEC EDGAR REST API**.
- Programmatically parsing Scope 1, Scope 2 (market & location), and Scope 3 emissions from official sustainability PDFs using **`pdfplumber`**.
- Standardizing units to metric tonnes ($tCO_2e$), calculating carbon intensity ($\frac{tCO_2e}{\text{USD Million}}$), and enforcing strict data quality and audit traceability standards.

> [!NOTE]
> In strict accordance with project rules, **zero synthetic or dummy data** were used. Every metric is accompanied by its source PDF, page number, table title, SEC accession number, and independent auditor assurance statement.

---

## 2. Project Directory Structure

```
corporate-carbon-tracker/
│
├── data/
│   ├── raw/
│   │   ├── sec_edgar/                  # Immutable raw SEC XBRL JSON files (22 files)
│   │   ├── sustainability_reports/     # Downloaded primary PDF reports (Apple, Google, MSFT, KO, JNJ, LMT, etc.)
│   │   └── source_inventory.csv        # Registry of companies, CIKs, tickers, sectors, URLs (22 companies)
│   │
│   ├── interim/
│   │   ├── raw_sec_financials.csv      # Extracted 10-K audited annual revenues (109 records)
│   │   └── raw_extracted_emissions.csv # Raw table values prior to harmonization (98 records)
│   │
│   └── processed/
│       └── company_emissions.csv       # Production master dataset (98 rows x 20 columns)
│
├── notebooks/
│   ├── 01_source_inventory.ipynb       # Phase 1: Company registry, coverage matrix, scoping
│   ├── 02_api_collection.ipynb        # Phase 2: Live SEC EDGAR REST API query & JSON parsing
│   ├── 03_pdf_extraction.ipynb         # Phase 3: pdfplumber table extraction & text mining
│   └── 04_clean_integrate_validate.ipynb # Phase 4: Harmonization, intensity calculation, validation
│
├── docs/
│   ├── data_dictionary.md              # Field definitions, data types, null rules, formulas
│   ├── extraction_methodology.md       # Protocols, endpoints, pdfplumber logic, citations
│   └── data_quality_report.md          # 6 validation check outcomes, coverage, intensity metrics
│
└── README.md                           # Project guide & reproduction instructions
```

---

## 3. Dataset Specification (`company_emissions.csv`)

The production dataset conforms to the 20-field specification mandated in Section 3 of the project guidelines:

| Field Name | Type | Unit | Description |
| :--- | :---: | :---: | :--- |
| `company_id` | String | - | Stable internal identifier (e.g., `TECH_MSFT`, `ENG_XOM`, `AUTO_TSLA`) |
| `company_name` | String | - | Normalized legal entity name |
| `ticker_or_lei` | String | - | Stock ticker symbol (`MSFT`, `AAPL`, `GOOGL`, `TSLA`, etc.) |
| `sector` | String | - | Industry sector (9 sectors covered) |
| `reporting_year` | Integer | YYYY | Reporting fiscal year (2019 to 2023) |
| `scope_1_tco2e` | Float | $tCO_2e$ | Direct emissions from operations, fuel combustion, fleet, fugitives |
| `scope_2_location_tco2e`| Float | $tCO_2e$ | Indirect emissions based on physical grid emission factors |
| `scope_2_market_tco2e` | Float | $tCO_2e$ | Indirect emissions based on contractual PPAs / green power instruments |
| `scope_3_tco2e` | Float | $tCO_2e$ | Value-chain emissions (upstream suppliers & downstream product use) |
| `revenue_value` | Float | USD | Audited annual revenue reported in SEC Form 10-K |
| `revenue_currency` | String | ISO | Denomination currency (`USD`) |
| `revenue_usd_m` | Float | Millions | Revenue in Millions of USD |
| `total_emissions_tco2e` | Float | $tCO_2e$ | $\text{Scope 1} + \text{Scope 2 (Market-based)}$ |
| `carbon_intensity_tco2e_per_usd_m`| Float | $\frac{tCO_2e}{\$M}$ | $\frac{\text{Total Emissions}}{\text{Revenue (USD Millions)}}$ |
| `reporting_boundary` | String | - | Consolidation approach (*Operational Control*, *Equity Share*, *Operated Basis*) |
| `source_title` | String | - | Name of primary report / filing |
| `source_url` | String | URL | Direct link to primary document |
| `source_page_or_table`| String | - | Exact page number and table identifier |
| `assurance_status` | String | - | Third-party auditor opinion (*Deloitte, EY, PwC, Apex, Lloyd's, ERM CVS, Bureau Veritas*) |
| `data_quality_note` | String | - | Specific notes on restatements, boundaries, or methodology |

---

## 4. Execution Sequence & Reproduction Guide

To run the pipeline from scratch:

### Prerequisites
Ensure Python 3.10+ is available with dependencies installed:
```bash
pip install pandas numpy requests pdfplumber nbformat jupyter
```

### Notebook Execution Workflow
Execute the Jupyter notebooks in order:

1. **`notebooks/01_source_inventory.ipynb`**:
   - Loads and verifies the corporate cohort (22 companies across 9 sectors).
   - Generates `data/raw/source_inventory.csv`.
2. **`notebooks/02_api_collection.ipynb`**:
   - Queries the official SEC EDGAR API (`data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`).
   - Caches immutable JSON payloads in `data/raw/sec_edgar/`.
   - Extracts 10-K audited revenues into `data/interim/raw_sec_financials.csv`.
3. **`notebooks/03_pdf_extraction.ipynb`**:
   - Inspects downloaded primary PDFs in `data/raw/sustainability_reports/`.
   - Demonstrates programmatic table extraction using `pdfplumber`.
   - Generates `data/interim/raw_extracted_emissions.csv`.
4. **`notebooks/04_clean_integrate_validate.ipynb`**:
   - Merges SEC financial turnover with primary emissions by `[company_id, reporting_year]`.
   - Harmonizes all units to metric tonnes ($tCO_2e$).
   - Calculates carbon intensity and executes all 6 formal data quality tests.
   - Exports the production master dataset to `data/processed/company_emissions.csv`.

---

## 5. Summary Findings & Carbon Intensity Profile

$$\text{Operational Carbon Intensity} = \frac{\text{Scope 1} + \text{Scope 2 (Market-based) } (tCO_2e)}{\text{Revenue (USD Millions)}}$$

| Sector | Companies | Observations | Median Intensity ($tCO_2e/\$M$) | Min | Max |
| :--- | :--- | :-: | :-: | :-: | :-: |
| **Consumer Discretionary** | Nike | 5 | **2.53** | 1.60 | 4.63 |
| **Technology** | Apple, MSFT, Google, Meta, Intel, NVIDIA, IBM, HP | 35 | **3.56** | 0.15 | 24.26 |
| **Healthcare** | Johnson & Johnson, Pfizer | 8 | **16.24** | 4.62 | 27.92 |
| **Automotive** | General Motors, Ford, Tesla | 14 | **21.98** | 10.52 | 129.76 |
| **Industrials** | Lockheed Martin, Caterpillar | 8 | **27.10** | 10.02 | 38.09 |
| **Retail & Consumer** | Walmart | 5 | **30.03** | 25.03 | 36.22 |
| **Technology / Retail** | Amazon | 5 | **34.44** | 29.54 | 128.78 |
| **Consumer Staples** | Coca-Cola | 3 | **115.80** | 108.19 | 133.75 |
| **Energy** | ExxonMobil, Chevron, ConocoPhillips | 15 | **372.26** | 235.45 | 867.76 |

---

## 6. Handoff to Deliverable 2
The cleaned secondary dataset (`company_emissions.csv`) provides the foundation for the machine learning and analytical objectives of **Deliverable 2**:
1. **Carbon Intensity Classification**: Supervised classification models (Random Forest, Gradient Boosting, XGBoost) to classify corporations into emissions tiers (*Low*, *Moderate*, *High Carbon Intensity*).
2. **Emissions Trend Forecasting**: Time-series forecasting (ARIMA, Prophet, LSTM) predicting emission reduction trajectories toward 2030 net-zero targets.
3. **Pledge vs. Actual Performance Tracking**: Quantitative variance modeling comparing announced reduction pledges against actual reported trajectories.
