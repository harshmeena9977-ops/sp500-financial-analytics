import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="S&P 500 Enterprise Financial & Risk Intelligence",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for Modern Corporate Styling
st.markdown("""
    <style>
        .main { background-color: #f4f6f9; }
        .block-container { padding-top: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("sp500_processed.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%B')
    return df

with st.spinner("Initializing Enterprise Financial Engine..."):
    df = load_data()

# --- SIDEBAR CONTROL CENTER ---
st.sidebar.markdown("## 🎛️ Control Panel")
st.sidebar.markdown("---")

# Filters
selected_year = st.sidebar.selectbox("Fiscal Year", ["All Years"] + sorted([str(y) for y in df['year'].unique()]))
symbols = sorted(df['symbol'].unique())
selected_symbol = st.sidebar.selectbox("Asset Ticker", symbols, index=symbols.index("AAPL") if "AAPL" in symbols else 0)

# Filter Dataset
symbol_data = df[df['symbol'] == selected_symbol].sort_values("date").reset_index(drop=True)
if selected_year != "All Years":
    symbol_data = symbol_data[symbol_data['year'] == int(selected_year)]

# --- MAIN DASHBOARD HEADER ---
st.markdown(f"## 🏢 Executive Finance & Risk Dashboard — `{selected_symbol}`")
st.markdown(f"**Reporting Period:** `{selected_year}` | **Metrics Engine:** Active Real-Time Streamlit Pipeline")
st.markdown("---")

if symbol_data.empty:
    st.warning("No financial records found for the selected parameters.")
else:
    # --- ROW 1: CORPORATE KPI CARDS (8 Metrics Grid) ---
    latest = symbol_data.iloc[-1]
    prev = symbol_data.iloc[-2] if len(symbol_data) > 1 else latest
    price_diff = latest['close'] - prev['close']
    pct_diff = (price_diff / prev['close']) * 100 if prev['close'] != 0 else 0

    total_rev_proxy = (symbol_data['close'] * symbol_data['volume']).sum() / 1e6  # Value traded in Millions
    avg_vol = symbol_data['volume'].mean()
    max_price = symbol_data['high'].max()
    min_price = symbol_data['low'].min()
    mean_volatility = symbol_data['volatility_20'].mean() * 100
    total_records = len(symbol_data)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Close Price", f"${latest['close']:.2f}", f"{pct_diff:.2f}%", delta_color="normal")
    col2.metric("Total Market Turnover", f"${total_rev_proxy:,.2f}M")
    col3.metric("Period High / Low", f"${max_price:.2f}", f"Low: ${min_price:.2f}")
    col4.metric("Avg Daily Volatility", f"{mean_volatility:.2f}%")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Avg Daily Volume", f"{avg_vol:,.0f}")
    col6.metric("Active Trading Days", f"{total_records:,}")
    col7.metric("20-Day SMA (Latest)", f"${latest['sma_20']:.2f}" if pd.notna(latest['sma_20']) else "N/A")
    col8.metric("50-Day SMA (Latest)", f"${latest['sma_50']:.2f}" if pd.notna(latest['sma_50']) else "N/A")

    st.markdown("---")

    # --- ROW 2: INTERACTIVE PLOTLY ANIMATED CHARTS ---
    r1_col1, r1_col2 = st.columns(2)

    with r1_col1:
        st.markdown("### 📈 Price Trajectory & Moving Averages")
        fig_price = px.line(
            symbol_data, x='date', y=['close', 'sma_20', 'sma_50'],
            labels={'value': 'USD ($)', 'date': 'Timeline', 'variable': 'Indicator'},
            color_discrete_map={'close': '#1f77b4', 'sma_20': '#ff7f0e', 'sma_50': '#2ca02c'}
        )
        fig_price.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=30, b=20), height=380, legend_title=''
        )
        st.plotly_chart(fig_price, use_container_width=True)

    with r1_col2:
        st.markdown("### 📊 Volume Distribution & Liquidity")
        fig_vol = px.bar(
            symbol_data, x='date', y='volume',
            labels={'volume': 'Trading Volume', 'date': 'Timeline'},
            color='volume', color_continuous_scale='Blues'
        )
        fig_vol.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=30, b=20), height=380, coloraxis_showscale=False
        )
        st.plotly_chart(fig_vol, use_container_width=True)

    # --- ROW 3: ADVANCED RISK & RETURN BREAKDOWN ---
    r2_col1, r2_col2 = st.columns(2)

    with r2_col1:
        st.markdown("### 📉 Rolling 20-Day Volatility Risk")
        fig_volat = px.area(
            symbol_data, x='date', y='volatility_20',
            labels={'volatility_20': 'Volatility Risk', 'date': 'Timeline'},
            color_discrete_sequence=['#d62728']
        )
        fig_volat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=30, b=20), height=320
        )
        st.plotly_chart(fig_volat, use_container_width=True)

    with r2_col2:
        st.markdown("### 🔄 Daily Return Distribution Analysis")
        fig_hist = px.histogram(
            symbol_data, x='daily_return', nbins=50,
            labels={'daily_return': 'Daily Percentage Return', 'count': 'Frequency'},
            color_discrete_sequence=['#9467bd']
        )
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=30, b=20), height=320
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # --- ROW 4: DATA EXPLORER TABLE ---
    st.markdown("### 📋 Live Granular Data Grid")
    st.dataframe(
        symbol_data[['date', 'open', 'high', 'low', 'close', 'volume', 'daily_return', 'sma_20', 'sma_50', 'volatility_20']].tail(100),
        use_container_width=True
    )