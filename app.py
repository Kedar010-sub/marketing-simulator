import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Marketing A/B Test Simulator", page_icon="📊", layout="wide")

st.title("📊 Marketing A/B Test Simulator")
st.markdown("Compare two marketing strategies and analyze their performance metrics")

if 'results' not in st.session_state:
    st.session_state.results = None

col1, col2 = st.columns(2)

with col1:
    st.header("🔵 Scenario A")
    ad_spend_a = st.number_input("Ad Spend ($)", min_value=0, max_value=1000000, value=10000, step=1000, key="ad_spend_a")
    ctr_a = st.number_input("Click-Through Rate (%)", min_value=0.0, max_value=20.0, value=2.5, step=0.1, key="ctr_a")
    conv_rate_a = st.number_input("Conversion Rate (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, key="conv_a")
    aov_a = st.number_input("Average Order Value ($)", min_value=0, max_value=1000, value=75, step=5, key="aov_a")
    cac_target_a = st.number_input("Target CAC ($)", min_value=0, max_value=500, value=50, step=5, key="cac_a")
    brand_awareness_a = st.slider("Brand Awareness (%)", min_value=0, max_value=100, value=30, key="brand_a")
    email_open_a = st.slider("Email Open Rate (%)", min_value=0, max_value=100, value=22, key="email_a")
    social_eng_a = st.number_input("Social Engagement Rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1, key="social_a")

with col2:
    st.header("🟢 Scenario B")
    ad_spend_b = st.number_input("Ad Spend ($)", min_value=0, max_value=1000000, value=10000, step=1000, key="ad_spend_b")
    ctr_b = st.number_input("Click-Through Rate (%)", min_value=0.0, max_value=20.0, value=2.5, step=0.1, key="ctr_b")
    conv_rate_b = st.number_input("Conversion Rate (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, key="conv_b")
    aov_b = st.number_input("Average Order Value ($)", min_value=0, max_value=1000, value=75, step=5, key="aov_b")
    cac_target_b = st.number_input("Target CAC ($)", min_value=0, max_value=500, value=50, step=5, key="cac_b")
    brand_awareness_b = st.slider("Brand Awareness (%)", min_value=0, max_value=100, value=30, key="brand_b")
    email_open_b = st.slider("Email Open Rate (%)", min_value=0, max_value=100, value=22, key="email_b")
    social_eng_b = st.number_input("Social Engagement Rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1, key="social_b")

def calculate_metrics(ad_spend, ctr, conv_rate, aov, brand_awareness, social_eng):
    impressions = ad_spend * 100
    clicks = impressions * (ctr / 100)
    conversions = clicks * (conv_rate / 100)
    revenue = conversions * aov
    profit = revenue - ad_spend
    roi = ((revenue - ad_spend) / ad_spend) * 100 if ad_spend > 0 else 0
    actual_cac = ad_spend / conversions if conversions > 0 else 0
    reach_score = impressions * (brand_awareness / 100)
    engagement_score = clicks * (social_eng / 100)
    
    return {
        'impressions': int(impressions),
        'clicks': int(clicks),
        'conversions': int(conversions),
        'revenue': round(revenue, 2),
        'profit': round(profit, 2),
        'roi': round(roi, 2),
        'actual_cac': round(actual_cac, 2),
        'reach_score': int(reach_score),
        'engagement_score': int(engagement_score)
    }

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])

with col_btn1:
    run_sim = st.button("▶️ Run Simulation", type="primary", use_container_width=True)

with col_btn2:
    reset = st.button("🔄 Reset", use_container_width=True)

if run_sim:
    with st.spinner("Running simulation..."):
        results_a = calculate_metrics(ad_spend_a, ctr_a, conv_rate_a, aov_a, brand_awareness_a, social_eng_a)
        results_b = calculate_metrics(ad_spend_b, ctr_b, conv_rate_b, aov_b, brand_awareness_b, social_eng_b)
        st.session_state.results = {'A': results_a, 'B': results_b}

if reset:
    st.session_state.results = None
    st.rerun()

if st.session_state.results:
    st.markdown("---")
    st.header("📈 Simulation Results")
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.subheader("🔵 Scenario A Results")
        results_a = st.session_state.results['A']
        metrics_col1, metrics_col2 = st.columns(2)
        with metrics_col1:
            st.metric("Impressions", f"{results_a['impressions']:,}")
            st.metric("Clicks", f"{results_a['clicks']:,}")
            st.metric("Conversions", f"{results_a['conversions']:,}")
            st.metric("Revenue", f"${results_a['revenue']:,.2f}")
        with metrics_col2:
            st.metric("Profit", f"${results_a['profit']:,.2f}")
            st.metric("ROI", f"{results_a['roi']:.2f}%")
            st.metric("Actual CAC", f"${results_a['actual_cac']:.2f}")
            st.metric("Engagement Score", f"{results_a['engagement_score']:,}")
    
    with col_res2:
        st.subheader("🟢 Scenario B Results")
        results_b = st.session_state.results['B']
        metrics_col1, metrics_col2 = st.columns(2)
        with metrics_col1:
            st.metric("Impressions", f"{results_b['impressions']:,}")
            st.metric("Clicks", f"{results_b['clicks']:,}")
            st.metric("Conversions", f"{results_b['conversions']:,}")
            st.metric("Revenue", f"${results_b['revenue']:,.2f}")
        with metrics_col2:
            st.metric("Profit", f"${results_b['profit']:,.2f}")
            st.metric("ROI", f"{results_b['roi']:.2f}%")
            st.metric("Actual CAC", f"${results_b['actual_cac']:.2f}")
            st.metric("Engagement Score", f"{results_b['engagement_score']:,}")
    
    st.markdown("---")
    st.subheader("📊 Performance Comparison")
    
    comparison_data = pd.DataFrame({
        'Metric': ['Impressions', 'Clicks', 'Conversions', 'Revenue', 'Profit'],
        'Scenario A': [results_a['impressions'], results_a['clicks'], results_a['conversions'], results_a['revenue'], results_a['profit']],
        'Scenario B': [results_b['impressions'], results_b['clicks'], results_b['conversions'], results_b['revenue'], results_b['profit']]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=comparison_data['Metric'], y=comparison_data['Scenario A'], name='Scenario A', marker_color='#3b82f6'))
    fig.add_trace(go.Bar(x=comparison_data['Metric'], y=comparison_data['Scenario B'], name='Scenario B', marker_color='#10b981'))
    fig.update_layout(barmode='group', title='Performance Metrics Comparison', xaxis_title='Metrics', yaxis_title='Value', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🏆 Winner Analysis")
    winner_col1, winner_col2, winner_col3 = st.columns(3)
    
    with winner_col1:
        revenue_winner = "Scenario A" if results_a['revenue'] > results_b['revenue'] else "Scenario B" if results_b['revenue'] > results_a['revenue'] else "Tie"
        st.metric("Higher Revenue", revenue_winner)
    
    with winner_col2:
        roi_winner = "Scenario A" if results_a['roi'] > results_b['roi'] else "Scenario B" if results_b['roi'] > results_a['roi'] else "Tie"
        st.metric("Higher ROI", roi_winner)
    
    with winner_col3:
        cac_winner = "Scenario A" if results_a['actual_cac'] < results_b['actual_cac'] else "Scenario B" if results_b['actual_cac'] < results_a['actual_cac'] else "Tie"
        st.metric("Lower CAC", cac_winner)