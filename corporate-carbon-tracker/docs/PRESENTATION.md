# Corporate Carbon Footprint Tracker — Project Presentation

> **Sem-7 Big Data Analytics (BDA) — Task EDA-1**  
> **Course**: Environment Data Analytics  
> **Deliverables Covered**: Deliverable 1 (Data Extraction & Auditing) & Deliverable 2 (ML Classification, Forecasting & Pledge Accountability)  
> **PowerPoint Slide Deck**: [`corporate-carbon-tracker/Corporate_Carbon_Tracker_Presentation.pptx`](../Corporate_Carbon_Tracker_Presentation.pptx)

---

## Slide 1: Title Slide
* **Project Title**: Corporate Carbon Footprint Tracker
* **Subtitle**: Audited Multi-Scope Emissions Tracking, Supervised Machine Learning, Time-Series Forecasting & Corporate Climate Pledge Accountability
* **Scope**: 65 Global Corporations | 16 Economic Sectors | FY2019–FY2023 Panel Dataset (313 Audited Company-Years)
* **Audited Provenance**: 100% verified against SEC EDGAR 10-K annual filings and primary sustainability reports (GRI/CDP/TCFD)

---

## Slide 2: Executive Context — The Corporate Climate Accountability Problem
* **The Greenwashing Dilemma**:
  * Over 80% of Fortune 500 corporations market voluntary "Net-Zero by 2030" or "Carbon Neutral" commitments.
  * Corporate self-reporting is plagued by greenwashing, unverified carbon offsets, and opaque carbon accounting.
  * Financial markets and regulatory bodies lack quantitative tools to evaluate whether claimed emissions reductions are authentic or marketing rhetoric.
* **The Big Data Challenge**:
  * Carbon accounting requires harmonizing Scope 1 (direct combustion), Scope 2 Market & Location (purchased electricity), and Scope 3 (upstream/downstream value chain).
  * Data is fragmented across SEC 10-K filings, corporate ESG reports, and disparate reporting units (imperial tons, MWh, gCO2e).
* **Project Mission**:
  * Build an audited, zero-synthetic data pipeline from primary regulatory sources.
  * Develop machine learning models to classify carbon intensity, project 2030 trajectories, and audit voluntary pledges.

---

## Slide 3: Core Project Features & Four-Module Architecture
1. **Audited Data Foundation**: 100% provenance back to SEC EDGAR 10-K filings and primary sustainability reports (0 synthetic imputation).
2. **Standardized Intensity Metric**: Carbon intensity measured in $\text{tCO}_2\text{e} / \text{USD Million Revenue}$ for fair cross-sector comparison.
3. **Module 1 (EDA & Feature Engineering)**: Right-skewness normalization, Scope 3 completeness analysis, and leak-free feature matrix generation (`features.csv`, `labels.csv`).
4. **Module 2 (Supervised Classification)**: 5-algorithm benchmark predicting `Low`, `Moderate`, and `High` carbon intensity tiers with an out-of-time test protocol (`classification_results.csv`).
5. **Module 3 (Time-Series Forecasting)**: Empirical forward projections (2024–2030) and Net-Zero 50% reduction alignment check (`forecasts_2024_2030.csv`, `netzero_gap_analysis.csv`).
6. **Module 4 (Pledge Gap Analysis)**: Quantitative audit comparing promised reduction pace vs. delivered pace and greenwashing risk matrix (`pledge_gap_results.csv`).

---

## Slide 4: Enterprise Technology Stack & Tooling

| Layer | Technologies & Libraries | Functionality |
|---|---|---|
| **Data Engineering** | Python 3.11, Pandas 2.3.3, NumPy 1.26.4 | Multi-year panel processing, unit normalization, matrix algebra |
| **Data Ingestion** | SEC EDGAR API, Requests, JSON | Programmatic retrieval of audited corporate revenues (USD millions) |
| **Supervised ML** | Scikit-Learn 1.2.2, XGBoost 3.2.0 | `ColumnTransformer` pipelines, Random Forest, XGBoost, SVC, KNN, `GridSearchCV` |
| **Time Series** | Statsmodels 0.14.0 | Autoregressive Integrated Moving Average (ARIMA), Holt Damped Trend smoothing |
| **Visualization** | Matplotlib, Seaborn, python-pptx | Publication-grade 300 DPI figures, automated PPT generation |
| **Web Dashboard** | Streamlit 1.30.0 | Interactive multi-tab web application for real-time scenario analytics |
| **Version Control** | Git, GitHub | Distributed multi-contributor workflow |

---

## Slide 5: Deliverable 1 Overview — Audited Data Extraction
* **Dataset Scale**: **65 global corporations**, **16 sectors**, **313 audited observations** across FY2019–FY2023.
* **Total Emissions Tracked**: Over **2.5 Billion metric tonnes of $\text{CO}_2\text{e}$**.
* **16 Sectors Represented**:
  * Technology (Apple, Microsoft, Alphabet, Amazon, Meta, NVIDIA, Intel, Salesforce, etc.)
  * Energy (ExxonMobil, Chevron, ConocoPhillips, Marathon, Valero)
  * Utilities (NextEra Energy, Duke, Southern Co, Dominion, Exelon)
  * Automotive (Ford, General Motors, Tesla)
  * Healthcare, Finance, Industrials, Aerospace, Retail, Real Estate, Materials, Mining, Transportation.
* **Auditability & Provenance**: Each row contains direct SEC source URLs, reporting boundaries, and data quality assurance notes.

---

## Slide 6: Deliverable 2 (Module 1) — Statistical Distributions & Correlations
* **Statistical Insights**:
  * Raw Scope 1 emissions exhibited extreme right skewness ($+6.18$), normalized via natural logarithmic transform ($\log(x+1)$).
  * Multicollinearity diagnosis: High Pearson correlation ($r = 0.82$) between Scope 1 and total emissions; revenue scales linearly with Scope 2.
* **Figures**:
  * `docs/figures/eda/01_univariate_distributions.png`: Raw vs Log-transformed Distributions.
  * `docs/figures/eda/06_correlation_matrix.png`: Multicollinearity Correlation Heatmap.
* **Artifacts Generated**: `features.csv` (9 standardized features) & `labels.csv` (balanced tertiles: High 111, Mod 103, Low 99).

---

## Slide 7: Deliverable 2 (Module 1) — Sector Benchmarking & Scope 3 Analysis
* **Cross-Sector Benchmarking**:
  * Utilities median intensity exceeds **1,200 $\text{tCO}_2\text{e} / \$M$**, whereas Finance operates below **1.5 $\text{tCO}_2\text{e} / \$M$** (nearly a 1,000× divergence).
  * Justified the use of **sector-adjusted tertiles** rather than global thresholds to avoid structural industry bias.
* **Scope 3 Value-Chain "Iceberg"**:
  * In Technology, Retail, and Automotive, Scope 3 accounts for **75% to 92%** of complete corporate footprints.
* **Figures**:
  * `docs/figures/eda/02_sector_intensity_boxplot.png`: Cross-Sector Carbon Intensity Distributions.
  * `docs/figures/eda/05_scope3_analysis.png`: Scope 3 Completeness & Value-Chain Multipliers.

---

## Slide 8: Deliverable 2 (Module 2) — Supervised Classification Benchmark
* **Problem Formulation**: Predict `intensity_label` (`Low`, `Moderate`, `High`) based on emissions profiles, revenue scale, and sector identity without target leakage.
* **Out-of-Time Protocol**: Trained on historical FY2019–FY2022 (248 rows), evaluated on forward FY2023 (65 rows).
* **Model Benchmark Results (FY2023 Forward Test Horizon)**:

| Model | 5-Fold CV Acc | Test Accuracy (2023) | Test Macro F1 | Test ROC-AUC (OvR) |
|---|:---:|:---:|:---:|:---:|
| 🌲 **Random Forest Classifier** | **64.9%** | **64.6%** | **0.640** | **0.824** |
| ⚡ **Support Vector Machine (SVC)** | 53.6% | 63.1% | 0.587 | 0.797 |
| 🚀 **XGBoost Classifier** | 63.7% | 61.5% | 0.598 | 0.804 |
| 📍 **K-Nearest Neighbors (KNN)** | 50.8% | 56.9% | 0.512 | 0.751 |
| 📈 **Logistic Regression (Baseline)** | 53.2% | 55.4% | 0.435 | 0.815 |

* **Figure**: `docs/figures/classification/04_model_comparison.png` (Multi-Metric Benchmark Chart).

---

## Slide 9: Deliverable 2 (Module 2) — Classification Diagnostics & Feature Attribution
* **Diagnostic Confusion Heatmaps**:
  * Tree ensembles cleanly separate Low from High carbon intensity tiers with zero diagonal misclassification between extreme tiers.
* **Feature Attribution (Gini & Gain)**:
  * Primary Global Drivers: `log_scope1` and `log_revenue` account for $>55\%$ of tree split importance.
  * Secondary Discriminators: `scope1_share` and `scope3_ratio` separate Moderate from High intensity corporations within heavy industries.
* **Figures**:
  * `docs/figures/classification/01_confusion_matrices.png`: 2×2 Confusion Heatmaps.
  * `docs/figures/classification/03_feature_importance.png`: Random Forest Gini vs. XGBoost Gain Rankings.
* **Artifact Exported**: `classification_results.csv` (65 FY2023 company predictions with calibrated class probabilities).

---

## Slide 10: Deliverable 2 (Module 3) — Time Series Emissions Forecasting
* **Out-of-Sample Backtesting Protocol (FY2023 Evaluation)**:

| Forecasting Model | Backtest MAE (tCO2e) | Backtest RMSE (tCO2e) | Backtest MAPE (%) |
|---|:---:|:---:|:---:|
| 🏆 **CAGR Trend Baseline** | **365,438** | **913,562** | **7.22%** |
| 📉 **Holt Damped Exponential Smoothing** | 552,657 | 1,184,951 | 9.18% |
| 📏 **Linear Regression OLS** | 448,810 | 1,040,142 | 11.69% |
| 🌐 **Sector-Pooled ARIMA(1,1,0)** | 630,435 | 1,406,720 | 11.74% |

* **Forward 2024–2030 Projections**: Generated annual Scope 1+2 projections for all 65 corporations (**455 company-years**).
* **Figures**:
  * `docs/figures/forecasting/01_model_backtest_accuracy.png`: Model Backtesting Performance.
  * `docs/figures/forecasting/02_sector_forecast_trajectories.png`: Multi-Year Sector Trajectories vs. SBTi 2030 Target Lines.

---

## Slide 11: Deliverable 2 (Module 3) — Net-Zero 2030 Commitment Alignment
* **SBTi 1.5°C Paris Agreement Target**: Requires at least **50% absolute emissions reduction** from baseline by 2030.
* **Empirical Reality Check**:
  * **On-Track**: **28 companies (43.1%)** are projected to achieve or surpass the 50% cut.
  * **Off-Track / Deficit**: **37 companies (56.9%)** face a substantial emissions gap.
* **Sector Polarization**:
  * Decarbonizing Leaders: Finance (100% on-track), Real Estate (66.7%), Consumer Staples (66.7%), Utilities (60%).
  * Decarbonizing Laggards: Energy (0% on-track), Mining (0%), Transportation (0%).
* **Figures**:
  * `docs/figures/forecasting/03_netzero_gap_distribution.png`: Sector On-Track Breakdown & Gap Distribution.
  * `docs/figures/forecasting/04_top_companies_trajectory.png`: Bellwether Trajectories (Apple, Amazon, Exxon, NextEra Energy, JPMorgan, Ford).

---

## Slide 12: Deliverable 2 (Module 4) — Pledge vs. Actual Reality Gap Analysis
* **Pledge Registry Auditing**: Curated 20 voluntary corporate climate commitments in `corporate_pledges.csv`.
* **Mathematical Gap Formulation**:
  $$\text{Required Annual Pace} = 1 - (1 - 0.90)^{1 / (\text{Target Year} - \text{Base Year})}$$
  $$\text{Actual Annual Pace} = -\text{CAGR}_{2019-2023}$$
  $$\text{Pledge Gap Score (pp)} = \text{Required Pace} - \text{Delivered Pace}$$
* **Empirical Results**:
  * **On-Track / Ahead**: Only **15% (3 of 20)**: Bank of America ($-16.9$ pp), Intel ($-2.8$ pp), Prologis ($-1.9$ pp).
  * **Minor Deficit (7 companies)**: Ford, GM, ExxonMobil, Chevron, Walmart, Unilever, Goldman Sachs (pledging 2040–2050 dates with lower annual requirements).
  * **Severe Deficit (10 companies, 50%)**: Facing $>5$ pp deficit or growing emissions.
* **Figures**:
  * `docs/figures/pledge_gap/01_pledge_gap_ranking.png`: Corporate Pledge Accountability Ranking.
  * `docs/figures/pledge_gap/02_pledge_vs_actual_trajectories.png`: Promised vs Actual Decarbonization Pathways.

---

## Slide 13: Deliverable 2 (Module 4) — The Big Tech AI Paradox & Greenwashing Risk
* **The Hyperscale AI Energy Paradox**:
  * Big Tech firms pledged aggressive **2030 Net-Zero targets** requiring $18.9\%–20.6\%$ annual cuts.
  * In reality, surging electricity consumption from AI computing and hyperscale data centers caused emissions **growth**:
    * **Alphabet / Google**: $+58.7$ pp gap (**$+39.8\%/\text{yr}$ emissions growth**)
    * **Amazon**: $+21.2$ pp gap (**$+10.8\%/\text{yr}$ emissions growth**)
    * **Meta**: $+30.6$ pp gap (**$+10.0\%/\text{yr}$ emissions growth**)
* **Strategic Greenwashing Risk Matrix**:
  * **Quadrant I (Genuine Climate Leaders)**: High Ambition + High Execution (Bank of America, Prologis, Intel).
  * **Quadrant IV (Credibility / Greenwashing Risk)**: Aggressive 2030 Pledges + Expanding Emissions (Alphabet, Amazon, Apple, Meta).
* **Figures**:
  * `docs/figures/pledge_gap/04_greenwashing_risk_matrix.png`: Ambition vs. Delivery Quadrant Matrix.
  * `docs/figures/pledge_gap/03_sector_pledge_alignment.png`: Sector-Level Pace Alignment.

---

## Slide 14: Interactive Streamlit Dashboard Showcase
* **Live Web Application**: Built with Streamlit (`streamlit run corporate-carbon-tracker/app/main.py`).
* **Interactive Capabilities**:
  1. **Executive Overview**: Real-time KPI cards ($2.5\text{B}+ \text{tCO}_2\text{e}$ tracked), sector distribution charts, top/bottom intensity leaderboards.
  2. **Corporate Deep-Dive**: Company selector with stacked multi-scope time series and verified SEC provenance links.
  3. **Forecasting & Pledge Tracker**: Dynamic scenario projections to 2030 and real-time Net-Zero gap calculation.

---

## Slide 15: Final Outcomes, Conclusions & Future Scope
* **Key Achievements**:
  * Built an audited 65-company, 16-sector dataset with zero synthetic imputation.
  * Proved that Tree Ensembles (Random Forest) deliver state-of-the-art carbon intensity classification (64.6% accuracy, 0.824 AUC).
  * Disproved corporate net-zero marketing by demonstrating that 56.9% of corporations are off-track for 2030 Paris targets.
* **Academic & Industry Implications**:
  * Provides institutional investors and ESG funds with an audited, quantitative framework to identify genuine decarbonization vs greenwashing risk.
* **Future Work**:
  * Automated SEC EDGAR XBRL scrapers for continuous real-time annual updates.
  * Granular Category 1–15 Scope 3 supply chain decomposition.
  * Integration of satellite remote sensing (e.g., MethaneSAT) for physical plume verification.
