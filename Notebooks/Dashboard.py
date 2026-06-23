import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(
    page_title="BMW Stock Dashboard",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------
# COLOR PALETTE
# ---------------------------------------------------------------
BG          = "#1B1F3B"   # Dark Navy
PRIMARY     = "#FFB6C1"   # Pastel Pink
SECONDARY   = "#98FF98"   # Mint Green
HIGHLIGHT   = "#C8A2C8"   # Lilac
DATA_LINE   = "#00FFFF"   # Neon Cyan
TEXT        = "#F5F5F5"   # Off-White
MUTED       = "#A9A9A9"   # Gray
CARD_BG     = "#252A4D"   # slightly lighter navy for cards

# ---------------------------------------------------------------
# CUSTOM CSS — fonts, colors, styling
# ---------------------------------------------------------------
st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Quicksand:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {{
    font-family: 'Quicksand', sans-serif;
    color: {TEXT};
}}

/* App background with subtle glowing roundel watermark */
.stApp {{
    background-color: {BG};
    background-image:
        radial-gradient(circle at 85% 8%, rgba(0,255,255,0.10) 0%, rgba(0,255,255,0) 40%),
        radial-gradient(circle at 10% 90%, rgba(255,182,193,0.08) 0%, rgba(255,182,193,0) 45%);
    background-attachment: fixed;
}}

/* Big watermark badge behind content */
.bmw-watermark {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Orbitron', sans-serif;
    font-size: 22vw;
    font-weight: 900;
    color: rgba(0, 255, 255, 0.035);
    z-index: 0;
    pointer-events: none;
    user-select: none;
    letter-spacing: 2vw;
}}

h1, h2, h3 {{
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 0.5px;
}}

h1 {{
    color: {PRIMARY} !important;
    text-shadow: 0 0 18px rgba(255,182,193,0.45);
}}
h2, h3 {{
    color: {SECONDARY} !important;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: #14172E;
    border-right: 1px solid rgba(200,162,200,0.25);
}}
section[data-testid="stSidebar"] * {{
    color: {TEXT} !important;
}}

/* Metric cards */
div[data-testid="stMetric"] {{
    background: {CARD_BG};
    border: 1px solid rgba(0,255,255,0.25);
    border-radius: 16px;
    padding: 14px 18px;
    box-shadow: 0 0 18px rgba(0,255,255,0.08);
}}
div[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
    font-family: 'Quicksand', sans-serif !important;
}}
div[data-testid="stMetricValue"] {{
    color: {DATA_LINE} !important;
    font-family: 'Orbitron', sans-serif !important;
}}

/* Tabs */
button[data-baseweb="tab"] {{
    font-family: 'Orbitron', sans-serif !important;
    color: {MUTED} !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {PRIMARY} !important;
    border-bottom: 3px solid {PRIMARY} !important;
}}

/* Badge / logo block */
.bmw-badge {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 6px;
}}
.bmw-roundel {{
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: conic-gradient({HIGHLIGHT} 0deg 90deg, {SECONDARY} 90deg 180deg, {HIGHLIGHT} 180deg 270deg, {SECONDARY} 270deg 360deg);
    border: 3px solid {TEXT};
    box-shadow: 0 0 22px rgba(0,255,255,0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 10px;
    color: {BG};
    text-align: center;
}}
.bmw-title {{
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 30px;
    color: {PRIMARY};
    text-shadow: 0 0 16px rgba(255,182,193,0.5);
    letter-spacing: 1px;
}}
.bmw-subtitle {{
    font-family: 'Quicksand', sans-serif;
    color: {MUTED};
    font-size: 14px;
    margin-top: -6px;
}}

/* Dataframe */
[data-testid="stDataFrame"] {{
    border: 1px solid rgba(152,255,152,0.25);
    border-radius: 12px;
}}

/* Sliders / widgets accent */
div[data-baseweb="slider"] > div > div {{
    background: {DATA_LINE} !important;
}}

hr {{
    border-color: rgba(169,169,169,0.25);
}}
</style>

<div class="bmw-watermark">BMW</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# HEADER WITH STYLIZED BADGE (no copyrighted logo used)
# ---------------------------------------------------------------
st.markdown(f"""
<div class="bmw-badge">
    <div class="bmw-roundel">BMW</div>
    <div>
        <div class="bmw-title">BMW STOCK ANALYTICS</div>
        <div class="bmw-subtitle">✨ Market dashboard ✨</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<hr style='margin-top:6px;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Data\Clean\Final_BMW_dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df

df = load_data()

# ---------------------------------------------------------------
# SIDEBAR — INTERACTIVE CONTROLS
# ---------------------------------------------------------------
with st.sidebar:
    st.markdown(f"<div class='bmw-roundel' style='margin-bottom:10px;'>BMW</div>", unsafe_allow_html=True)
    st.markdown("### 🎛️ Controls")

    min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
    date_range = st.date_input(
        "📅 Date range",
        value=(max(min_date, max_date.replace(year=max_date.year - 3)), max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    price_field = st.selectbox(
        "💎 Price field to chart",
        ["Close", "Open", "High", "Low", "Adj_Close"],
        index=0,
    )

    show_ma = st.checkbox("📈 Show moving averages", value=True)
    ma_short = st.slider("Short MA window (days)", 5, 60, 20)
    ma_long = st.slider("Long MA window (days)", 50, 300, 100)

    chart_type = st.radio("🕹️ Chart style", ["Line", "Candlestick"], horizontal=True)

    st.markdown("---")
    st.markdown(f"<span style='color:{MUTED};font-size:12px;'>Data: cleaned BMW OHLCV dataset 🐱‍💻</span>", unsafe_allow_html=True)

mask = (df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)
fdf = df.loc[mask].copy()

if fdf.empty:
    st.warning("No data in the selected date range — please widen it. 🛑")
    st.stop()

fdf[f"MA_{ma_short}"] = fdf["Close"].rolling(ma_short).mean()
fdf[f"MA_{ma_long}"] = fdf["Close"].rolling(ma_long).mean()

# ---------------------------------------------------------------
# PLOTLY THEME HELPER
# ---------------------------------------------------------------
def style_fig(fig, title=None, height=450):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family="Quicksand, sans-serif", color=TEXT, size=13),
        title=dict(text=title, font=dict(family="Orbitron, sans-serif", color=SECONDARY, size=18)) if title else None,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=height,
        margin=dict(t=60, l=10, r=10, b=10),
    )
    fig.update_xaxes(gridcolor="rgba(169,169,169,0.15)", zerolinecolor="rgba(169,169,169,0.2)")
    fig.update_yaxes(gridcolor="rgba(169,169,169,0.15)", zerolinecolor="rgba(169,169,169,0.2)")
    return fig

# ---------------------------------------------------------------
# KPI METRICS
# ---------------------------------------------------------------
latest = fdf.iloc[-1]
first = fdf.iloc[0]
pct_change = (latest["Close"] - first["Close"]) / first["Close"] * 100
avg_vol = fdf["Volume"].mean()
volatility = fdf["Daily_Return"].std()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💖 Latest Close", f"{latest['Close']:.2f}")
k2.metric("🌿 Period Change", f"{pct_change:+.2f}%")
k3.metric("🔮 Highest Close", f"{fdf['Close'].max():.2f}")
k4.metric("🌙 Lowest Close", f"{fdf['Close'].min():.2f}")
k5.metric("⚡ Avg Daily Volatility", f"{volatility:.2f}%")

st.markdown("")

# ---------------------------------------------------------------
# TABS
# ---------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📈 Price Trends", "🎲 Returns & Volatility", "🧬 Correlations", "🗂️ Raw Data"])

# ---- TAB 1: PRICE TRENDS ----
with tab1:
    st.markdown("### Price Trend Explorer")

    if chart_type == "Candlestick":
        fig = go.Figure(data=[go.Candlestick(
            x=fdf["Date"], open=fdf["Open"], high=fdf["High"],
            low=fdf["Low"], close=fdf["Close"],
            increasing_line_color=SECONDARY, decreasing_line_color=PRIMARY,
            name="BMW"
        )])
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fdf["Date"], y=fdf[price_field], mode="lines",
            name=price_field, line=dict(color=DATA_LINE, width=1.6)
        ))

    if show_ma:
        fig.add_trace(go.Scatter(
            x=fdf["Date"], y=fdf[f"MA_{ma_short}"], mode="lines",
            name=f"MA {ma_short}d", line=dict(color=PRIMARY, width=1.4, dash="dot")
        ))
        fig.add_trace(go.Scatter(
            x=fdf["Date"], y=fdf[f"MA_{ma_long}"], mode="lines",
            name=f"MA {ma_long}d", line=dict(color=HIGHLIGHT, width=1.4, dash="dot")
        ))

    fig = style_fig(fig, f"BMW {price_field} Price Over Time", height=480)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        vol_fig = px.bar(fdf, x="Date", y="Volume", color_discrete_sequence=[SECONDARY])
        vol_fig = style_fig(vol_fig, "Trading Volume", height=350)
        st.plotly_chart(vol_fig, use_container_width=True)
    with c2:
        yearly = fdf.set_index("Date")["Close"].resample("YE").mean().reset_index()
        yfig = px.bar(yearly, x="Date", y="Close", color_discrete_sequence=[HIGHLIGHT])
        yfig = style_fig(yfig, "Average Yearly Close", height=350)
        st.plotly_chart(yfig, use_container_width=True)

# ---- TAB 2: RETURNS & VOLATILITY ----
with tab2:
    st.markdown("### Daily Returns Distribution")
    rc1, rc2 = st.columns(2)
    with rc1:
        hist_fig = px.histogram(fdf, x="Daily_Return", nbins=80, color_discrete_sequence=[PRIMARY])
        hist_fig = style_fig(hist_fig, "Distribution of Daily Returns (%)", height=400)
        st.plotly_chart(hist_fig, use_container_width=True)
    with rc2:
        ret_fig = go.Figure()
        ret_fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["Daily_Return"], mode="lines",
                                      line=dict(color=DATA_LINE, width=0.8)))
        ret_fig = style_fig(ret_fig, "Daily Returns Over Time", height=400)
        st.plotly_chart(ret_fig, use_container_width=True)

    st.markdown("### Rolling Volatility")
    roll_window = st.slider("Rolling window (days) for volatility", 5, 90, 30)
    fdf["RollVol"] = fdf["Daily_Return"].rolling(roll_window).std()
    vfig = go.Figure()
    vfig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["RollVol"], mode="lines",
                               line=dict(color=SECONDARY, width=1.4), fill="tozeroy",
                               fillcolor="rgba(152,255,152,0.12)"))
    vfig = style_fig(vfig, f"{roll_window}-Day Rolling Volatility", height=400)
    st.plotly_chart(vfig, use_container_width=True)

# ---- TAB 3: CORRELATIONS ----
with tab3:
    st.markdown("### Feature Correlation Heatmap")
    num_cols = ["Open", "High", "Low", "Close", "Adj_Close", "Volume", "Daily_Return", "Price_Range"]
    corr = fdf[num_cols].corr()
    heat_fig = px.imshow(
        corr, text_auto=".2f", color_continuous_scale=[BG, HIGHLIGHT, DATA_LINE],
        aspect="auto"
    )
    heat_fig = style_fig(heat_fig, "Correlation Matrix", height=500)
    st.plotly_chart(heat_fig, use_container_width=True)

    st.markdown("### Price vs Volume Scatter")
    sc_fig = px.scatter(fdf, x="Volume", y="Close", color="Daily_Return",
                         color_continuous_scale=[PRIMARY, HIGHLIGHT, DATA_LINE])
    sc_fig = style_fig(sc_fig, "Close Price vs Volume", height=450)
    st.plotly_chart(sc_fig, use_container_width=True)

# ---- TAB 4: RAW DATA ----
with tab4:
    st.markdown("### Explore the Cleaned Dataset")
    search_cols = st.multiselect("Columns to display", df.columns.tolist(), default=df.columns.tolist())
    st.dataframe(fdf[search_cols], use_container_width=True, height=420)

    csv = fdf[search_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download filtered data as CSV", csv, "bmw_filtered.csv", "text/csv")

st.markdown(f"""
<hr>
<div style='text-align:center; color:{MUTED}; font-size:12px; padding-bottom:10px;'>
made with 💖 + 🧠 — BMW Stock Analytics Dashboard
</div>
""", unsafe_allow_html=True)