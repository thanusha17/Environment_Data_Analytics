# Data Dictionary: Corporate Carbon Footprint Tracker
## Deliverable 1: Standardized Company Emissions Dataset (`company_emissions.csv`)

---

### Dataset Overview
- **File Name**: `company_emissions.csv`
- **Location**: `corporate-carbon-tracker/data/processed/company_emissions.csv`
- **Granularity**: Exactly one row per corporation per reporting/fiscal year (`company_id` + `reporting_year`).
- **Target Reporting Period**: FY2019 – FY2023.
- **Total Fields**: 20 standardized attributes.

---

### Column Definitions & Specifications

| # | Column Name | Data Type | Nullable | Units | Description & Calculation Rules |
| :-: | :--- | :--- | :-: | :--- | :--- |
| **1** | `company_id` | String | No | Alphanumeric | Internal unique identifier consisting of sector prefix and company ticker (e.g., `TECH_MSFT`, `ENG_XOM`, `AUTO_GM`). |
| **2** | `company_name` | String | No | Text | Normalized legal corporate name matching regulatory registrations. |
| **3** | `ticker_or_lei` | String | No | Alphanumeric | Primary equity stock ticker symbol (e.g., `MSFT`, `AAPL`, `GOOGL`). |
| **4** | `sector` | String | No | Text | Industry sector classification based on Global Industry Classification Standard (GICS) categories (`Technology`, `Energy`, `Automotive`, `Technology / Retail`). |
| **5** | `reporting_year` | Integer | No | Year (YYYY) | Fiscal or reporting calendar year to which the emissions and financial turnover apply (`2019` to `2023`). |
| **6** | `scope_1_tco2e` | Float | No | $tCO_2e$ | Direct greenhouse gas emissions resulting from on-site fossil fuel combustion, corporate vehicle fleets, and fugitive refrigerant losses. Harmonized to metric tonnes of $CO_2$ equivalent. |
| **7** | `scope_2_location_tco2e` | Float | Yes | $tCO_2e$ | Indirect emissions calculated using the grid-average emission factor of the physical subregion where electricity is consumed. Retained strictly separate from market-based emissions. |
| **8** | `scope_2_market_tco2e` | Float | Yes | $tCO_2e$ | Indirect emissions calculated using supplier-specific contractual emission factors, Power Purchase Agreements (PPAs), and Energy Attribute Certificates (EACs/RECs). Kept strictly separate from location-based figures. |
| **9** | `scope_3_tco2e` | Float | Yes | $tCO_2e$ | Total value chain emissions across relevant GHG Protocol Categories (e.g., purchased goods and services, capital goods, fuel-related activities, product transport, use of sold products). Null if not disclosed; never imputed as zero. |
| **10** | `revenue_value` | Float | No | Currency units | Total audited annual revenue reported in official SEC Form 10-K filings. |
| **11** | `revenue_currency` | String | No | ISO 4217 | Three-letter currency code representing the financial reporting denomination (`USD`). |
| **12** | `revenue_usd_m` | Float | No | Millions USD | Financial revenue converted into Millions of U.S. Dollars: $\text{revenue\_usd\_m} = \frac{\text{revenue\_value}}{10^6}$. |
| **13** | `total_emissions_tco2e` | Float | No | $tCO_2e$ | Calculated total operational footprint. Evaluated strictly without double counting as: $\text{Scope 1} + \text{Scope 2 (Market-based)}$ (falls back to location-based if market-based is unavailable). |
| **14** | `carbon_intensity_tco2e_per_usd_m` | Float | No | $\frac{tCO_2e}{\text{USD Million}}$ | Operational carbon intensity metric: $\text{carbon\_intensity} = \frac{\text{total\_emissions\_tco2e}}{\text{revenue\_usd\_m}}$. Measures emissions efficiency per unit of economic output. |
| **15** | `reporting_boundary` | String | No | Text | Organizational consolidation approach applied under the GHG Protocol (`Operational Control`, `Equity Share`, `Operated Basis`). |
| **16** | `source_title` | String | No | Text | Canonical title of the primary sustainability disclosure or ESG data fact sheet (e.g., *Google 2024 Environmental Report*, *Apple Environmental Progress Report*). |
| **17** | `source_url` | String | No | URL | Official public repository URL from which the primary PDF document was retrieved. |
| **18** | `source_page_or_table` | String | No | Text | Specific page number and table identifier within the source PDF (e.g., `Page 76, Environmental data tables`, `Page 3, Table 1`). |
| **19** | `assurance_status` | String | No | Text | Level of independent third-party external audit verification and assurance provider (e.g., *Third-party Assured (Deloitte & Touche LLP)*, *Third-party Assured (Apex Companies)*). |
| **20** | `data_quality_note` | String | Yes | Text | Audit trail notes documenting restatements, boundary modifications, methodological refinements, or specific extraction assumptions. |

---

### Missing Value Conventions
- **Null / NaN**: Indicates that a metric was neither published nor estimated by the corporation in that specific reporting cycle (e.g., Apple does not compute Scope 2 location-based emissions because their facilities run 100% on renewable contractual contracts).
- **Explicit Zero (`0.0`)**: Used exclusively when a company reports verified net-zero emissions for that specific sub-scope (e.g., Apple Scope 2 electricity market emissions = $0.0$).
- **No Zero Imputation**: Missing Scope 3 or Scope 2 values are never filled with $0.0$ to prevent skewing downstream analytics in Deliverable 2.
