import streamlit as st
import pandas as pd
import requests
import re as _re
from datetime import datetime

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GrowForMe · Credit Scoring",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
    --green-900:#0d2b1a; --green-800:#133d24; --green-700:#1a5230;
    --green-600:#1f6b3c; --green-500:#2a8a4f; --green-400:#3db870;
    --green-300:#6ed49a; --green-200:#a8f0c6; --green-100:#d6fae8;
    --cream:#f7f4ee; --sand:#e8e2d5; --bark:#7a6a52;
    --ink:#1a1a1a; --muted:#5a5a5a; --white:#ffffff;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink);}
.stApp{background:var(--cream);}
[data-testid="stSidebar"]{background:var(--green-900);}
[data-testid="stSidebar"] *{color:var(--green-100) !important;}
[data-testid="stSidebar"] hr{border-color:var(--green-700) !important;margin:1.2rem 0;}
.hero-header{background:linear-gradient(135deg,var(--green-800) 0%,var(--green-600) 60%,var(--green-500) 100%);border-radius:16px;padding:2.5rem 3rem;margin-bottom:2rem;position:relative;overflow:hidden;}
.hero-title{font-family:'DM Serif Display',serif;font-size:2.4rem;color:#fff;margin:0 0 0.4rem;line-height:1.1;}
.hero-sub{font-size:0.95rem;color:var(--green-200);margin:0;font-weight:300;}
.card{background:var(--white);border-radius:12px;padding:1.5rem;box-shadow:0 1px 4px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.04);margin-bottom:1.2rem;}
.card-title{font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--green-800);margin:0 0 1rem;padding-bottom:0.6rem;border-bottom:2px solid var(--green-100);}
.farmer-nav{display:flex;align-items:center;gap:0.5rem;background:var(--white);border-radius:10px;padding:0.8rem 1rem;margin-bottom:1.5rem;box-shadow:0 1px 4px rgba(0,0,0,0.06);}
.farmer-badge{background:var(--green-100);color:var(--green-800);border-radius:6px;padding:0.25rem 0.7rem;font-size:0.78rem;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;}
.farmer-name{font-family:'DM Serif Display',serif;font-size:1.3rem;color:var(--ink);}
.farmer-meta{font-size:0.82rem;color:var(--muted);margin-left:auto;font-family:'DM Mono',monospace;}
.score-ring-wrap{text-align:center;padding:1.5rem 0;}
.score-value{font-family:'DM Serif Display',serif;font-size:4rem;line-height:1;margin:0;}
.score-band{display:inline-block;border-radius:20px;padding:0.3rem 1.2rem;font-size:0.85rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-top:0.5rem;}
.band-excellent{background:#d1fae5;color:#065f46;}
.band-good{background:#dcfce7;color:#166534;}
.band-fair{background:#fef9c3;color:#854d0e;}
.band-poor{background:#fee2e2;color:#991b1b;}
.driver-row{display:flex;align-items:center;gap:0.8rem;margin-bottom:0.7rem;}
.driver-label{font-size:0.8rem;font-weight:500;width:160px;flex-shrink:0;color:var(--ink);font-family:'DM Mono',monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.driver-bar-bg{flex:1;background:var(--green-100);border-radius:4px;height:8px;overflow:hidden;}
.driver-bar-fill{height:100%;border-radius:4px;}
.driver-val{font-size:0.78rem;font-family:'DM Mono',monospace;width:52px;text-align:right;}
.insight-section{border-radius:10px;margin:0.7rem 0;overflow:hidden;border:1px solid rgba(0,0,0,0.07);}
.insight-header{display:flex;align-items:center;gap:0.5rem;padding:0.5rem 0.85rem;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;}
.insight-icon{font-size:0.95rem;}
.positive-header{background:#dcfce7;color:#14532d;}
.drag-header{background:#fee2e2;color:#7f1d1d;}
.whatif-header{background:#fef9c3;color:#713f12;}
.insight-body{padding:0.75rem 0.85rem;background:var(--white);}
.whatif-feature{font-family:'DM Serif Display',serif;font-size:1rem;color:var(--green-800);margin-bottom:0.3rem;}
.whatif-advice{font-size:0.85rem;color:var(--ink);line-height:1.55;}
.upside-badge{display:inline-block;background:#fef08a;color:#713f12;border-radius:20px;padding:0.12rem 0.6rem;font-size:0.7rem;font-weight:700;letter-spacing:0.04em;margin-left:0.4rem;vertical-align:middle;}
.reasoning-box{background:var(--green-100);border-left:3px solid var(--green-500);border-radius:0 8px 8px 0;padding:0.9rem 1.1rem;font-size:0.88rem;line-height:1.6;color:var(--green-900);margin-top:0.8rem;}
.info-chip{display:inline-block;background:var(--sand);color:var(--bark);border-radius:6px;padding:0.2rem 0.6rem;font-size:0.75rem;font-weight:500;margin:0.15rem;font-family:'DM Mono',monospace;}
.stButton > button{background:var(--green-600) !important;color:white !important;border:none !important;border-radius:8px !important;font-weight:600 !important;transition:background 0.2s ease !important;}
.stButton > button:hover{background:var(--green-500) !important;}
.stDownloadButton > button{background:transparent !important;color:var(--green-700) !important;border:2px solid var(--green-500) !important;border-radius:8px !important;font-weight:600 !important;}
.stDownloadButton > button:hover{background:var(--green-100) !important;}
[data-testid="stFileUploader"]{border:2px dashed var(--green-300) !important;border-radius:12px !important;background:var(--green-100) !important;}
[data-testid="stMetricValue"]{font-family:'DM Serif Display',serif !important;color:var(--green-800) !important;}
.block-container{padding-top:2rem !important;}
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
DEFAULT_BASE_URL = "https://grow4me.onrender.com"
BOOL_VALS        = {"TRUE", "FALSE"}
ENDPOINTS        = {"ML-based (XGBoost)": "/score/xgboost", "Rule-based": "/score/rule-based"}
RESPONSE_KEY     = {"ML-based (XGBoost)": "xgboost",        "Rule-based": "rule_based"}

# ─── CSV Parser ───────────────────────────────────────────────────────────────
def _parse_raw_line(line):
    vals = line.strip().split(",")
    idx  = 0
    def take():
        nonlocal idx
        v = vals[idx]; idx += 1; return v.strip()
    r = {}
    r["farmer_id"]            = take()
    r["farmer_name"]          = take()
    r["gender"]               = take()
    r["region"]               = take()
    r["drought_flood_index"]  = take()
    r["savings_ghs"]          = take()
    take()                                   # savings_usd – skip
    r["payment_frequency"]    = take()
    r["farmer_budget_ghs"]    = take()
    crops = []
    while idx < len(vals) and vals[idx].strip() not in BOOL_VALS:
        crops.append(take())
    r["crop_types"]            = ",".join(crops)
    r["is_association_member"] = take()
    r["has_motorbike"]         = take()
    r["acres"]                 = take()
    r["satellite_verified"]    = take()
    r["repayment_rate"]        = take()
    n_yield = len(vals) - idx - 13
    r["yield_data"]             = ",".join([take() for _ in range(max(n_yield, 1))])
    r["endorsements"]           = take()
    r["irrigation_type"]        = take()
    r["irrigation_scheme"]      = take()
    r["market_access_index"]    = take()
    r["training_sessions"]      = take()
    r["livestock_value_ghs"]    = take()
    r["alternative_income_ghs"] = take()
    r["insurance_type"]         = take()
    r["insurance_subscription"] = take()
    r["digital_score"]          = take()
    r["soil_health_index"]      = take()
    take(); take()                           # credit_score, creditworthiness – skip
    return r

def _coerce(val):
    if isinstance(val, str):
        u = val.strip().upper()
        if u == "TRUE":  return True
        if u == "FALSE": return False
        try:    return int(val)
        except: pass
        try:    return float(val)
        except: pass
    return val

def load_csv(file_obj):
    content = file_obj.read().decode("utf-8")
    lines   = [l for l in content.splitlines() if l.strip()]
    return [{k: _coerce(v) for k, v in _parse_raw_line(line).items()} for line in lines[1:]]

def build_payload(farmer):
    API_FIELDS = [
        "farmer_id","farmer_name","gender","region","drought_flood_index","savings_ghs",
        "payment_frequency","crop_types","is_association_member","has_motorbike","acres",
        "satellite_verified","repayment_rate","yield_data","endorsements","irrigation_type",
        "irrigation_scheme","market_access_index","training_sessions","livestock_value_ghs",
        "alternative_income_ghs","insurance_type","insurance_subscription","digital_score",
        "soil_health_index","farmer_budget_ghs",
    ]
    return {k: farmer[k] for k in API_FIELDS if k in farmer}

# ─── API Call ─────────────────────────────────────────────────────────────────
def call_api(base_url, endpoint, payload):
    url = base_url.rstrip("/") + endpoint
    try:
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to **{url}**. Render may be waking — wait ~30 s and retry.")
    except requests.exceptions.Timeout:
        st.error("Request timed out (60 s). Render may be starting up. Please retry.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return None

# ─── Reasoning Parser & Renderer ─────────────────────────────────────────────
def parse_reasoning(text):
    r = {"positives":[],"drags":[],"whatif_feature":"","whatif_advice":"","whatif_upside":"","raw":text}
    pos_m = _re.search(r"Top positive contributors:\s*(.+?)(?:\.\s*Biggest drags:|$)", text, _re.IGNORECASE)
    if pos_m:
        for item in _re.split(r";\s*", pos_m.group(1)):
            item = item.strip().rstrip(".")
            m = _re.match(r"(.+?)\s*\(\+?([\d.]+)\)", item)
            r["positives"].append({"label": m.group(1).strip(), "value": float(m.group(2))} if m else {"label": item, "value": None})
    drag_m = _re.search(r"Biggest drags:\s*(.+?)(?:\.\s*What-if:|$)", text, _re.IGNORECASE)
    if drag_m:
        for item in _re.split(r";\s*", drag_m.group(1)):
            item = item.strip().rstrip(".")
            m = _re.match(r"(.+?)\s*\(-(?:opportunity\s*)?([\d.]+)\)", item)
            r["drags"].append({"label": m.group(1).strip(), "value": float(m.group(2))} if m else {"label": item, "value": None})
    wi_m = _re.search(r"What-if:(.+)", text, _re.IGNORECASE | _re.DOTALL)
    if wi_m:
        wi = wi_m.group(1).strip()
        fm = _re.search(r"Best single what-if change:\s*(.+?)\s*->", wi, _re.IGNORECASE)
        am = _re.search(r"->\s*(.+?)(?:\.\s*Estimated|$)", wi, _re.IGNORECASE)
        um = _re.search(r"Estimated score upside:\s*\+?([\d.]+)", wi, _re.IGNORECASE)
        if fm: r["whatif_feature"] = fm.group(1).strip()
        if am: r["whatif_advice"]  = am.group(1).strip()
        if um: r["whatif_upside"]  = um.group(1)
    return r

def render_reasoning(parsed):
    pos  = parsed.get("positives", [])
    drags= parsed.get("drags", [])
    wf   = parsed.get("whatif_feature", "")
    wa   = parsed.get("whatif_advice", "")
    wu   = parsed.get("whatif_upside", "")
    raw  = parsed.get("raw", "")
    if not pos and not drags and not wf:
        st.markdown(f"<div class='reasoning-box'><strong>Model Reasoning</strong><br>{raw}</div>", unsafe_allow_html=True)
        return
    if pos:
        items_html = ""
        for p in pos:
            val = (" (+%.2f)" % p["value"]) if p["value"] is not None else ""
            items_html += "<div style='margin-bottom: 0.5rem; color: #1a8f4f;'>• " + p["label"] + val + "</div>"
        st.markdown(
            "<div class='insight-section'><div class='insight-header positive-header'>"
            "<span class='insight-icon'>📈</span><span>Top Positive Contributors</span></div>"
            "<div class='insight-body'>" + items_html + "</div></div>",
            unsafe_allow_html=True,
        )
    if drags:
        items_html = ""
        for d in drags:
            val = (" (−%.2f)" % d["value"]) if d["value"] is not None else ""
            items_html += "<div style='margin-bottom: 0.5rem; color: #b91c1c;'>• " + d["label"] + val + "</div>"
        st.markdown(
            "<div class='insight-section'><div class='insight-header drag-header'>"
            "<span class='insight-icon'>📉</span><span>Opportunity Gaps</span></div>"
            "<div class='insight-body'>" + items_html + "</div></div>",
            unsafe_allow_html=True,
        )
    if wf or wa:
        badge = ("<span class='upside-badge'>+" + wu + " pts</span>") if wu else ""
        st.markdown(
            "<div class='insight-section'><div class='insight-header whatif-header'>"
            "<span class='insight-icon'>💡</span><span>Best What-If Action " + badge + "</span></div>"
            "<div class='insight-body'><div class='whatif-feature'>" + wf + "</div>"
            "<div class='whatif-advice'>" + wa + ".</div></div></div>",
            unsafe_allow_html=True,
        )

# ─── Misc helpers ─────────────────────────────────────────────────────────────
def band_class(band):
    b = (band or "").lower()
    if "excellent" in b: return "band-excellent"
    if "good"      in b: return "band-good"
    if "fair"      in b: return "band-fair"
    return "band-poor"

def score_color(score):
    if score >= 75: return "#1a8f4f"
    if score >= 55: return "#ca8a04"
    return "#c0392b"

def rkey(fid, model):
    return f"{fid}||{model}"

def build_results_csv(results):
    rows = []
    for key, data in results.items():
        fid, mdl = key.split("||", 1)
        p    = parse_reasoning(data.get("reasoning", ""))
        pos  = p.get("positives", [])
        drgs = p.get("drags", [])
        rows.append({
            "farmer_id":      fid, "model": mdl,
            "score":          data.get("score",""), "band": data.get("band",""),
            "top_positive_1": pos[0]["label"]  if len(pos)  > 0 else "",
            "top_positive_2": pos[1]["label"]  if len(pos)  > 1 else "",
            "top_positive_3": pos[2]["label"]  if len(pos)  > 2 else "",
            "top_drag_1":     drgs[0]["label"] if len(drgs) > 0 else "",
            "top_drag_2":     drgs[1]["label"] if len(drgs) > 1 else "",
            "whatif_feature": p.get("whatif_feature",""),
            "whatif_advice":  p.get("whatif_advice",""),
            "whatif_upside":  p.get("whatif_upside",""),
            "full_reasoning": data.get("reasoning",""),
        })
    return pd.DataFrame(rows).to_csv(index=False) if rows else ""

# ─── Session State ────────────────────────────────────────────────────────────
if "results"  not in st.session_state: st.session_state.results  = {}
if "page_idx" not in st.session_state: st.session_state.page_idx = 0
if "farmers"  not in st.session_state: st.session_state.farmers  = None

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='padding:0.5rem 0 1rem'><p style='font-family:DM Serif Display,serif;font-size:1.6rem;color:#6ed49a;margin:0;line-height:1'>GrowForMe</p><p style='font-size:0.72rem;color:#3db870;letter-spacing:0.12em;text-transform:uppercase;margin:0'>Credit Intelligence</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#3db870;margin-bottom:0.5rem'>API Endpoint</p>", unsafe_allow_html=True)
    base_url = st.text_input("Base URL", value=DEFAULT_BASE_URL, label_visibility="collapsed")
    try:
        _h = requests.get(base_url.rstrip("/") + "/health", timeout=5)
        indicator = "● API online" if _h.status_code == 200 else f"⚠ API responded {_h.status_code}"
        color_ind = "#6ed49a" if _h.status_code == 200 else "#f59e0b"
    except Exception:
        indicator, color_ind = "○ API unreachable (may be sleeping)", "#f87171"
    st.markdown(f"<span style='color:{color_ind};font-size:0.78rem'>{indicator}</span>", unsafe_allow_html=True)
    st.markdown(f"<a href='{base_url.rstrip('/')}/docs' target='_blank' style='font-size:0.72rem;color:#3db870;text-decoration:none'>📄 View API docs ↗</a>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#3db870;margin-bottom:0.5rem'>Scoring Model</p>", unsafe_allow_html=True)
    model_choice = st.radio("Model", list(ENDPOINTS.keys()), label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:0.78rem;color:#a8f0c6;line-height:1.6'>Powered by <strong style='color:#6ed49a'>grow4me.onrender.com</strong>.<br>Upload CSV · score farmers · download results.</div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.results:
        st.download_button("⬇ Download All Results", data=build_results_csv(st.session_state.results),
                           file_name=f"credit_scores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                           mime="text/csv", use_container_width=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='hero-header'><p class='hero-title'>🌱 Credit Scoring Dashboard</p><p class='hero-sub'>Upload farmer data · select a model · view AI-driven credit insights</p></div>", unsafe_allow_html=True)

# ─── Upload ───────────────────────────────────────────────────────────────────
st.markdown("<div class='card'><p class='card-title'>① Upload Farmer Data</p>", unsafe_allow_html=True)
uploaded = st.file_uploader("Drop your farmer_data.csv here", type=["csv"], label_visibility="collapsed")
if uploaded:
    try:
        farmers = load_csv(uploaded)
        st.session_state.farmers  = farmers
        st.session_state.page_idx = 0
        st.session_state.results  = {}
        st.success(f"✅ Loaded **{len(farmers)} farmer{'s' if len(farmers)!=1 else ''}** from `{uploaded.name}`")
        with st.expander("Preview parsed data"):
            st.dataframe(pd.DataFrame(farmers), use_container_width=True, height=180)
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")
st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.farmers:
    st.markdown("<div style='text-align:center;padding:4rem 2rem;color:var(--muted)'><p style='font-size:3rem;margin:0'>🌾</p><p style='font-family:DM Serif Display,serif;font-size:1.4rem;color:var(--green-700);margin:0.5rem 0'>Upload a CSV to get started</p><p style='font-size:0.88rem'>Upload your <code>farmer_data.csv</code> above to begin scoring farmers.</p></div>", unsafe_allow_html=True)
    st.stop()

farmers      = st.session_state.farmers
total        = len(farmers)
results      = st.session_state.results
ep           = ENDPOINTS[model_choice]
rk_model     = RESPONSE_KEY[model_choice]

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab_single, tab_bulk, tab_summary = st.tabs(["👤 Score One Farmer", "⚡ Score All Farmers", "📊 Results Summary"])

# ══════════ TAB 1 — Single farmer ════════════════════════════════════════════
with tab_single:
    idx    = st.session_state.page_idx
    farmer = farmers[idx]
    fid    = str(farmer.get("farmer_id", idx))
    rk     = rkey(fid, model_choice)

    st.markdown(f"<div class='farmer-nav'><span class='farmer-badge'>Farmer {idx+1} of {total}</span><span class='farmer-name'>{farmer.get('farmer_name','Unknown')}</span><span class='farmer-meta'>ID: {fid} &nbsp;|&nbsp; {farmer.get('region','—')}</span></div>", unsafe_allow_html=True)

    c1, _, c3 = st.columns([1,6,1])
    with c1:
        if st.button("◀ Prev", disabled=(idx==0), use_container_width=True):
            st.session_state.page_idx -= 1
            st.rerun()
    with c3:
        if st.button("Next ▶", disabled=(idx==total-1), use_container_width=True):
            st.session_state.page_idx += 1
            st.rerun()

    left, right = st.columns([1,1], gap="large")
    with left:
        st.markdown("<div class='card'><p class='card-title'>Farmer Profile</p>", unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        m1.metric("Gender",         farmer.get("gender","—"))
        m2.metric("Region",         farmer.get("region","—"))
        m1.metric("Farm Size",      f"{farmer.get('acres','—')} ac")
        m2.metric("Repayment Rate", f"{farmer.get('repayment_rate','—')}%")
        m1.metric("Digital Score",  farmer.get("digital_score","—"))
        m2.metric("Soil Health",    farmer.get("soil_health_index","—"))
        crops = str(farmer.get("crop_types",""))
        st.markdown("<p style='font-size:0.82rem;color:var(--muted);margin-top:0.5rem'>Crops</p>", unsafe_allow_html=True)
        st.markdown("".join(f"<span class='info-chip'>{c.strip()}</span>" for c in crops.split(",") if c.strip()), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("🔍 View API Payload"):
            st.json(build_payload(farmer))

    with right:
        st.markdown(f"<div class='card'><p class='card-title'>② Score with <em>{model_choice}</em></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.75rem;color:var(--muted);margin-bottom:0.5rem'>⚡ Hosted on Render — first request may take ~30 s to wake the server.</p>", unsafe_allow_html=True)

        if st.button("🚀 Get Credit Score", use_container_width=True, key="btn_single"):
            with st.spinner("Scoring… (cold-start may take ~30 s)"):
                raw = call_api(base_url, ep, build_payload(farmer))
            if raw:
                md = raw.get(rk_model, raw)
                st.session_state.results[rk] = {"score": md.get("score",0), "band": md.get("band","—"), "reasoning": md.get("reasoning","")}

        # Always read fresh from session_state (not the stale `results` copy)
        cached = st.session_state.results.get(rk)
        if cached:
            sc = cached["score"]; bd = cached["band"]; rs = cached["reasoning"]
            st.markdown(f"<div class='score-ring-wrap'><p class='score-value' style='color:{score_color(sc)}'>{sc:.1f}</p><span class='score-band {band_class(bd)}'>{bd}</span><p style='font-size:0.75rem;color:var(--muted);margin-top:0.5rem'>out of 100</p></div>", unsafe_allow_html=True)
            render_reasoning(parse_reasoning(rs))
        else:
            st.markdown("<div style='text-align:center;padding:2rem;color:var(--muted)'><p style='font-size:2.5rem;margin:0'>📊</p><p>Click <strong>Get Credit Score</strong> to run the model.</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════ TAB 2 — Bulk scoring ══════════════════════════════════════════════
with tab_bulk:
    st.markdown("<div class='card'><p class='card-title'>⚡ Score All Farmers</p>", unsafe_allow_html=True)
    already = sum(1 for f in farmers if rkey(str(f.get("farmer_id","")), model_choice) in results)
    st.markdown(f"<p style='font-size:0.88rem;color:var(--muted)'>{already} of {total} farmers already scored with <strong>{model_choice}</strong>.</p>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1,1])
    with col_a: run_all = st.button("🚀 Score All Farmers", use_container_width=True, key="btn_bulk")
    with col_b: rescore = st.checkbox("Re-score already scored farmers", value=False)

    if run_all:
        to_score = [f for f in farmers if rescore or rkey(str(f.get("farmer_id","")), model_choice) not in results]
        if not to_score:
            st.info("All farmers already scored. Check 'Re-score' to run again.")
        else:
            prog   = st.progress(0, text="Starting…")
            status = st.empty()
            errors = []
            for i, f in enumerate(to_score):
                fid  = str(f.get("farmer_id", i))
                name = f.get("farmer_name", f"Farmer {fid}")
                prog.progress(i / len(to_score), text=f"Scoring {name} ({i+1}/{len(to_score)})…")
                status.markdown(f"<div style='background:var(--green-100);border-radius:8px;padding:0.75rem 1rem;font-size:0.85rem;color:var(--green-800)'>⏳ Calling API for <strong>{name}</strong> (ID: {fid})…</div>", unsafe_allow_html=True)
                raw = call_api(base_url, ep, build_payload(f))
                if raw:
                    md = raw.get(rk_model, raw)
                    st.session_state.results[rkey(fid, model_choice)] = {"score": md.get("score",0), "band": md.get("band","—"), "reasoning": md.get("reasoning","")}
                else:
                    errors.append(f"{name} (ID: {fid})")
            prog.progress(1.0, text="Done!")
            status.empty()
            if errors:
                st.warning(f"⚠ {len(to_score)-len(errors)}/{len(to_score)} scored. Failed: " + ", ".join(errors))
            else:
                st.success(f"✅ All {len(to_score)} farmers scored successfully!")

    # Always read fresh from session_state for the display grid
    scored = [f for f in farmers if rkey(str(f.get("farmer_id","")), model_choice) in st.session_state.results]
    if scored:
        st.markdown("<hr style='margin:1rem 0'>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:0.82rem;font-weight:600;color:var(--green-800)'>{len(scored)} Scored Farmers</p>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, f in enumerate(scored):
            fid  = str(f.get("farmer_id",""))
            data = st.session_state.results[rkey(fid, model_choice)]
            sc   = data["score"]; bd = data["band"]
            with cols[i % 3]:
                st.markdown(
                    f"<div style='background:var(--white);border-radius:10px;padding:1rem;margin-bottom:0.8rem;border:1px solid var(--sand)'>"
                    f"<p style='font-family:DM Serif Display,serif;font-size:0.95rem;color:var(--ink);margin:0 0 0.2rem'>{f.get('farmer_name','—')}</p>"
                    f"<p style='font-size:0.72rem;color:var(--muted);margin:0 0 0.6rem;font-family:DM Mono,monospace'>ID: {fid} · {f.get('region','—')}</p>"
                    f"<span style='font-family:DM Serif Display,serif;font-size:1.8rem;color:{score_color(sc)}'>{sc:.1f}</span>"
                    f"&nbsp;<span class='score-band {band_class(bd)}' style='font-size:0.65rem'>{bd}</span></div>",
                    unsafe_allow_html=True,
                )
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════ TAB 3 — Summary ═══════════════════════════════════════════════════
with tab_summary:
    st.markdown("<div class='card'><p class='card-title'>📊 All Scored Farmers</p>", unsafe_allow_html=True)
    live_results = st.session_state.results
    if not live_results:
        st.info("No results yet. Score farmers in the other tabs first.")
    else:
        rows = []
        for key, data in live_results.items():
            fid, mdl = key.split("||", 1)
            p    = parse_reasoning(data.get("reasoning",""))
            pos  = p.get("positives",[])
            drgs = p.get("drags",[])
            rows.append({
                "Farmer ID":    fid, "Model": mdl,
                "Score":        round(data["score"],2), "Band": data["band"],
                "Top Positive": pos[0]["label"]  if pos  else "—",
                "Top Gap":      drgs[0]["label"] if drgs else "—",
                "What-If":      p.get("whatif_feature","—"),
                "Score Upside": f"+{p['whatif_upside']} pts" if p.get("whatif_upside") else "—",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown("<hr style='margin:1rem 0'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.88rem;font-weight:600;color:var(--green-800)'>Detailed Breakdown per Farmer</p>", unsafe_allow_html=True)
        for key, data in live_results.items():
            fid, mdl = key.split("||", 1)
            name = next((f.get("farmer_name", fid) for f in farmers if str(f.get("farmer_id",""))==fid), fid)
            sc   = data["score"]; bd = data["band"]
            with st.expander(f"**{name}** (ID {fid}) · {mdl} · {sc:.1f} — {bd}"):
                st.markdown(f"<div style='text-align:center;padding:0.8rem 0'><span style='font-family:DM Serif Display,serif;font-size:2.5rem;color:{score_color(sc)}'>{sc:.1f}</span>&nbsp;<span class='score-band {band_class(bd)}'>{bd}</span></div>", unsafe_allow_html=True)
                render_reasoning(parse_reasoning(data["reasoning"]))

        st.markdown("<hr style='margin:1rem 0'>", unsafe_allow_html=True)
        st.download_button("⬇ Download Results CSV", data=build_results_csv(live_results),
                           file_name=f"credit_scores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)