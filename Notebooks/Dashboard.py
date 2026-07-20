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
BG          = "#051F20"   # Very Dark Green
PRIMARY     = "#0B2B26"   # Deep Forest Green
SECONDARY   = "#163832"   # Dark Teal Green
HIGHLIGHT   = "#235347"   # Medium Green
DATA_LINE   = "#8EB69B"   # Soft Sage Green
TEXT        = "#8EB69B"   # Soft Sage Green (same as DATA_LINE)
MUTED       = "#163832"   # Reusing Dark Teal Green for muted tones
CARD_BG     = "#0B2B26"   # Deep Forest Green for card background

# ---------------------------------------------------------------
# CUSTOM CSS — cyberpunk trading-terminal skin (palette unchanged)
# ---------------------------------------------------------------
st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">

<style>
:root {{
    --hud-corner: {DATA_LINE};g
}}

html, body, [class*="css"] {{
    font-family: 'Share Tech Mono', monospace;
    color: {TEXT};
}}

/* App background — navy void + HUD scanline grid */
.stApp {{
    background-color: {BG};
    background-image:
        radial-gradient(circle at 85% 8%, rgba(0,255,255,0.10) 0%, rgba(0,255,255,0) 40%),
        radial-gradient(circle at 10% 90%, rgba(255,182,193,0.08) 0%, rgba(255,182,193,0) 45%),
        repeating-linear-gradient(0deg, rgba(0,255,255,0.035) 0px, rgba(0,255,255,0.035) 1px, transparent 1px, transparent 3px),
        repeating-linear-gradient(90deg, rgba(200,162,200,0.02) 0px, rgba(200,162,200,0.02) 1px, transparent 1px, transparent 48px);
    background-attachment: fixed;
}}

/* Ambient scanline sweep — one animated signature element, used sparingly */
.scan-sweep {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {DATA_LINE}, transparent);
    box-shadow: 0 0 12px 2px rgba(0,255,255,0.6);
    opacity: 0.5;
    z-index: 1;
    pointer-events: none;
    animation: sweep 7s linear infinite;
}}
@keyframes sweep {{
    0%   {{ top: 0%; opacity: 0; }}
    5%   {{ opacity: 0.5; }}
    95%  {{ opacity: 0.5; }}
    100% {{ top: 100%; opacity: 0; }}
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
    color: {HIGHLIGHT} !important;
    text-shadow: 0 0 18px rgba(255,182,193,0.45);
}}
h2, h3 {{
    color: {DATA_LINE} !important;
}}
h2::before, h3::before {{
    content: "// ";
    color: {DATA_LINE};
    opacity: 0.7;
}}

/* Sidebar — terminal control panel */
section[data-testid="stSidebar"] {{
    background-color: {CARD_BG};
    border-right: 1px solid rgba(142,182,155,0.25);
    box-shadow: inset -8px 0 24px rgba(142,182,155,0.08);
}}
section[data-testid="stSidebar"] * {{
    color: {TEXT} !important;
    font-family: 'Share Tech Mono', monospace !important;
}}

/* --- HUD corner-bracket frame, reused on metrics / charts / tables --- */
div[data-testid="stMetric"],
div[data-testid="stPlotlyChart"],
[data-testid="stDataFrame"] {{
    position: relative;
    background: {CARD_BG};
    border: 1px solid rgba(0,255,255,0.18);
    border-radius: 4px;
    box-shadow: 0 0 18px rgba(0,255,255,0.08);
}}
div[data-testid="stMetric"]::before,
div[data-testid="stPlotlyChart"]::before,
[data-testid="stDataFrame"]::before {{
    content: "";
    position: absolute;
    inset: 6px;
    pointer-events: none;
    background-image:
        linear-gradient(to right, var(--hud-corner) 2px, transparent 2px),
        linear-gradient(to bottom, var(--hud-corner) 2px, transparent 2px),
        linear-gradient(to left, var(--hud-corner) 2px, transparent 2px),
        linear-gradient(to bottom, var(--hud-corner) 2px, transparent 2px),
        linear-gradient(to right, var(--hud-corner) 2px, transparent 2px),
        linear-gradient(to top, var(--hud-corner) 2px, transparent 2px),
        linear-gradient(to left, var(--hud-corner) 2px, transparent 2px),
        linear-gradient(to top, var(--hud-corner) 2px, transparent 2px);
    background-size: 14px 14px;
    background-repeat: no-repeat;
    background-position: top left, top left, top right, top right, bottom left, bottom left, bottom right, bottom right;
    opacity: 0.85;
}}

div[data-testid="stMetric"] {{
    padding: 16px 18px;
}}
div[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
    font-family: 'Share Tech Mono', monospace !important;
    text-transform: uppercase;
    font-size: 12px !important;
    letter-spacing: 1px;
}}
div[data-testid="stMetricValue"] {{
    color: {DATA_LINE} !important;
    font-family: 'Orbitron', sans-serif !important;
    text-shadow: 0 0 10px rgba(0,255,255,0.5);
}}

/* Tabs — terminal command switches */
div[data-baseweb="tab-list"] {{
    border-bottom: 1px solid rgba(0,255,255,0.2) !important;
    gap: 4px;
}}
button[data-baseweb="tab"] {{
    font-family: 'Share Tech Mono', monospace !important;
    color: {MUTED} !important;
    background: rgba(0,255,255,0.03);
    border: 1px solid rgba(0,255,255,0.12) !important;
    border-radius: 4px 4px 0 0 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {PRIMARY} !important;
    background: rgba(255,182,193,0.06);
    border-color: rgba(255,182,193,0.4) !important;
    border-bottom: 2px solid {PRIMARY} !important;
    text-shadow: 0 0 8px rgba(255,182,193,0.4);
}}

/* Badge / logo block */
.bmw-badge {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 6px;
    position: relative;
    z-index: 1;
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
    color: {DATA_LINE};
    text-shadow: 0 0 16px rgba(255,182,193,0.5);
    letter-spacing: 1px;
}}
.bmw-title .cursor {{
    display: inline-block;
    color: {HIGHLIGHT};
    animation: blink 1.1s steps(1) infinite;
}}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
.bmw-subtitle {{
    font-family: 'Share Tech Mono', monospace;
    color: {MUTED};
    font-size: 13px;
    margin-top: -4px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}}
.bmw-subtitle span {{ color: {HIGHLIGHT}; }}

/* Ticker tape — scrolling live-feed strip */
.ticker-wrap {{
    position: relative;
    overflow: hidden;
    width: 100%;
    background: #10132A;
    border-top: 1px solid rgba(0,255,255,0.25);
    border-bottom: 1px solid rgba(0,255,255,0.25);
    box-shadow: 0 0 14px rgba(0,255,255,0.08) inset;
    padding: 8px 0;
    margin: 10px 0 18px 0;
}}
.ticker-track {{
    display: inline-block;
    white-space: nowrap;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    letter-spacing: 1px;
    animation: ticker 28s linear infinite;
    padding-left: 100%;
}}
.ticker-track span.tk-up {{ color: {SECONDARY}; text-shadow: 0 0 6px rgba(152,255,152,0.5); }}
.ticker-track span.tk-down {{ color: {PRIMARY}; text-shadow: 0 0 6px rgba(255,182,193,0.5); }}
.ticker-track span.tk-label {{ color: {MUTED}; }}
.ticker-track span.tk-sep {{ color: {HIGHLIGHT}; margin: 0 18px; }}
@keyframes ticker {{
    0%   {{ transform: translateX(0); }}
    100% {{ transform: translateX(-100%); }}
}}

/* Dataframe text */
[data-testid="stDataFrame"] * {{
    font-family: 'Share Tech Mono', monospace !important;
}}

/* Sliders / widgets accent */
div[data-baseweb="slider"] > div > div {{
    background: {DATA_LINE} !important;
}}

hr {{
    border-color: rgba(0,255,255,0.2);
}}
</style>

<div class="bmw-watermark">BMW</div>
<div class="scan-sweep"></div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# HEADER WITH STYLIZED BADGE (no copyrighted logo used)
# ---------------------------------------------------------------
st.markdown(f"""
<div class="bmw-badge">
    <div class="bmw-roundel">BMW</div>
    <div>
        <div class="bmw-title">&gt; BMW_STOCK_ANALYTICS<span class="cursor">_</span></div>
        <div class="bmw-subtitle">status: <span>live feed</span> &nbsp;//&nbsp; source: ohlcv.csv &nbsp;//&nbsp; protocol: navy-cyan</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Data/Clean/Final_BMW_dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df

df = load_data()

# ---------------------------------------------------------------
# LIVE TICKER TAPE — scrolling readout from the full dataset
# ---------------------------------------------------------------
_last, _prev = df.iloc[-1], df.iloc[-2]
_chg = _last["Close"] - _prev["Close"]
_pct = (_chg / _prev["Close"]) * 100
_dir = "tk-up" if _chg >= 0 else "tk-down"
_arrow = "▲" if _chg >= 0 else "▼"

_ticker_items = f"""
<span class="tk-label">LAST_CLOSE</span> {_last['Close']:.2f}
<span class="tk-sep">//</span>
<span class="{_dir}">{_arrow} {_chg:+.2f} ({_pct:+.2f}%)</span>
<span class="tk-sep">//</span>
<span class="tk-label">VOL</span> {_last['Volume']:,.0f}
<span class="tk-sep">//</span>
<span class="tk-label">HIGH</span> {_last['High']:.2f}
<span class="tk-sep">//</span>
<span class="tk-label">LOW</span> {_last['Low']:.2f}
<span class="tk-sep">//</span>
<span class="tk-label">AS_OF</span> {_last['Date'].strftime('%Y-%m-%d')}
"""
st.markdown(f"""
<div class="ticker-wrap">
    <div class="ticker-track">{_ticker_items * 3}</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# SIDEBAR — INTERACTIVE CONTROLS
# ---------------------------------------------------------------
with st.sidebar:
    st.markdown(f"<div class='bmw-roundel' style='margin-bottom:10px;'>BMW</div>", unsafe_allow_html=True)
    st.markdown("### $ controls")

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
        font=dict(family="Share Tech Mono, monospace", color=TEXT, size=12),
        title=dict(text=f"// {title}", font=dict(family="Orbitron, sans-serif", color=SECONDARY, size=17)) if title else None,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(family="Share Tech Mono, monospace")),
        height=height,
        margin=dict(t=60, l=10, r=10, b=10),
    )
    fig.update_xaxes(gridcolor="rgba(0,255,255,0.10)", zerolinecolor="rgba(0,255,255,0.15)", griddash="dot")
    fig.update_yaxes(gridcolor="rgba(0,255,255,0.10)", zerolinecolor="rgba(0,255,255,0.15)", griddash="dot")
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
k1.metric("LAST_CLOSE", f"{latest['Close']:.2f}")
k2.metric("PERIOD_Δ", f"{pct_change:+.2f}%")
k3.metric("HIGH_MAX", f"{fdf['Close'].max():.2f}")
k4.metric("LOW_MIN", f"{fdf['Close'].min():.2f}")
k5.metric("VOLATILITY_σ", f"{volatility:.2f}%")

st.markdown("")

# ---------------------------------------------------------------
# TABS
# ---------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📈 PRICE_TRENDS", "🎲 RETURNS_VOL", "🧬 CORRELATIONS", "🗂️ RAW_DATA"])

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
<div style='text-align:center; color:{MUTED}; font-size:12px; padding-bottom:10px; font-family:"Share Tech Mono", monospace; letter-spacing:1px;'>
&gt; END_OF_FEED <span style="color:{DATA_LINE};">_</span> &nbsp;//&nbsp; BMW_STOCK_ANALYTICS.TERMINAL
</div>
""", unsafe_allow_html=True)