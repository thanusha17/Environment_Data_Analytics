# Deliverable 2: Implementation Plan
## Corporate Carbon Footprint Tracker — Theme 2: Environment Data Analytics (EDA-1)

> **Status**: Planning Phase | **Dataset**: 313 rows · 65 companies · 16 sectors · FY2019–2023  
> **Predecessor**: Deliverable 1 — Data Collection, Extraction, Cleaning & Documentation ✅

---

## 0. What We Have Going In

The `company_emissions.csv` production master dataset gives us:

| Field Available | Analytical Potential |
|---|---|
| `scope_1_tco2e`, `scope_2_market_tco2e` | Core emission signals for ML features |
| `scope_3_tco2e` | Value-chain depth (available for ~74% of rows) |
| `carbon_intensity_tco2e_per_usd_m` | Ready-made regression/classification target |
| `sector` (16 categories) | Natural grouping/stratification variable |
| `reporting_year` (2019–2023) | 5-point time series per company |
| `revenue_usd_m` | Economic normalizer, co-variate |
| 65 companies, all third-party assured | High-quality, audited label data |

---

## 1. Deliverable 2 Objectives (from README Handoff)

The three formal objectives stated in the README are:

1. **Carbon Intensity Classification** — Supervised ML models to classify corporations into emissions intensity tiers
2. **Emissions Trend Forecasting** — Time-series forecasting toward 2030 net-zero trajectories
3. **Pledge vs. Actual Tracking** — Quantitative gap analysis between announced targets and real trajectories

We scope these into **4 analytical modules** below, each producing a notebook.

---

## 2. Proposed Notebook Structure

```
notebooks/
├── 10_eda_and_feature_engineering.ipynb     # Module 1 — EDA & Feature Engineering
├── 11_classification_models.ipynb           # Module 2 — Intensity Classification (ML)
├── 12_forecasting_models.ipynb              # Module 3 — Emissions Trend Forecasting
└── 13_pledge_gap_analysis.ipynb             # Module 4 — Pledge vs. Actual Gap Analysis

docs/
└── deliverable2_plan.md                     # ← this file
```

---

## 3. Module 1 — Exploratory Data Analysis & Feature Engineering
**Notebook**: `10_eda_and_feature_engineering.ipynb`

### 3.1 Goals
- Understand distribution of emissions and intensity across sectors and years
- Identify correlations and outliers
- Engineer the feature matrix that all ML models will consume

### 3.2 EDA Tasks

#### A. Univariate Analysis
- Distribution plots (histogram + KDE) for `scope_1`, `scope_2_market`, `scope_3`, `carbon_intensity`
- Log-transform check (emissions data is right-skewed; log scale likely needed)
- Percentile table per scope per sector

#### B. Sector-Level Comparative Analysis
- Box plots of `carbon_intensity_tco2e_per_usd_m` by sector (sorted by median)
- Heatmap: companies × years showing intensity (annotated)
- Bar chart: top 10 / bottom 10 most intensive companies in 2023

#### C. Trend Analysis (2019–2023)
- Line plots per sector showing mean Scope 1+2 trajectory
- COVID-19 dip visibility in 2020 (Transportation, Automotive, Airlines)
- YoY percentage change table per company

#### D. Scope 3 Coverage Analysis
- Pie chart: % rows with Scope 3 data by sector
- Scatter: Scope 3 vs Scope 1+2 (to see value-chain multiplier ratio)

#### E. Correlation Matrix
- Pearson correlation: `scope_1`, `scope_2`, `scope_3`, `revenue_usd_m`, `carbon_intensity`
- Identify multicollinearity before ML

### 3.3 Feature Engineering

| Feature | Formula / Method | Rationale |
|---|---|---|
| `log_scope1` | `log(scope_1 + 1)` | Normalize heavy right skew |
| `log_scope2` | `log(scope_2_market + 1)` | Same reason |
| `log_revenue` | `log(revenue_usd_m + 1)` | Revenue scale normalization |
| `scope3_ratio` | `scope_3 / (scope_1 + scope_2)` | Value-chain leverage metric |
| `scope2_reduction` | `(scope_2_market_2019 - scope_2_market_yr) / scope_2_market_2019` | Clean energy progress |
| `yoy_intensity_change` | `intensity_yr - intensity_{yr-1}` | Momentum signal |
| `sector_median_intensity` | Sector-level median in that year | Sector benchmark |
| `intensity_vs_sector_median` | `intensity - sector_median_intensity` | Relative performance |
| `scope1_share` | `scope_1 / total_emissions` | Source mix indicator |
| `intensity_label` | Tertile cut: Low / Moderate / High | **Classification target** |

#### Intensity Label Definition (for Module 2)
Classify each company-year into three tiers using **sector-adjusted tertiles**:
- **Low** — Bottom 33rd percentile of carbon intensity within sector
- **Moderate** — 33rd–67th percentile
- **High** — Top 33rd percentile

> Using sector-adjusted tertiles (not global) because comparing a utility with a tech company on raw intensity is meaningless.

### 3.4 Output Artifacts
- `data/processed/features.csv` — engineered feature matrix (all company-years)
- `data/processed/labels.csv` — intensity tier labels per company-year
- Saved plots in `docs/figures/eda/`

---

## 4. Module 2 — Carbon Intensity Classification (Supervised ML)
**Notebook**: `11_classification_models.ipynb`

### 4.1 Problem Statement
Given a company's sector, emissions profile, and financial scale, predict whether it falls in the **Low / Moderate / High** carbon intensity tier.

### 4.2 Target Variable
`intensity_label` — 3-class classification (engineered in Module 1)

### 4.3 Feature Set
```
Features (X):
  - log_scope1, log_scope2, log_revenue
  - sector (one-hot encoded, 16 sectors → 15 dummies)
  - reporting_year (as int; captures macro time trend)
  - scope1_share
  - yoy_intensity_change (lag feature)
  - scope3_ratio (where available; else median-imputed)

Target (y):
  - intensity_label: Low | Moderate | High
```

### 4.4 Models to Train

| Model | Library | Why |
|---|---|---|
| **Logistic Regression** | scikit-learn | Interpretable baseline |
| **Random Forest** | scikit-learn | Handles non-linearity, sector interactions |
| **Gradient Boosting (XGBoost)** | xgboost | Best typical tabular performance |
| **Support Vector Machine (SVM)** | scikit-learn | Good on small datasets |
| **K-Nearest Neighbors** | scikit-learn | Distance-based comparison company |

### 4.5 Experimental Setup

```
Train/Test Split:
  - Strategy: Year-based split — train on 2019–2022, test on 2023
  - Reason: Prevents data leakage; simulates real forecasting scenario
  - Train size: ~260 rows | Test size: ~53 rows (2023 data)

Cross-validation:
  - 5-fold stratified CV on training set
  - Stratified by both class AND sector to avoid sector imbalance
```

### 4.6 Evaluation Metrics
- **Accuracy** — Overall correctness
- **Macro F1-score** — Class-balanced performance (important for imbalanced tiers)
- **Confusion Matrix** — Visualize which tiers get confused
- **ROC-AUC (OvR)** — Per-class discrimination
- **Feature Importance** — From RF and XGBoost (SHAP values if time permits)

### 4.7 Hyperparameter Tuning
- `GridSearchCV` on top 2 performing models
- Key params: RF (`n_estimators`, `max_depth`, `min_samples_leaf`), XGBoost (`n_estimators`, `learning_rate`, `max_depth`, `subsample`)

### 4.8 Expected Insights
- Which features most strongly predict carbon intensity tier?
- Do sectors completely determine the tier, or do within-sector differences matter?
- Which companies are "over-performing" their sector benchmark?

### 4.9 Output Artifacts
- `data/processed/classification_results.csv` — Predictions + true labels per company-year
- `docs/figures/classification/` — Confusion matrices, feature importance charts, ROC curves

---

## 5. Module 3 — Emissions Trend Forecasting
**Notebook**: `12_forecasting_models.ipynb`

### 5.1 Problem Statement
Forecast each company's Scope 1+2 emissions from 2024 → 2030 to:
1. Project where they'll be against net-zero targets
2. Identify companies on track vs. at risk

### 5.2 Data Setup

```
Input: Annual company_emissions.csv (2019–2023) — 5 data points per company
Forecast horizon: 2024–2030 (7 future years)
Target variable: total_emissions_tco2e (Scope 1 + Scope 2 market)

Per-company time series shape:
  Year:       2019  2020  2021  2022  2023
  Emissions:  [y1]  [y2]  [y3]  [y4]  [y5]   → predict [2024..2030]
```

> **Note on small-n**: With only 5 data points per company, complex per-company LSTM is overfit risk. We use sector-level pooling + trend-based methods.

### 5.3 Forecasting Approaches

#### Approach A: Compound Annual Growth Rate (CAGR) Baseline
- Fit CAGR = `(emissions_2023 / emissions_2019)^(1/4) - 1` per company
- Project forward: `emissions_t = emissions_2023 × (1 + CAGR)^(t - 2023)`
- Simple, interpretable, strong baseline

#### Approach B: Linear Regression Trend (per company)
- OLS: `emissions ~ year` per company
- Project slope forward to 2030
- Good for companies with monotone decline (e.g., Apple, Microsoft)

#### Approach C: Sector-Level Pooled ARIMA
- Aggregate emissions per sector per year → 5-point series per sector (more stable)
- Fit ARIMA(1,1,0) or (0,1,1) per sector using `statsmodels`
- Assign sector forecast as context for company-level scaling

#### Approach D: Facebook Prophet (Sector-Level)
- Use `prophet` library with yearly seasonality disabled (annual data)
- Handles changepoints (COVID 2020 dip) automatically
- Better uncertainty intervals (95% CI bands on plots)

#### Approach E: XGBoost Regression (Cross-Company)
- Train a single model across all companies with lagged features:
  `[emissions_t-1, emissions_t-2, sector_OHE, year, revenue_usd_m]`
- Predict next year recursively from 2024→2030
- Tests if cross-company patterns generalize

### 5.4 Net-Zero Alignment Check
For each company/sector, compute:
- **2030 Projected Emissions** (from best model)
- **Required 2030 target** = 50% reduction from 2019 baseline (Science-Based Targets initiative — SBTi 1.5°C pathway)
- **Gap** = Projected 2030 − Required 2030 target
- **On-Track flag**: True if projected ≤ required

### 5.5 Evaluation (Backtesting)
- Train on 2019–2022, predict 2023, compare against actual 2023
- Metrics: **MAE**, **MAPE**, **RMSE** per company and per sector
- Pick best method per sector based on backtesting MAPE

### 5.6 Output Artifacts
- `data/processed/forecasts_2024_2030.csv` — Company × Year forecasted emissions
- `data/processed/netzero_gap_analysis.csv` — On-track flag + gap per company
- `docs/figures/forecasting/` — Line plots per sector (historical + forecast + SBTi target line)

---

## 6. Module 4 — Pledge vs. Actual Gap Analysis
**Notebook**: `13_pledge_gap_analysis.ipynb`

### 6.1 Problem Statement
Many corporations have announced voluntary net-zero or reduction pledges. This module compares:
- **What they promised** (published targets)
- **What they actually did** (our audited dataset, 2019–2023)

### 6.2 Corporate Pledge Dataset
We'll create a small `data/raw/corporate_pledges.csv` (manually curated, ~20 companies with public pledges):

| Field | Description |
|---|---|
| `company_id` | Match to `company_emissions.csv` |
| `pledge_type` | `net-zero`, `carbon-neutral`, `SBTi-1.5C`, `SBTi-WB2C` |
| `baseline_year` | Year pledge reduction is measured from |
| `target_year` | Year company claims to achieve target |
| `target_reduction_pct` | % reduction from baseline (e.g., 50%, 100%) |
| `scope_covered` | `S1`, `S1+S2`, `S1+S2+S3` |
| `pledge_source_url` | Official announcement link |

**Initial pledge dataset (20 companies)**:

| Company | Pledge | Baseline | Target Year | % Reduction |
|---|---|---|---|---|
| Microsoft | Net Zero | 2020 | 2030 | 100% (S1+S2+S3) |
| Apple | Carbon Neutral (ops) | 2019 | 2030 | 100% (S1+S2) |
| Alphabet/Google | Carbon Free Energy | 2019 | 2030 | 100% (S2 market) |
| Amazon | Net Zero | 2019 | 2040 | 100% (all scopes) |
| Meta | Net Zero | 2020 | 2030 | 100% (S1+S2+S3) |
| Ford | Carbon Neutral | 2021 | 2050 | 100% (S1+S2) |
| General Motors | Carbon Neutral | 2020 | 2040 | 100% |
| ExxonMobil | GHG Intensity -20% | 2016 | 2025 | 20% intensity |
| Chevron | GHG Intensity -35% | 2016 | 2028 | 35% intensity |
| Walmart | Net Zero | 2015 | 2040 | 100% (S1+S2) |
| Unilever | Net Zero | 2019 | 2039 | 100% |
| Johnson & Johnson | Carbon Neutral | 2016 | 2030 | 100% (S1+S2) |
| Pfizer | Net Zero | 2019 | 2040 | 100% |
| JPMorgan Chase | Carbon Neutral (ops) | 2019 | 2030 | 100% (S1+S2) |
| Goldman Sachs | Carbon Neutral (ops) | 2019 | 2030 | 100% (S1+S2) |
| Delta (comparative) | Carbon Neutral | 2019 | 2050 | 100% |
| AT&T | Carbon Neutral | 2020 | 2035 | 100% (S1+S2) |
| Prologis | Net Zero | 2020 | 2040 | 100% |
| Disney | Net Zero | 2020 | 2030 | 100% (S1+S2) |
| Intel | Net Zero | 2010 | 2030 | 100% (S1+S2) |

### 6.3 Analysis Steps

#### Step 1: Implied Annual Reduction Required
For each pledging company:
```
required_annual_reduction_pct = 1 - (1 - target_reduction_pct)^(1/(target_year - baseline_year))
```

#### Step 2: Actual Annual Reduction Achieved (2019–2023)
```
actual_cagr = (emissions_2023 / emissions_baseline_year)^(1/(2023 - baseline_year)) - 1
actual_annual_reduction_pct = -actual_cagr   # negative CAGR = reduction
```

#### Step 3: Pledge Gap Score
```
gap = required_annual_reduction_pct - actual_annual_reduction_pct
```
- `gap > 0` → Company is **falling behind** its pledge
- `gap ≤ 0` → Company is **on track** or **ahead**

#### Step 4: Trajectory Extrapolation
- Project actual trajectory to target year using linear trend
- Compare against pledge target value
- Compute absolute gap in tCO2e at target year

### 6.4 Visualizations
- **Pledge Tracker Dashboard** (matplotlib):
  - Per-company: actual trajectory (solid line) vs. required reduction path (dashed target line)
  - Color coded: 🟢 On-track | 🟡 Slightly behind | 🔴 Significantly behind
- **Gap Ranking Bar Chart**: Companies ranked by pledge gap score
- **Sector Summary**: Which sectors are most/least aligned with pledges?

### 6.5 Output Artifacts
- `data/raw/corporate_pledges.csv` — Manually curated pledge registry
- `data/processed/pledge_gap_results.csv` — Gap score, on-track flag, projected vs. required
- `docs/figures/pledge_gap/` — Per-company trajectory plots

---

## 7. Technology Stack for Deliverable 2

| Category | Libraries |
|---|---|
| **Data manipulation** | `pandas`, `numpy` |
| **Visualization** | `matplotlib`, `seaborn`, `plotly` (interactive) |
| **ML — Classification** | `scikit-learn`, `xgboost` |
| **ML — Forecasting** | `statsmodels` (ARIMA), `prophet` |
| **ML — Interpretability** | `shap` (SHAP values for feature importance) |
| **Evaluation** | `sklearn.metrics`, `sklearn.model_selection` |
| **Utilities** | `warnings`, `pathlib`, `json` |

Install command:
```bash
pip install scikit-learn xgboost prophet statsmodels shap plotly
```

---

## 8. Execution Sequence

```
Module 1  →  Module 2  →  Module 3  →  Module 4
  EDA &           ML            Time           Pledge
 Features    Classification   Series           Gap
  (10_)          (11_)        Forecast        Analysis
                               (12_)           (13_)
```

> Each module depends on `features.csv` from Module 1. Modules 2, 3, and 4 can be developed in parallel after Module 1 is complete.

---

## 9. Expected Deliverable 2 Outputs Summary

| Output File | Source Module | Description |
|---|---|---|
| `data/processed/features.csv` | Module 1 | Engineered feature matrix |
| `data/processed/labels.csv` | Module 1 | Intensity tier labels |
| `data/processed/classification_results.csv` | Module 2 | ML predictions vs. actuals |
| `data/processed/forecasts_2024_2030.csv` | Module 3 | Emissions forecast to 2030 |
| `data/processed/netzero_gap_analysis.csv` | Module 3 | Net-zero alignment per company |
| `data/raw/corporate_pledges.csv` | Module 4 | Pledge registry (curated) |
| `data/processed/pledge_gap_results.csv` | Module 4 | Gap scores and on-track flags |
| `docs/figures/` | All modules | Plots and visualizations |

---

## 10. Key Design Decisions & Rationale

### Why sector-adjusted intensity labels?
Raw carbon intensity ranges from 0.15 (Apple) to 5,000+ (Duke Energy utility). Comparing across sectors with global thresholds would result in all utility companies being "High" and all tech companies being "Low" — trivially sector-predictable. Sector-relative tertiles make the classification problem meaningful.

### Why year-based train/test split?
A random split would leak 2023 data into training (a company's 2020 and 2023 data are correlated). The time-based split — train 2019–2022, test 2023 — simulates a genuine real-world deployment scenario.

### Why CAGR + Linear Regression as forecasting baselines?
With only 5 time points per company, complex models (LSTM, per-company ARIMA) will overfit. CAGR and linear regression give honest, interpretable baselines. Prophet and XGBoost cross-company models add sophistication while mitigating small-n risk.

### Why manually curate pledges?
No standardized machine-readable database of corporate climate pledges exists. CDP, SBTi, and company press releases must be cross-referenced manually. We prioritize quality and auditability over automation here, consistent with Deliverable 1 principles.

---

## 11. Open Questions / Decisions Needed

- [ ] Should we use **global tertiles** or **sector-adjusted tertiles** for classification labels? (Recommendation: sector-adjusted)
- [ ] Do we want **interactive Plotly dashboards** or just static matplotlib? (Plotly is better for a demo)
- [ ] Should Scope 3 be included in the forecasting target, or keep it Scope 1+2 only? (Recommendation: Scope 1+2 only due to 26% missing Scope 3)
- [ ] Which companies to include in the pledge registry? (Start with the 20 listed in §6.2)
- [ ] Do we need a written report document (`.md` or `.pdf`) summarizing D2 findings, or just notebooks?
