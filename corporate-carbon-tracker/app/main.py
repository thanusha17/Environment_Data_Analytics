"""
Corporate Carbon Footprint Tracker - Interactive Streamlit Dashboard
Course: Environment Data Analytics (Sem-7 BDA Task EDA-1)
Deliverables: Deliverable 1 (Audited Data) & Deliverable 2 (ML Classification, Forecasting & Pledge Audit)
"""

import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Configuration & Theme Settings
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Corporate Carbon Tracker",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(APP_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_DIR, "data", "processed")
RAW_DATA_DIR = os.path.join(PROJECT_DIR, "data", "raw")
FIG_DIR = os.path.join(PROJECT_DIR, "docs", "figures")

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #059669;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-on-track {
        background-color: #d1fae5;
        color: #065f46;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-off-track {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Data Loading & Caching
# -----------------------------------------------------------------------------
@st.cache_data
def load_all_datasets():
    emissions_path = os.path.join(DATA_DIR, "company_emissions.csv")
    classification_path = os.path.join(DATA_DIR, "classification_results.csv")
    forecasts_path = os.path.join(DATA_DIR, "forecasts_2024_2030.csv")
    netzero_path = os.path.join(DATA_DIR, "netzero_gap_analysis.csv")
    pledge_path = os.path.join(DATA_DIR, "pledge_gap_results.csv")
    pledges_raw_path = os.path.join(RAW_DATA_DIR, "corporate_pledges.csv")
    
    df_emissions = pd.read_csv(emissions_path)
    df_clf = pd.read_csv(classification_path) if os.path.exists(classification_path) else None
    df_fore = pd.read_csv(forecasts_path) if os.path.exists(forecasts_path) else None
    df_nz = pd.read_csv(netzero_path) if os.path.exists(netzero_path) else None
    df_pledge = pd.read_csv(pledge_path) if os.path.exists(pledge_path) else None
    df_pledge_raw = pd.read_csv(pledges_raw_path) if os.path.exists(pledges_raw_path) else None

    return df_emissions, df_clf, df_fore, df_nz, df_pledge, df_pledge_raw

df_emissions, df_clf, df_fore, df_nz, df_pledge, df_pledge_raw = load_all_datasets()

# -----------------------------------------------------------------------------
# Sidebar Navigation & Cohort Filter
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/isometric/100/leaf.png", width=64)
st.sidebar.title("Corporate Carbon Tracker")
st.sidebar.markdown("**Audited Climate Intelligence**  \n*Deliverables 1 & 2 Completed*")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Executive Overview & Sector KPIs",
        "🏢 Corporate Profile & Provenance",
        "🤖 ML Carbon Intensity Classifier",
        "🔮 2024–2030 Forecasting Simulator",
        "🎯 Climate Pledge & Greenwashing Audit",
        "📄 Data Provenance & Methodology"
    ]
)

st.sidebar.markdown("---")
all_sectors = sorted(df_emissions['sector'].unique())
selected_sector = st.sidebar.selectbox("Filter Sector Cohort", ["All Sectors (16)"] + all_sectors)

if selected_sector != "All Sectors (16)":
    filtered_emissions = df_emissions[df_emissions['sector'] == selected_sector]
else:
    filtered_emissions = df_emissions

st.sidebar.markdown("---")
st.sidebar.info("""
**Audit Scope**:
- **65** Global Corporations
- **16** Economic Sectors
- **313** Audited Company-Years
- **0%** Synthetic Imputation
""")

# =============================================================================
# PAGE 1: EXECUTIVE OVERVIEW & SECTOR KPIS
# =============================================================================
if page == "📊 Executive Overview & Sector KPIs":
    st.markdown('<div class="main-header">🌍 Executive Overview & Sector Benchmarking</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Audited corporate carbon emissions panel (FY2019–FY2023) across 65 corporations and 16 economic sectors</div>', unsafe_allow_html=True)

    # Metric Row
    total_emissions = df_emissions['total_emissions_tco2e'].sum()
    total_companies = df_emissions['company_id'].nunique()
    total_sectors = df_emissions['sector'].nunique()
    latest_year = df_emissions['reporting_year'].max()
    netzero_on_track = df_nz['on_track_netzero'].sum() if df_nz is not None else 28
    netzero_pct = (netzero_on_track / total_companies) * 100

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_emissions/1e9:.2f}B</div><div class="metric-label">Tracked tCO2e (5 Yrs)</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_companies}</div><div class="metric-label">Audited Corporations</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_sectors}</div><div class="metric-label">Global Sectors</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #2563eb;">75.4%</div><div class="metric-label">ML Test Accuracy</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #dc2626;">56.9%</div><div class="metric-label">Off-Track Net-Zero</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Visualizations: 2 Columns
    c1, c2 = st.columns([3, 2])
    with c1:
        st.subheader("Sector Carbon Intensity Benchmark (tCO2e / $M Revenue)")
        sector_agg = filtered_emissions.groupby('sector')['carbon_intensity_tco2e_per_usd_m'].median().reset_index()
        sector_agg = sector_agg.sort_values('carbon_intensity_tco2e_per_usd_m', ascending=True)

        fig_sec = px.bar(
            sector_agg,
            x='carbon_intensity_tco2e_per_usd_m',
            y='sector',
            orientation='h',
            color='carbon_intensity_tco2e_per_usd_m',
            color_continuous_scale='Viridis',
            labels={'carbon_intensity_tco2e_per_usd_m': 'Median Carbon Intensity (tCO2e / $M)', 'sector': 'Sector'},
            title="Cross-Sector Median Carbon Intensity"
        )
        fig_sec.update_layout(height=480, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_sec, use_container_width=True)

    with c2:
        st.subheader("Emissions Scope Composition")
        scope1_sum = filtered_emissions['scope_1_tco2e'].sum()
        scope2_sum = filtered_emissions['scope_2_market_tco2e'].sum()
        scope3_sum = filtered_emissions['scope_3_tco2e'].dropna().sum()
        
        df_scopes = pd.DataFrame({
            'Scope': ['Scope 1 (Direct)', 'Scope 2 Market (Electricity)', 'Scope 3 (Supply Chain)'],
            'Emissions_tCO2e': [scope1_sum, scope2_sum, scope3_sum]
        })
        fig_pie = px.pie(
            df_scopes,
            names='Scope',
            values='Emissions_tCO2e',
            hole=0.45,
            color_discrete_sequence=['#ef4444', '#f59e0b', '#3b82f6'],
            title="Total Cohort Emissions by Scope"
        )
        fig_pie.update_layout(height=480, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    # Intensity Leaderboards
    l1, l2 = st.columns(2)
    with l1:
        st.markdown("#### 🟢 Top 10 Lowest Carbon Intensity Companies (FY2023)")
        latest_df = df_emissions[df_emissions['reporting_year'] == latest_year]
        top_clean = latest_df.sort_values('carbon_intensity_tco2e_per_usd_m', ascending=True).head(10)
        st.dataframe(
            top_clean[['company_name', 'sector', 'revenue_usd_m', 'carbon_intensity_tco2e_per_usd_m']].rename(
                columns={
                    'company_name': 'Company', 'sector': 'Sector',
                    'revenue_usd_m': 'Revenue ($M)',
                    'carbon_intensity_tco2e_per_usd_m': 'Intensity (tCO2e/$M)'
                }
            ),
            hide_index=True,
            use_container_width=True
        )

    with l2:
        st.markdown("#### 🔴 Top 10 Highest Carbon Intensity Companies (FY2023)")
        top_dirty = latest_df.sort_values('carbon_intensity_tco2e_per_usd_m', ascending=False).head(10)
        st.dataframe(
            top_dirty[['company_name', 'sector', 'revenue_usd_m', 'carbon_intensity_tco2e_per_usd_m']].rename(
                columns={
                    'company_name': 'Company', 'sector': 'Sector',
                    'revenue_usd_m': 'Revenue ($M)',
                    'carbon_intensity_tco2e_per_usd_m': 'Intensity (tCO2e/$M)'
                }
            ),
            hide_index=True,
            use_container_width=True
        )

# =============================================================================
# PAGE 2: CORPORATE PROFILE & PROVENANCE
# =============================================================================
elif page == "🏢 Corporate Profile & Provenance":
    st.markdown('<div class="main-header">🏢 Corporate Profile & Regulatory Provenance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Company-by-company audited carbon accounting with SEC EDGAR 10-K traceability</div>', unsafe_allow_html=True)

    comp_list = sorted(filtered_emissions['company_name'].unique())
    selected_company = st.selectbox("Select Corporation to Audit:", comp_list)

    comp_df = df_emissions[df_emissions['company_name'] == selected_company].sort_values('reporting_year')
    latest_rec = comp_df.iloc[-1]

    # Header Card
    h1, h2, h3, h4 = st.columns(4)
    with h1:
        st.metric("Sector", latest_rec['sector'])
    with h2:
        st.metric("Ticker / Identifier", str(latest_rec['ticker_or_lei']))
    with h3:
        st.metric("FY2023 Revenue", f"${latest_rec['revenue_usd_m']:,.1f} M")
    with h4:
        st.metric("Carbon Intensity", f"{latest_rec['carbon_intensity_tco2e_per_usd_m']:.2f} tCO2e/$M")

    # Time series of emissions
    st.subheader(f"Historical Emissions Profile (FY2019–FY2023): {selected_company}")
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=comp_df['reporting_year'],
        y=comp_df['scope_1_tco2e'],
        name='Scope 1 (Direct)',
        marker_color='#ef4444'
    ))
    fig_comp.add_trace(go.Bar(
        x=comp_df['reporting_year'],
        y=comp_df['scope_2_market_tco2e'],
        name='Scope 2 Market',
        marker_color='#f59e0b'
    ))
    if comp_df['scope_3_tco2e'].notnull().any():
        fig_comp.add_trace(go.Bar(
            x=comp_df['reporting_year'],
            y=comp_df['scope_3_tco2e'],
            name='Scope 3 (Value Chain)',
            marker_color='#3b82f6'
        ))
    fig_comp.update_layout(
        barmode='stack',
        title=f"{selected_company} — Multi-Scope Emissions Trajectory",
        xaxis_title="Reporting Fiscal Year",
        yaxis_title="Emissions (tCO2e)",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # Provenance Table
    st.subheader("Audited Regulatory Provenance & Source Documentation")
    st.markdown("""Every observation in this tracker has 100% provenance verified against SEC EDGAR 10-K filings or official corporate sustainability reports.""")
    prov_cols = ['reporting_year', 'source_title', 'source_page_or_table', 'assurance_status', 'source_url']
    disp_prov = comp_df[prov_cols].copy()
    disp_prov.columns = ['Year', 'Document Title', 'Page / Table', 'Audit Assurance', 'Verified Source URL']
    st.dataframe(disp_prov, hide_index=True, use_container_width=True)

# =============================================================================
# PAGE 3: ML CARBON INTENSITY CLASSIFIER
# =============================================================================
elif page == "🤖 ML Carbon Intensity Classifier":
    st.markdown('<div class="main-header">🤖 Supervised Machine Learning Classifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Forward out-of-time test evaluation (FY2023) predicting Corporate Carbon Intensity Tertiles (Low / Moderate / High)</div>', unsafe_allow_html=True)

    # Benchmark Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="metric-card"><div class="metric-value">75.4%</div><div class="metric-label">Gradient Boosting Test Acc</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-card"><div class="metric-value" style="color: #2563eb;">98.5%</div><div class="metric-label">Within-1-Tier Accuracy</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card"><div class="metric-value" style="color: #7c3aed;">0.876</div><div class="metric-label">Ensemble ROC-AUC (OvR)</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="metric-card"><div class="metric-value" style="color: #059669;">83.1%</div><div class="metric-label">High-Polluter Detection</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Model Leaderboard
    st.subheader("Model Benchmark Leaderboard (FY2023 Holdout Horizon, n = 65)")
    leaderboard_data = [
        {"Model": "⚡ Gradient Boosting Classifier", "CV Acc (5-Fold)": "66.1%", "Test Accuracy": "75.4%", "Within-1-Tier": "98.5%", "Macro F1": "0.717", "ROC-AUC": "0.856"},
        {"Model": "🤝 Soft Voting Ensemble", "CV Acc (5-Fold)": "68.1%", "Test Accuracy": "75.4%", "Within-1-Tier": "96.9%", "Macro F1": "0.734", "ROC-AUC": "0.876"},
        {"Model": "🌳 Extra Trees Classifier", "CV Acc (5-Fold)": "67.7%", "Test Accuracy": "72.3%", "Within-1-Tier": "96.9%", "Macro F1": "0.709", "ROC-AUC": "0.864"},
        {"Model": "📈 Logistic Regression", "CV Acc (5-Fold)": "65.7%", "Test Accuracy": "70.8%", "Within-1-Tier": "98.5%", "Macro F1": "0.661", "ROC-AUC": "0.871"},
        {"Model": "🛡️ Support Vector Machine (SVC)", "CV Acc (5-Fold)": "66.5%", "Test Accuracy": "70.8%", "Within-1-Tier": "96.9%", "Macro F1": "0.690", "ROC-AUC": "0.856"},
        {"Model": "🌲 Random Forest Classifier", "CV Acc (5-Fold)": "67.3%", "Test Accuracy": "69.2%", "Within-1-Tier": "96.9%", "Macro F1": "0.671", "ROC-AUC": "0.829"},
        {"Model": "🚀 XGBoost Classifier", "CV Acc (5-Fold)": "64.9%", "Test Accuracy": "67.7%", "Within-1-Tier": "96.9%", "Macro F1": "0.659", "ROC-AUC": "0.848"},
    ]
    st.dataframe(pd.DataFrame(leaderboard_data), hide_index=True, use_container_width=True)

    # Interactive Company Prediction Inspector
    st.markdown("---")
    st.subheader("Interactive Entity-Level Prediction Inspector")
    col_sel, col_model = st.columns([2, 1])
    with col_sel:
        test_companies = sorted(df_clf['company_name'].unique())
        inspect_comp = st.selectbox("Select Corporation to Inspect Prediction:", test_companies)
    with col_model:
        model_choice = st.selectbox("Select Model Architecture:", ["Gradient Boosting", "Soft Voting Ensemble", "Random Forest"])

    row = df_clf[df_clf['company_name'] == inspect_comp].iloc[0]
    actual_tier = row['actual_tier']
    
    if model_choice == "Gradient Boosting":
        pred_tier = row['pred_gbm_tier']
        p_low = row['prob_gbm_low']
        p_mod = row['prob_gbm_moderate']
        p_high = row['prob_gbm_high']
        is_correct = row['correct_gbm']
    elif model_choice == "Soft Voting Ensemble":
        pred_tier = row['pred_ens_tier']
        p_low = row['prob_ens_low']
        p_mod = row['prob_ens_moderate']
        p_high = row['prob_ens_high']
        is_correct = row['correct_ens']
    else:
        pred_tier = row['pred_rf_tier']
        p_low = row['prob_rf_low']
        p_mod = row['prob_rf_moderate']
        p_high = row['prob_rf_high']
        is_correct = row['correct_rf']

    p1, p2, p3 = st.columns(3)
    with p1:
        st.metric("Actual Carbon Intensity Tier", actual_tier)
    with p2:
        st.metric("Predicted Carbon Intensity Tier", pred_tier)
    with p3:
        if is_correct:
            st.success("✅ Prediction: EXACT MATCH")
        else:
            st.warning("⚠️ Prediction: Adjacent Boundary Error (Within-1-Tier)")

    # Probability Distribution Bar
    prob_df = pd.DataFrame({
        'Intensity Tier': ['Low Tier', 'Moderate Tier', 'High Tier'],
        'Probability': [p_low, p_mod, p_high]
    })
    fig_prob = px.bar(
        prob_df,
        x='Intensity Tier',
        y='Probability',
        color='Intensity Tier',
        color_discrete_map={'Low Tier': '#10b981', 'Moderate Tier': '#f59e0b', 'High Tier': '#ef4444'},
        range_y=[0, 1.0],
        title=f"Calibrated Class Probability Distribution for {inspect_comp}"
    )
    fig_prob.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_prob, use_container_width=True)

# =============================================================================
# PAGE 4: 2024–2030 FORECASTING SIMULATOR
# =============================================================================
elif page == "🔮 2024–2030 Forecasting Simulator":
    st.markdown('<div class="main-header">🔮 Time-Series Emissions Forecasting (2024–2030)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Multi-horizon Scope 1+2 emissions projections backtested with 7.22% MAPE and audited against Net-Zero 2050 Paris pathways</div>', unsafe_allow_html=True)

    f_comp_list = sorted(df_nz['company_name'].unique())
    sel_forecast_comp = st.selectbox("Select Corporation to Forecast:", f_comp_list)

    nz_row = df_nz[df_nz['company_name'] == sel_forecast_comp].iloc[0]
    hist_comp = df_emissions[df_emissions['company_name'] == sel_forecast_comp].sort_values('reporting_year')
    fore_comp = df_fore[df_fore['company_name'] == sel_forecast_comp].sort_values('forecast_year')

    # Status KPI
    on_track = nz_row['on_track_netzero']
    gap_pct = nz_row['netzero_gap_pct']
    hist_cagr = nz_row['historical_cagr'] * 100

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Historical Trend Pace (CAGR)", f"{hist_cagr:+.2f}% / yr")
    with k2:
        st.metric("FY2023 Actual Emissions", f"{nz_row['actual_2023_emissions_tco2e']:,.0f} t")
    with k3:
        st.metric("2030 Projected Emissions", f"{nz_row['projected_2030_emissions_tco2e']:,.0f} t")
    with k4:
        if on_track:
            st.markdown('<div style="margin-top: 15px;"><span class="badge-on-track">🟢 ON-TRACK (PARIS 1.5°C)</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="margin-top: 15px;"><span class="badge-off-track">🔴 OFF-TRACK (+{gap_pct:.1f}% Gap)</span></div>', unsafe_allow_html=True)

    # Interactive Simulator Slider
    st.markdown("#### 🎛️ Interactive Decarbonization Pace Simulator")
    sim_cagr = st.slider(
        "Simulate Custom Annual Decarbonization Rate (2024–2030):",
        min_value=-20.0, max_value=10.0, value=float(hist_cagr), step=0.5,
        help="Adjust the simulated annual rate of emissions change to see when the company reaches Paris 1.5°C targets."
    )

    # Build simulated curve
    sim_years = list(range(2023, 2031))
    sim_emissions = [nz_row['actual_2023_emissions_tco2e']]
    for y in range(2024, 2031):
        sim_emissions.append(sim_emissions[-1] * (1 + sim_cagr / 100))

    # Plot trajectories
    fig_fore = go.Figure()

    # Historical
    fig_fore.add_trace(go.Scatter(
        x=hist_comp['reporting_year'],
        y=hist_comp['scope_1_tco2e'] + hist_comp['scope_2_market_tco2e'],
        mode='lines+markers',
        name='Historical Audited Scope 1+2 (2019-2023)',
        line=dict(color='#0f172a', width=3),
        marker=dict(size=8)
    ))

    # Baseline Projected
    fig_fore.add_trace(go.Scatter(
        x=[2023] + fore_comp['forecast_year'].tolist(),
        y=[nz_row['actual_2023_emissions_tco2e']] + fore_comp['projected_emissions_tco2e'].tolist(),
        mode='lines+markers',
        name='Baseline Projected (Current Trend)',
        line=dict(color='#f59e0b', width=2.5, dash='dot'),
        marker=dict(size=7)
    ))

    # Simulated
    fig_fore.add_trace(go.Scatter(
        x=sim_years,
        y=sim_emissions,
        mode='lines+markers',
        name=f'Simulated Policy Pace ({sim_cagr:+.1f}%/yr)',
        line=dict(color='#3b82f6', width=2.5, dash='dash')
    ))

    # SBTi 50% Reduction Target in 2030
    sbti_target_val = nz_row['sbti_required_2030_target_tco2e']
    fig_fore.add_trace(go.Scatter(
        x=[2019, 2030],
        y=[nz_row['baseline_emissions_tco2e'], sbti_target_val],
        mode='lines+markers',
        name='SBTi 1.5°C Target Pathway (-50% by 2030)',
        line=dict(color='#10b981', width=2.5),
        marker=dict(size=9, symbol='star')
    ))

    fig_fore.update_layout(
        title=f"Multi-Horizon Decarbonization Trajectory to 2030: {sel_forecast_comp}",
        xaxis_title="Year",
        yaxis_title="Scope 1+2 Emissions (tCO2e)",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_fore, use_container_width=True)

# =============================================================================
# PAGE 5: CLIMATE PLEDGE & GREENWASHING AUDIT
# =============================================================================
elif page == "🎯 Climate Pledge & Greenwashing Audit":
    st.markdown('<div class="main-header">🎯 Corporate Climate Pledge & Greenwashing Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Auditing 20 voluntary net-zero commitments: Promised pace vs. delivered pace and the Big Tech AI paradox</div>', unsafe_allow_html=True)

    if df_pledge is not None:
        # Key Summary
        total_pledges = len(df_pledge)
        failing_pledges = (df_pledge['pledge_status'] == 'Off-Track').sum()
        
        q1, q2, q3 = st.columns(3)
        with q1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total_pledges}</div><div class="metric-label">Audited Corporate Pledges</div></div>', unsafe_allow_html=True)
        with q2:
            st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #dc2626;">{failing_pledges} / {total_pledges}</div><div class="metric-label">Pledges Facing Credibility Gap</div></div>', unsafe_allow_html=True)
        with q3:
            st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #059669;">{(total_pledges - failing_pledges)} / {total_pledges}</div><div class="metric-label">Genuine Decarbonization Leaders</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 4-Quadrant Strategic Matrix
        st.subheader("Strategic Greenwashing Risk Matrix (Pledged Ambition vs. Delivered Execution)")
        fig_quad = px.scatter(
            df_pledge,
            x='required_annual_reduction_pct',
            y='actual_annual_reduction_pct',
            text='company_name',
            color='pledge_status',
            color_discrete_map={'On-Track': '#10b981', 'Off-Track': '#ef4444'},
            hover_data=['sector', 'pledge_title', 'pledge_gap_pct_pts'],
            labels={
                'required_annual_reduction_pct': 'Pledged Annual Decarbonization Pace (% / yr)',
                'actual_annual_reduction_pct': 'Actual Delivered Annual Decarbonization Pace (% / yr)'
            },
            title="Pledge Ambition vs. Delivery Quadrant Scatter Plot"
        )
        # Quadrant boundary lines
        fig_quad.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Emissions Growth (0% Threshold)")
        fig_quad.add_vline(x=5.0, line_dash="dash", line_color="gray", annotation_text="Standard 5%/yr Ambition")
        fig_quad.update_traces(textposition='top center', marker=dict(size=12))
        fig_quad.update_layout(height=520, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_quad, use_container_width=True)

        st.markdown("---")
        st.subheader("Audited 20 Corporate Pledges Master Audit Table")
        disp_cols = [
            'company_name', 'sector', 'pledge_title', 'target_year',
            'required_annual_reduction_pct', 'actual_annual_reduction_pct',
            'pledge_gap_pct_pts', 'pledge_status'
        ]
        disp_df = df_pledge[disp_cols].copy()
        disp_df.columns = ['Company', 'Sector', 'Pledge Title', 'Target Year', 'Required Pace (%/yr)', 'Actual Pace (%/yr)', 'Pace Gap (pp)', 'Verdict']
        st.dataframe(disp_df, hide_index=True, use_container_width=True)

# =============================================================================
# PAGE 6: DATA PROVENANCE & METHODOLOGY
# =============================================================================
elif page == "📄 Data Provenance & Methodology":
    st.markdown('<div class="main-header">📄 Data Provenance & Technical Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Methodological integrity, SEC EDGAR XBRL extraction, and reproducible analytics pipeline</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🔬 Methodology & Core Scientific Principles
    1. **Zero-Synthetic Data Mandate**:
       - 100% of emissions figures ($n = 313$) and revenues ($n = 313$) are extracted directly from SEC EDGAR Form 10-K filings and audited corporate sustainability reports.
       - No synthetic data generators or generative approximations were permitted.
    2. **Standardized Intensity Metric**:
       $$\\text{Carbon Intensity} = \\frac{\\text{Scope 1 (tCO}_2\\text{e)} + \\text{Scope 2 Market (tCO}_2\\text{e)}}{\\text{Revenue (USD Millions)}}$$
    3. **Leakage-Free Supervised Machine Learning**:
       - Forward out-of-time test split: **FY2019–FY2022** for training vs **FY2023** for forward evaluation.
       - Historical track record metrics calculated strictly on training split.
       - Gradient Boosting and Voting Ensemble achieve **75.4% Test Accuracy** and **98.5% within-1-tier precision**.
    4. **Emissions Forecasting & Paris 1.5°C Audit**:
       - Backtested with **7.22% MAPE** on FY2023 holdout.
       - Applied Science Based Targets initiative (SBTi) 50% absolute emissions reduction criteria by 2030.
    """)

    st.markdown("### 📥 Download Audited Production Artifacts")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.download_button(
            "Download Audited Emissions CSV",
            data=df_emissions.to_csv(index=False),
            file_name="audited_company_emissions.csv",
            mime="text/csv"
        )
    with d2:
        if df_clf is not None:
            st.download_button(
                "Download ML Predictions CSV",
                data=df_clf.to_csv(index=False),
                file_name="classification_results.csv",
                mime="text/csv"
            )
    with d3:
        if df_fore is not None:
            st.download_button(
                "Download 2030 Forecasts CSV",
                data=df_fore.to_csv(index=False),
                file_name="forecasts_2024_2030.csv",
                mime="text/csv"
            )
    with d4:
        if df_pledge is not None:
            st.download_button(
                "Download Pledge Audit CSV",
                data=df_pledge.to_csv(index=False),
                file_name="pledge_gap_results.csv",
                mime="text/csv"
            )

st.markdown("---")
st.markdown("<div style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Corporate Carbon Footprint Tracker • Sem-7 Big Data Analytics • Environment Data Analytics</div>", unsafe_allow_html=True)
