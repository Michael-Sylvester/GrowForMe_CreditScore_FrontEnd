import streamlit as st
import pandas as pd
import requests
import json
import io
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GrowForMe · Credit Scoring",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --green-900: #0d2b1a;
    --green-800: #133d24;
    --green-700: #1a5230;
    --green-600: #1f6b3c;
    --green-500: #2a8a4f;
    --green-400: #3db870;
    --green-300: #6ed49a;
    --green-200: #a8f0c6;
    --green-100: #d6fae8;
    --cream:     #f7f4ee;
    --sand:      #e8e2d5;
    --bark:      #7a6a52;
    --ink:       #1a1a1a;
    --muted:     #5a5a5a;
    --white:     #ffffff;
    --accent:    #e8a020;
    --danger:    #c0392b;
    --warn:      #d4760d;
    --good:      #1a8f4f;
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

/* App background */
.stApp {
    background: var(--cream);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--green-900);
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: var(--green-100) !important;
}
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] .stSelectbox > label {
    color: var(--green-300) !important;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
[data-testid="stSidebar"] hr {
    border-color: var(--green-700) !important;
    margin: 1.2rem 0;
}

/* ── Hero header ── */
.hero-header {
    background: linear-gradient(135deg, var(--green-800) 0%, var(--green-600) 60%, var(--green-500) 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.03);
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: var(--white);
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 0.95rem;
    color: var(--green-200);
    margin: 0;
    font-weight: 300;
}

/* ── Cards ── */
.card {
    background: var(--white);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 1.2rem;
}
.card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: var(--green-800);
    margin: 0 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid var(--green-100);
}

/* ── Farmer nav pills ── */
.farmer-nav {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--white);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.farmer-badge {
    background: var(--green-100);
    color: var(--green-800);
    border-radius: 6px;
    padding: 0.25rem 0.7rem;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.farmer-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: var(--ink);
}
.farmer-meta {
    font-size: 0.82rem;
    color: var(--muted);
    margin-left: auto;
    font-family: 'DM Mono', monospace;
}

/* ── Score display ── */
.score-ring-wrap {
    text-align: center;
    padding: 1.5rem 0;
}
.score-value {
    font-family: 'DM Serif Display', serif;
    font-size: 4rem;
    line-height: 1;
    margin: 0;
}
.score-band {
    display: inline-block;
    border-radius: 20px;
    padding: 0.3rem 1.2rem;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.5rem;
}
.band-excellent { background: #d1fae5; color: #065f46; }
.band-good      { background: #dcfce7; color: #166534; }
.band-fair      { background: #fef9c3; color: #854d0e; }
.band-poor      { background: #fee2e2; color: #991b1b; }

/* ── Feature driver bars ── */
.driver-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.7rem;
}
.driver-label {
    font-size: 0.82rem;
    font-weight: 500;
    width: 160px;
    flex-shrink: 0;
    color: var(--ink);
    font-family: 'DM Mono', monospace;
}
.driver-bar-bg {
    flex: 1;
    background: var(--green-100);
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
}
.driver-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--green-500), var(--green-400));
    transition: width 0.6s ease;
}
.driver-val {
    font-size: 0.78rem;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    width: 50px;
    text-align: right;
}

/* ── Data table tweaks ── */
.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--green-600) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.55rem 1.4rem !important;
    transition: background 0.2s ease, transform 0.1s ease !important;
}
.stButton > button:hover {
    background: var(--green-500) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Download button */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--green-700) !important;
    border: 2px solid var(--green-500) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover {
    background: var(--green-100) !important;
}

/* ── Reasoning box ── */
.reasoning-box {
    background: var(--green-100);
    border-left: 3px solid var(--green-500);
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    font-size: 0.88rem;
    line-height: 1.6;
    color: var(--green-900);
    margin-top: 0.8rem;
    font-family: 'DM Sans', sans-serif;
}

/* ── Info chips ── */
.info-chip {
    display: inline-block;
    background: var(--sand);
    color: var(--bark);
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.15rem;
    font-family: 'DM Mono', monospace;
}

/* ── Step indicators ── */
.step-row {
    display: flex;
    gap: 0;
    margin-bottom: 2rem;
    align-items: center;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.step-dot {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
}
.step-dot.done { background: var(--green-500); color: white; }
.step-dot.active { background: var(--accent); color: white; }
.step-dot.pending { background: var(--sand); color: var(--bark); }
.step-label { font-size: 0.8rem; color: var(--muted); }
.step-line { flex: 1; height: 2px; background: var(--sand); margin: 0 0.5rem; }

/* ── Upload area ── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--green-300) !important;
    border-radius: 12px !important;
    background: var(--green-100) !important;
    padding: 1rem !important;
}

/* ── Metric overrides ── */
[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    color: var(--green-800) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
}

/* Hide default streamlit header padding on main */
.block-container {
    padding-top: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Constants ───────────────────────────────────────────────────────────────

ENDPOINTS = {
    "ML-based (XGBoost)": "/score/xgboost",
    "Rule-based":          "/score/rule-based",
}

RESPONSE_KEY = {
    "ML-based (XGBoost)": "xgboost",
    "Rule-based":          "rule_based",
}

DEFAULT_BASE_URL = "http://localhost:8000"

# Boolean sentinel values in the raw CSV
_BOOL_VALS = {"TRUE", "FALSE"}


def _parse_raw_line(line: str) -> dict:
    """
    Parse one raw CSV data line (already split on commas) into a clean dict.

    The CSV is malformed because `crop_types` and `yield_data` contain
    unquoted commas, making a naive pd.read_csv() shift every column after
    them. We parse positionally instead:

    Fixed positions (0-based):
      0   farmer_id
      1   farmer_name
      2   gender
      3   region
      4   drought_flood_index
      5   savings_ghs
      6   savings_usd          (not sent to API)
      7   payment_frequency
      8   farmer_budget_ghs
      9…  crop_types           (1–3 values, ends when TRUE/FALSE is seen)
      +0  is_association_member
      +1  has_motorbike
      +2  acres
      +3  satellite_verified
      +4  repayment_rate
      +5… yield_data           (variable count; 13 fixed fields follow it)
      …
      -13 endorsements
      -12 irrigation_type
      -11 irrigation_scheme
      -10 market_access_index
      -9  training_sessions
      -8  livestock_value_usd
      -7  alternative_income_usd
      -6  insurance_type
      -5  insurance_subscription
      -4  digital_score
      -3  soil_health_index
      -2  credit_score         (not sent to API)
      -1  creditworthiness     (not sent to API)
    """
    vals = line.strip().split(",")
    idx = 0

    def take():
        nonlocal idx
        v = vals[idx]; idx += 1
        return v.strip()

    r = {}
    r["farmer_id"]            = take()
    r["farmer_name"]          = take()
    r["gender"]               = take()
    r["region"]               = take()
    r["drought_flood_index"]  = take()
    r["savings_ghs"]          = take()
    _savings_usd              = take()          # skip – not in API
    r["payment_frequency"]    = take()
    r["farmer_budget_ghs"]    = take()

    # crop_types: collect tokens until we hit TRUE/FALSE
    crops = []
    while idx < len(vals) and vals[idx].strip() not in _BOOL_VALS:
        crops.append(take())
    r["crop_types"] = ",".join(crops)

    r["is_association_member"] = take()
    r["has_motorbike"]         = take()
    r["acres"]                 = take()
    r["satellite_verified"]    = take()
    r["repayment_rate"]        = take()

    # yield_data: everything up to the 13 tail-fixed fields
    tail_count = 13   # endorsements … creditworthiness
    n_yield = len(vals) - idx - tail_count
    yield_vals = [take() for _ in range(n_yield)]
    r["yield_data"] = ",".join(yield_vals)

    r["endorsements"]           = take()
    r["irrigation_type"]        = take()
    r["irrigation_scheme"]      = take()
    r["market_access_index"]    = take()
    r["training_sessions"]      = take()
    r["livestock_value_ghs"]    = take()   # CSV calls it _usd but we pass as GHS
    r["alternative_income_ghs"] = take()
    r["insurance_type"]         = take()
    r["insurance_subscription"] = take()
    r["digital_score"]          = take()
    r["soil_health_index"]      = take()
    _credit_score               = take()   # already known – skip
    _creditworthiness           = take()   # already known – skip

    return r


def _coerce(val: str):
    """Convert a string token to the most appropriate native Python type."""
    if isinstance(val, str):
        u = val.strip().upper()
        if u == "TRUE":  return True
        if u == "FALSE": return False
        # Try int first, then float, then leave as string
        try:    return int(val)
        except ValueError: pass
        try:    return float(val)
        except ValueError: pass
    # numpy scalars → native Python
    import numpy as np
    if isinstance(val, (np.integer,)):  return int(val)
    if isinstance(val, (np.floating,)): return float(val)
    if isinstance(val, (np.bool_,)):    return bool(val)
    return val


def load_csv(file_obj) -> list[dict]:
    """
    Read the uploaded CSV and return a list of clean farmer dicts,
    correctly handling unquoted commas inside crop_types and yield_data.
    """
    content = file_obj.read().decode("utf-8")
    lines = [l for l in content.splitlines() if l.strip()]
    # skip header row
    rows = []
    for line in lines[1:]:
        parsed = _parse_raw_line(line)
        # coerce every value to native Python type
        rows.append({k: _coerce(v) for k, v in parsed.items()})
    return rows


def build_payload(farmer: dict) -> dict:
    """
    Build the exact JSON payload the FastAPI backend expects.
    Only includes fields the API accepts; all values are native Python types.
    """
    API_FIELDS = [
        "farmer_id", "farmer_name", "gender", "region",
        "drought_flood_index", "savings_ghs", "payment_frequency",
        "crop_types", "is_association_member", "has_motorbike",
        "acres", "satellite_verified", "repayment_rate",
        "yield_data", "endorsements", "irrigation_type",
        "irrigation_scheme", "market_access_index", "training_sessions",
        "livestock_value_ghs", "alternative_income_ghs", "insurance_type",
        "insurance_subscription", "digital_score", "soil_health_index",
        "farmer_budget_ghs",
    ]
    return {k: farmer[k] for k in API_FIELDS if k in farmer}

ENDPOINTS = {
    "ML-based (XGBoost)": "/score/xgboost",
    "Rule-based":          "/score/rule-based",
}

RESPONSE_KEY = {
    "ML-based (XGBoost)": "xgboost",
    "Rule-based":          "rule_based",
}

DEFAULT_BASE_URL = "http://localhost:8000"


# ─── Session State Init ───────────────────────────────────────────────────────
if "results"  not in st.session_state: st.session_state.results  = {}
if "page_idx" not in st.session_state: st.session_state.page_idx = 0
if "farmers"  not in st.session_state: st.session_state.farmers  = None  # list[dict]

# ─── Additional helpers ────────────────────────────────────────────────────────

def call_api(base_url: str, endpoint: str, payload: dict) -> dict | None:
    url = base_url.rstrip("/") + endpoint
    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to API at **{url}**. Is the server running?")
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The server took too long to respond.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API returned an error: {e.response.status_code} — {e.response.text}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return None


def band_class(band: str) -> str:
    b = (band or "").lower()
    if "excellent" in b: return "band-excellent"
    if "good"      in b: return "band-good"
    if "fair"      in b: return "band-fair"
    return "band-poor"


def score_color(score: float) -> str:
    if score >= 75: return "#1a8f4f"
    if score >= 55: return "#ca8a04"
    return "#c0392b"


def extract_top_features(reasoning: str) -> list[str]:
    """Best-effort extraction of feature names from the reasoning string."""
    import re
    lines = [l.strip() for l in reasoning.split("\n") if l.strip()]
    features = []
    for line in lines:
        clean = re.sub(r'^[\-\*\d\.\)]+\s*', '', line)
        if clean and len(clean) < 100:
            features.append(clean)
        if len(features) >= 3:
            break
    return features if features else ["See full reasoning below"]


def build_results_csv() -> str:
    rows = []
    for key, data in st.session_state.results.items():
        parts     = key.rsplit("_", 1)
        fid       = parts[0]
        model_lbl = "_".join(parts[1:]) if len(parts) > 1 else "—"
        feats     = data.get("features", [])
        rows.append({
            "farmer_id": fid,
            "model":     model_lbl,
            "score":     data.get("score", ""),
            "band":      data.get("band", ""),
            "feature_1": feats[0] if len(feats) > 0 else "",
            "feature_2": feats[1] if len(feats) > 1 else "",
            "feature_3": feats[2] if len(feats) > 2 else "",
            "reasoning": data.get("reasoning", ""),
        })
    if not rows:
        return ""
    return pd.DataFrame(rows).to_csv(index=False)


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1rem 0'>
        <p style='font-family: DM Serif Display, serif; font-size: 1.6rem; color: #6ed49a; margin: 0; line-height: 1'>GrowForMe</p>
        <p style='font-size: 0.72rem; color: #3db870; letter-spacing: 0.12em; text-transform: uppercase; margin: 0'>Credit Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; color:#3db870; margin-bottom:0.5rem'>API Configuration</p>", unsafe_allow_html=True)
    base_url = st.text_input("Base URL", value=DEFAULT_BASE_URL, label_visibility="collapsed",
                             placeholder="http://localhost:8000")

    st.markdown("---")
    st.markdown("<p style='font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; color:#3db870; margin-bottom:0.5rem'>Scoring Model</p>", unsafe_allow_html=True)
    model_choice = st.radio("Model", list(ENDPOINTS.keys()), label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<p style='font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; color:#3db870; margin-bottom:0.5rem'>About</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 0.78rem; color: #a8f0c6; line-height: 1.6'>
    Upload a farmer CSV, cycle through farmers, and get AI-powered credit scores from your scoring API.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.results:
        st.markdown("<p style='font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; color:#3db870; margin-bottom:0.5rem'>Export</p>", unsafe_allow_html=True)
        csv_data = build_results_csv()
        st.download_button(
            label="⬇ Download All Results",
            data=csv_data,
            file_name=f"credit_scores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
    <p class='hero-title'>🌱 Credit Scoring Dashboard</p>
    <p class='hero-sub'>Upload farmer data · select a model · view AI-driven credit insights</p>
</div>
""", unsafe_allow_html=True)

# ─── Step 1: Upload ───────────────────────────────────────────────────────────
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<p class='card-title'>① Upload Farmer Data</p>", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Drop your farmer_data.csv here",
    type=["csv"],
    label_visibility="collapsed",
)

if uploaded:
    try:
        farmers = load_csv(uploaded)
        st.session_state.farmers  = farmers
        st.session_state.page_idx = 0
        total = len(farmers)
        st.success(f"✅ Loaded **{total} farmer{'s' if total != 1 else ''}** from `{uploaded.name}`")
        with st.expander("Preview parsed data"):
            st.dataframe(pd.DataFrame(farmers), use_container_width=True, height=180)
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# ─── Step 2 + 3: Score & Results ─────────────────────────────────────────────
if st.session_state.farmers:
    farmers = st.session_state.farmers
    total   = len(farmers)
    idx     = st.session_state.page_idx
    farmer  = farmers[idx]

    # ── Farmer navigation ──
    st.markdown(f"""
    <div class='farmer-nav'>
        <span class='farmer-badge'>Farmer {idx + 1} of {total}</span>
        <span class='farmer-name'>{farmer.get('farmer_name', 'Unknown')}</span>
        <span class='farmer-meta'>ID: {farmer.get('farmer_id', '—')} &nbsp;|&nbsp; {farmer.get('region', '—')}</span>
    </div>
    """, unsafe_allow_html=True)

    nav_col1, _, nav_col3 = st.columns([1, 6, 1])
    with nav_col1:
        if st.button("◀ Prev", disabled=(idx == 0), use_container_width=True):
            st.session_state.page_idx -= 1
            st.rerun()
    with nav_col3:
        if st.button("Next ▶", disabled=(idx == total - 1), use_container_width=True):
            st.session_state.page_idx += 1
            st.rerun()

    # ── Two-column layout ──
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-title'>Farmer Profile</p>", unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        m1.metric("Gender",         farmer.get("gender", "—"))
        m2.metric("Region",         farmer.get("region", "—"))
        m1.metric("Farm Size",      f"{farmer.get('acres', '—')} ac")
        m2.metric("Repayment Rate", f"{farmer.get('repayment_rate', '—')}%")
        m1.metric("Digital Score",  farmer.get("digital_score", "—"))
        m2.metric("Soil Health",    farmer.get("soil_health_index", "—"))

        crops = farmer.get("crop_types", "")
        st.markdown("<p style='font-size:0.82rem; color: var(--muted); margin-top: 0.5rem'>Crops</p>", unsafe_allow_html=True)
        chip_html = "".join(f"<span class='info-chip'>{c.strip()}</span>" for c in str(crops).split(",") if c.strip())
        st.markdown(chip_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("🔍 View API Payload"):
            st.json(build_payload(farmer))

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<p class='card-title'>② Score with <em>{model_choice}</em></p>", unsafe_allow_html=True)

        farmer_id  = str(farmer.get("farmer_id", idx))
        result_key = f"{farmer_id}_{model_choice}"
        cached     = st.session_state.results.get(result_key)

        if st.button("🚀 Get Credit Score", use_container_width=True):
            payload  = build_payload(farmer)
            endpoint = ENDPOINTS[model_choice]
            with st.spinner("Calling scoring API…"):
                raw = call_api(base_url, endpoint, payload)

            if raw:
                resp_key   = RESPONSE_KEY[model_choice]
                model_data = raw.get(resp_key, raw)
                score      = model_data.get("score", 0)
                band       = model_data.get("band", "—")
                reasoning  = model_data.get("reasoning", "")
                features   = extract_top_features(reasoning)

                st.session_state.results[result_key] = {
                    "score":     score,
                    "band":      band,
                    "reasoning": reasoning,
                    "features":  features,
                }
                st.rerun()

        if cached:
            score     = cached["score"]
            band      = cached["band"]
            features  = cached["features"]
            reasoning = cached["reasoning"]

            color = score_color(score)
            bc    = band_class(band)
            st.markdown(f"""
            <div class='score-ring-wrap'>
                <p class='score-value' style='color:{color}'>{score:.1f}</p>
                <span class='score-band {bc}'>{band}</span>
                <p style='font-size:0.75rem; color: var(--muted); margin-top: 0.5rem'>out of 100</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<p style='font-size:0.82rem; font-weight:600; color:var(--green-800); margin:0.5rem 0 0.7rem'>Top Contributing Factors</p>", unsafe_allow_html=True)
            for i, feat in enumerate(features[:3]):
                bar_pct = max(30, 100 - i * 20)
                st.markdown(f"""
                <div class='driver-row'>
                    <span class='driver-label'>#{i+1} {feat[:30]}</span>
                    <div class='driver-bar-bg'>
                        <div class='driver-bar-fill' style='width:{bar_pct}%'></div>
                    </div>
                    <span class='driver-val'>{'High' if i==0 else 'Med' if i==1 else 'Low'}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='reasoning-box'>
                <strong>Model Reasoning</strong><br>
                {reasoning}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style='text-align:center; padding: 2rem; color: var(--muted)'>
                <p style='font-size:2.5rem; margin:0'>📊</p>
                <p>Click <strong>Get Credit Score</strong> to run the model for this farmer.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── All results summary ────────────────────────────────────────────────
    if st.session_state.results:
        st.markdown("<div class='card' style='margin-top:1.5rem'>", unsafe_allow_html=True)
        st.markdown("<p class='card-title'>③ All Scored Farmers</p>", unsafe_allow_html=True)

        summary_rows = []
        for key, data in st.session_state.results.items():
            parts = key.split("_", 1)
            summary_rows.append({
                "Farmer ID":  parts[0],
                "Model":      parts[1] if len(parts) > 1 else "—",
                "Score":      f"{data['score']:.1f}",
                "Band":       data["band"],
                "Top Factor": data["features"][0] if data["features"] else "—",
            })

        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

        st.download_button(
            label="⬇ Download Results CSV",
            data=build_results_csv(),
            file_name=f"credit_scores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div style='text-align:center; padding: 4rem 2rem; color: var(--muted)'>
        <p style='font-size:3rem; margin:0'>🌾</p>
        <p style='font-family: DM Serif Display, serif; font-size:1.4rem; color: var(--green-700); margin:0.5rem 0'>Upload a CSV to get started</p>
        <p style='font-size:0.88rem'>Upload your <code>farmer_data.csv</code> above to begin scoring farmers.</p>
    </div>
    """, unsafe_allow_html=True)