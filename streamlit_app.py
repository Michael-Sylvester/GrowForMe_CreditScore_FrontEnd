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
.score-value{font-family:'DM Serif Display',serif;font-size:20rem;font-weight:bold;line-height:2;margin:0;text-shadow: 2px 2px 10px rgba(0,0,0,0.1);}
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
    vals = [v.strip() for v in line.strip().split(",")]
    idx  = 0
    def take():
        nonlocal idx; v = vals[idx]; idx += 1; return v

    r = {}
    r["farmer_id"]            = take()   # 1001
    r["farmer_name"]          = take()   # Ibrahim Tetteh
    r["gender"]               = take()   # male
    r["region"]               = take()   # Ashanti
    r["drought_flood_index"]  = take()   # 20.7
    r["savings_ghs"]          = take()   # 8198.10
    # The API error indicates that the CSV has farmer_budget_ghs before payment_frequency.
    r["farmer_budget_ghs"]    = take()
    r["payment_frequency"]    = take()
    
    # Crop types: consume until TRUE/FALSE
    crops = []
    while idx < len(vals) and vals[idx].lower() not in {"true", "false"}:
        crops.append(take())
    r["crop_types"] = ",".join(crops)   # "staple,cash_crop,vegetable"

    r["is_association_member"] = take()  # TRUE
    r["has_motorbike"]         = take()  # FALSE
    r["acres"]                 = take()  # 2.5
    r["satellite_verified"]    = take()  # TRUE
    r["repayment_rate"]        = take()  # 95.5

    # Yield: consume only tokens with a decimal point — stops at plain int (endorsements)
    yields = []
    while idx < len(vals) and "." in vals[idx]:
        try:
            float(vals[idx]); yields.append(take())
        except ValueError:
            break
    r["yield_data"] = ",".join(yields)   # "111.3,133.0,125.9"

    r["endorsements"]        = take()   # 3
    r["irrigation_type"]     = take()   # canal
    r["irrigation_scheme"]   = take()   # FALSE
    r["market_access_index"] = take()   # 100.0
    r["training_sessions"]   = take()   # 8
    # CSV has USD values here — convert to GHS using a 1:1 passthrough
    # (API field name says GHS but CSV only has USD; send as-is, values are still useful)
    r["livestock_value_ghs"]    = take()  # 191.44 (was Livestock Value Usd)
    r["alternative_income_ghs"] = take()  # 39.05  (was Alternative Income Usd)
    r["insurance_type"]         = take()  # both
    r["insurance_subscription"] = take()  # TRUE
    r["digital_score"]          = take()  # 100.0
    r["soil_health_index"]      = take()  # 75.9
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
        "payment_frequency","farmer_budget_ghs","crop_types","is_association_member","has_motorbike","acres",
        "satellite_verified","repayment_rate","yield_data","endorsements","irrigation_type",
        "irrigation_scheme","market_access_index","training_sessions","livestock_value_ghs",
        "alternative_income_ghs","insurance_type","insurance_subscription","digital_score",
        "soil_health_index"
    ]
    return {k: farmer[k] for k in API_FIELDS if k in farmer}

def create_farmer_form(default_farmer=None, form_key="farmer_form"):
    """Create a form for farmer data input, pre-filled with default_farmer if provided."""
    with st.form(form_key):
        col1, col2 = st.columns(2)
        
        with col1:
            farmer_id = st.text_input("Farmer ID", value=str(default_farmer.get("farmer_id", "")) if default_farmer else "")
            farmer_name = st.text_input("Farmer Name", value=default_farmer.get("farmer_name", "") if default_farmer else "")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(default_farmer.get("gender", "Male")) if default_farmer and default_farmer.get("gender") in ["Male", "Female", "Other"] else 0)
            region = st.text_input("Region", value=default_farmer.get("region", "") if default_farmer else "")
            drought_flood_index = st.number_input("Drought Flood Index", value=float(default_farmer.get("drought_flood_index", 0)) if default_farmer else 0.0, step=0.1)
            savings_ghs = st.number_input("Savings (GHS)", value=float(default_farmer.get("savings_ghs", 0)) if default_farmer else 0.0, step=0.01)
            payment_frequency = st.number_input("Payment Frequency", value=int(default_farmer.get("payment_frequency", 0)) if default_farmer and str(default_farmer.get("payment_frequency", 0)).isdigit() else 0, step=1)
            crop_types = st.text_input("Crop Types (comma-separated)", value=default_farmer.get("crop_types", "") if default_farmer else "")
            is_association_member = st.checkbox("Is Association Member", value=bool(default_farmer.get("is_association_member", False)) if default_farmer else False)
            has_motorbike = st.checkbox("Has Motorbike", value=bool(default_farmer.get("has_motorbike", False)) if default_farmer else False)
            acres = st.number_input("Acres", value=float(default_farmer.get("acres", 0)) if default_farmer else 0.0, step=0.1)
            satellite_verified = st.checkbox("Satellite Verified", value=bool(default_farmer.get("satellite_verified", False)) if default_farmer else False)
            repayment_rate = st.number_input("Repayment Rate (%)", value=float(default_farmer.get("repayment_rate", 0)) if default_farmer else 0.0, step=0.1)
        
        with col2:
            yield_data = st.text_input("Yield Data (comma-separated)", value=default_farmer.get("yield_data", "") if default_farmer else "")
            endorsements = st.number_input("Endorsements", value=int(default_farmer.get("endorsements", 0)) if default_farmer and str(default_farmer.get("endorsements", 0)).isdigit() else 0, step=1)
            irrigation_type = st.text_input("Irrigation Type", value=default_farmer.get("irrigation_type", "") if default_farmer else "")
            irrigation_scheme = st.checkbox("Irrigation Scheme", value=bool(default_farmer.get("irrigation_scheme", False)) if default_farmer else False)
            market_access_index = st.number_input("Market Access Index", value=float(default_farmer.get("market_access_index", 0)) if default_farmer else 0.0, step=0.1)
            training_sessions = st.number_input("Training Sessions", value=int(default_farmer.get("training_sessions", 0)) if default_farmer and str(default_farmer.get("training_sessions", 0)).isdigit() else 0, step=1)
            livestock_value_ghs = st.number_input("Livestock Value (GHS)", value=float(default_farmer.get("livestock_value_ghs", 0)) if default_farmer else 0.0, step=0.01)
            alternative_income_ghs = st.number_input("Alternative Income (GHS)", value=float(default_farmer.get("alternative_income_ghs", 0)) if default_farmer else 0.0, step=0.01)
            insurance_type = st.text_input("Insurance Type", value=default_farmer.get("insurance_type", "") if default_farmer else "")
            insurance_subscription = st.checkbox("Insurance Subscription", value=bool(default_farmer.get("insurance_subscription", False)) if default_farmer else False)
            digital_score = st.number_input("Digital Score", value=float(default_farmer.get("digital_score", 0)) if default_farmer else 0.0, step=0.1)
            soil_health_index = st.number_input("Soil Health Index", value=float(default_farmer.get("soil_health_index", 0)) if default_farmer else 0.0, step=0.1)
            farmer_budget_ghs = st.number_input("Farmer Budget (GHS)", value=float(default_farmer.get("farmer_budget_ghs", 0)) if default_farmer else 0.0, step=0.01)
        
        submitted = st.form_submit_button("🚀 Get Credit Score", use_container_width=True)
        
        if submitted:
            farmer_data = {
                "farmer_id": farmer_id,
                "farmer_name": farmer_name,
                "gender": gender,
                "region": region,
                "drought_flood_index": drought_flood_index,
                "savings_ghs": savings_ghs,
                "payment_frequency": payment_frequency,
                "crop_types": crop_types,
                "is_association_member": is_association_member,
                "has_motorbike": has_motorbike,
                "acres": acres,
                "satellite_verified": satellite_verified,
                "repayment_rate": repayment_rate,
                "yield_data": yield_data,
                "endorsements": endorsements,
                "irrigation_type": irrigation_type,
                "irrigation_scheme": irrigation_scheme,
                "market_access_index": market_access_index,
                "training_sessions": training_sessions,
                "livestock_value_ghs": livestock_value_ghs,
                "alternative_income_ghs": alternative_income_ghs,
                "insurance_type": insurance_type,
                "insurance_subscription": insurance_subscription,
                "digital_score": digital_score,
                "soil_health_index": soil_health_index,
                "farmer_budget_ghs": farmer_budget_ghs,
            }
            return farmer_data
    return None

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

def call_batch_api(base_url, file_obj):
    url = base_url.rstrip("/") + "/score/batch/rule-based/csv"
    try:
        files = {'file': ('farmer_data.csv', file_obj, 'text/csv')}
        resp = requests.post(url, files=files, timeout=120)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to **{url}**. Render may be waking — wait ~30 s and retry.")
    except requests.exceptions.Timeout:
        st.error("Request timed out (120 s). Render may be starting up. Please retry.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return None

# ─── Reasoning Parser & Renderer ─────────────────────────────────────────────
def parse_reasoning(text):
    if not isinstance(text, str):
        text = str(text or "")
    r = {"positives":[],"drags":[],"whatif_feature":"","whatif_advice":"","whatif_upside":"","raw":text}
    pos_m = _re.search(r"(?:Top positive contributors|Positive factors|Strengths|Advantages):\s*(.+?)(?:\.\s*(?:Biggest drags|Opportunity gaps|Negative factors|Drawbacks|What-if|Recommendation|Suggested|Improvement):|$)", text, _re.IGNORECASE)
    if pos_m:
        for item in _re.split(r";\s*", pos_m.group(1)):
            item = item.strip().rstrip(".")
            m = _re.match(r"(.+?)\s*\(\+?([\d.]+)\)", item)
            r["positives"].append({"label": m.group(1).strip(), "value": float(m.group(2))} if m else {"label": item, "value": None})
    drag_m = _re.search(r"(?:Biggest drags|Opportunity gaps|Negative factors|Drawbacks):\s*(.+?)(?:\.\s*(?:What-if|Recommendation|Suggested|Improvement):|$)", text, _re.IGNORECASE)
    if drag_m:
        for item in _re.split(r";\s*", drag_m.group(1)):
            item = item.strip().rstrip(".")
            m = _re.match(r"(.+?)\s*\(-(?:opportunity\s*)?([\d.]+)\)", item)
            r["drags"].append({"label": m.group(1).strip(), "value": float(m.group(2))} if m else {"label": item, "value": None})
    wi_m = _re.search(r"(?:What-if|Recommendation|Suggested action|Improvement suggestion|Best improvement):\s*(.+)", text, _re.IGNORECASE | _re.DOTALL)
    if wi_m:
        wi = wi_m.group(1).strip()
        fm = _re.search(r"(?:Best single what-if change|Best improvement|Recommended change|Key recommendation):\s*(.+?)\s*(?:->|would|could)", wi, _re.IGNORECASE)
        am = _re.search(r"(?:->|would|could)\s*(.+?)(?:\.\s*(?:Estimated|Expected|Potential)|$)", wi, _re.IGNORECASE)
        um = _re.search(r"(?:Estimated|Expected|Potential) (?:score )?upside:\s*\+?([\d.]+)", wi, _re.IGNORECASE)
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
        # Split raw reasoning on semi-colons and display as bullet list
        items = [item.strip() for item in raw.split(';') if item.strip()]
        if len(items) > 1:
            items_html = "".join(f"<div style='margin-bottom: 0.5rem;'>• {item}</div>" for item in items)
            st.markdown(f"<div class='reasoning-box'><strong>Model Reasoning</strong><br>{items_html}</div>", unsafe_allow_html=True)
        else:
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

# ─── Page Navigation Callbacks ────────────────────────────────────────────────
def next_farmer():
    st.session_state.page_idx += 1

def prev_farmer():
    st.session_state.page_idx -= 1


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

def safe_float(val, default=0.0):
    try: return float(val) if val is not None else default
    except (ValueError, TypeError): return default

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
if "batch_results" not in st.session_state: st.session_state.batch_results = None
if "raw_csv" not in st.session_state: st.session_state.raw_csv = None

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
        uploaded.seek(0)
        current_file_bytes = uploaded.read()
        
        # Only re-parse and reset if the user uploaded a new file
        if st.session_state.raw_csv != current_file_bytes:
            st.session_state.raw_csv = current_file_bytes
            uploaded.seek(0)
            st.session_state.farmers = load_csv(uploaded)
            st.session_state.page_idx = 0
            st.session_state.results  = {}
            st.session_state.batch_results = None
            
        st.success(f"✅ Loaded **{len(st.session_state.farmers)} farmer{'s' if len(st.session_state.farmers)!=1 else ''}** from `{uploaded.name}`")
        with st.expander("Preview parsed data"):
            st.dataframe(pd.DataFrame(st.session_state.farmers), use_container_width=True, height=180)
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")
st.markdown("</div>", unsafe_allow_html=True)

farmers      = st.session_state.farmers if st.session_state.farmers else []
total        = len(farmers)
results      = st.session_state.results

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab_rule, tab_ml, tab_batch, tab_summary = st.tabs(["Rule-based Scoring", "ML-based Scoring", "Batch Processing", "Results Summary"])

# ══════════ TAB 1 — Rule-based Scoring ═══════════════════════════════════════
with tab_rule:
    st.markdown("<div class='card'><p class='card-title'>📋 Rule-based Scoring</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.88rem;color:var(--muted);margin-bottom:1rem'>Fill the form with farmer data (pre-filled from CSV if uploaded) and get a rule-based credit score.</p>", unsafe_allow_html=True)
    
    default_farmer = farmers[0] if farmers else None
    farmer_data = create_farmer_form(default_farmer, "rule_form")
    
    if farmer_data:
        fid = str(farmer_data["farmer_id"])
        rk = rkey(fid, "Rule-based")
        
        with st.spinner("Scoring… (cold-start may take ~30 s)"):
            raw = call_api(base_url, ENDPOINTS["Rule-based"], build_payload(farmer_data))
        
        if raw:
            md = raw.get(RESPONSE_KEY["Rule-based"], raw)
            sc = safe_float(md.get("score", 0))
            bd = str(md.get("band", "—") or "—")
            rs = str(md.get("reasoning", "") or "")
            st.session_state.results[rk] = {"score": sc, "band": bd, "reasoning": rs}
            st.markdown(f"<div class='score-ring-wrap'><div style=\"font-family:'DM Serif Display',serif;font-size:7rem;font-weight:bold;line-height:1;color:{score_color(sc)};text-shadow:2px 2px 10px rgba(0,0,0,0.1);margin-bottom:0.5rem;\">{sc:.1f}</div><span class='score-band {band_class(bd)}'>{bd}</span><p style='font-size:0.75rem;color:var(--muted);margin-top:0.5rem'>out of 100</p></div>", unsafe_allow_html=True)
            render_reasoning(parse_reasoning(rs))
        else:
            st.error("Failed to get score. Please try again.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════ TAB 2 — ML-based Scoring ══════════════════════════════════════════
with tab_ml:
    st.markdown("<div class='card'><p class='card-title'>🤖 ML-based Scoring</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.88rem;color:var(--muted);margin-bottom:1rem'>Fill the form with farmer data (pre-filled from CSV if uploaded) and get an ML-based credit score.</p>", unsafe_allow_html=True)
    
    default_farmer = farmers[0] if farmers else None
    farmer_data = create_farmer_form(default_farmer, "ml_form")
    
    if farmer_data:
        fid = str(farmer_data["farmer_id"])
        rk = rkey(fid, "ML-based (XGBoost)")
        
        with st.spinner("Scoring… (cold-start may take ~30 s)"):
            raw = call_api(base_url, ENDPOINTS["ML-based (XGBoost)"], build_payload(farmer_data))
        
        if raw:
            md = raw.get(RESPONSE_KEY["ML-based (XGBoost)"], raw)
            sc = safe_float(md.get("score", 0))
            bd = str(md.get("band", "—") or "—")
            rs = str(md.get("reasoning", "") or "")
            st.session_state.results[rk] = {"score": sc, "band": bd, "reasoning": rs}
            st.markdown(f"<div class='score-ring-wrap'><div style=\"font-family:'DM Serif Display',serif;font-size:7rem;font-weight:bold;line-height:1;color:{score_color(sc)};text-shadow:2px 2px 10px rgba(0,0,0,0.1);margin-bottom:0.5rem;\">{sc:.1f}</div><span class='score-band {band_class(bd)}'>{bd}</span><p style='font-size:0.75rem;color:var(--muted);margin-top:0.5rem'>out of 100</p></div>", unsafe_allow_html=True)
            render_reasoning(parse_reasoning(rs))
        else:
            st.error("Failed to get score. Please try again.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════ TAB 3 — Batch Processing ══════════════════════════════════════════
# ══════════ TAB 3 — Batch Processing ══════════════════════════════════════════
with tab_batch:
    st.markdown("<div class='card'><p class='card-title'>⚡ Batch Processing</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.88rem;color:var(--muted);margin-bottom:1rem'>Score all uploaded farmers using the rule-based model.</p>", unsafe_allow_html=True)

    if not st.session_state.farmers:
        st.info("Please upload farmer data first in the section above.")

    elif st.session_state.batch_results is not None:
        # ── Results already in session — show them ──────────────────────────
        batch_results = st.session_state.batch_results
        st.success(f"✅ Batch processing completed! {len(batch_results)} farmer(s) scored.")

        if batch_results:
            # Create a lookup for farmer names from the original upload
            name_lookup = {str(f.get("farmer_id", "")): f.get("farmer_name", "N/A") for f in st.session_state.farmers}

            st.markdown("<p style='font-weight: 600; font-size: 1.1rem; color: var(--green-800);'>Batch Results Breakdown</p>", unsafe_allow_html=True)
            
            dl_data = []
            for item in batch_results:
                fid = str(item.get("farmer_id", ""))
                fname = name_lookup.get(fid, "Unknown Farmer")
                score = safe_float(item.get("score", 0))
                band  = str(item.get("band", "—") or "—")
                reasoning = str(item.get("reasoning", "") or "")
                
                dl_data.append({"farmer_id": fid, "farmer_name": fname, "score": score, "band": band, "reasoning": reasoning})
                
                # Display the individual results beautifully in an expander instead of a DataFrame
                with st.expander(f"**{fname}** (ID: {fid}) · Score: {score:.1f} — {band}"):
                    st.markdown(f"<div style='text-align:center;padding:0.8rem 0'><span style='font-family:DM Serif Display,serif;font-size:2.5rem;color:{score_color(score)}'>{score:.1f}</span>&nbsp;<span class='score-band {band_class(band)}'>{band}</span></div>", unsafe_allow_html=True)
                    render_reasoning(parse_reasoning(reasoning))

            st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)
            col_dl, col_rst = st.columns([3, 1])
            with col_dl:
                dl_csv = pd.DataFrame(dl_data).to_csv(index=False) if dl_data else ""
                st.download_button("⬇ Download Batch Results", data=dl_csv,
                                   file_name=f"batch_scores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                   mime="text/csv", use_container_width=True)
            with col_rst:
                if st.button("Reset Batch", use_container_width=True):
                    st.session_state.batch_results = None
                    st.rerun()
        else:
            # This handles the case where the API returns an empty list of results
            st.warning("Batch processing ran successfully but returned no results.")

    else:
        # ── No results yet — show preview + process button ──────────────────
        st.markdown("### Farmer Data Preview")
        st.dataframe(pd.DataFrame(st.session_state.farmers), use_container_width=True, height=250)

        if st.button("Process Batch", use_container_width=True):
            import io
            raw = None
            with st.spinner("Processing batch… (may take several minutes)"):
                try:
                    # The raw CSV has a complex, variable structure.
                    # We parse it using `load_csv` (already done when uploaded),
                    # then rebuild a clean, standard CSV to send to the API.
                    farmers_data = st.session_state.get("farmers")
                    if not farmers_data:
                        st.error("No farmer data has been loaded or parsed. Please re-upload the file.")
                        st.stop()

                    # The API expects a CSV with columns in a specific order.
                    api_columns = [
                        "farmer_id", "farmer_name", "gender", "region", "drought_flood_index",
                        "savings_ghs", "payment_frequency", "farmer_budget_ghs", "crop_types",
                        "is_association_member", "has_motorbike", "acres", "satellite_verified",
                        "repayment_rate", "yield_data", "endorsements", "irrigation_type",
                        "irrigation_scheme", "market_access_index", "training_sessions",
                        "livestock_value_ghs", "alternative_income_ghs", "insurance_type",
                        "insurance_subscription", "digital_score", "soil_health_index"
                    ]
                    df = pd.DataFrame(farmers_data)
                    df_clean = df.reindex(columns=api_columns)

                    # Convert the clean DataFrame to CSV bytes and send.
                    clean_csv_bytes = df_clean.to_csv(index=False).encode('utf-8')
                    raw = call_batch_api(base_url, io.BytesIO(clean_csv_bytes))
                except Exception as e:
                    st.error(f"Failed to process or send CSV: {e}")

            if raw is not None:
                # The API schema might be a dict {"results": [...]} or directly a list
                if isinstance(raw, dict) and "results" in raw:
                    batch_res = raw["results"]
                elif isinstance(raw, list):
                    batch_res = raw
                else:
                    batch_res = [raw] if isinstance(raw, dict) else []

                # Validate that we got a list. If not, show an error.
                if not isinstance(batch_res, list):
                    st.error("Could not parse batch results. The API response did not contain a valid 'results' list.")
                    st.json(raw)
                else:
                    # Success: we have a list of results (it might be empty, which is fine).
                    # Update the main results dictionary for the summary tab.
                    for result in batch_res:
                        fid = str(result.get("farmer_id", ""))
                        # The result object from the batch API has a farmer_id.
                        # We only add it to the main results dict if the ID is not empty.
                        if fid:
                            st.session_state.results[rkey(fid, "Rule-based")] = {
                                "score":     safe_float(result.get("score", 0)),
                                "band":      str(result.get("band", "—") or "—"),
                                "reasoning": str(result.get("reasoning", "") or ""),
                            }
                    # Store the raw batch results in the session to update the UI, then trigger a refresh.
                    st.session_state.batch_results = batch_res
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════ TAB 4 — Results Summary ═══════════════════════════════════════════
with tab_summary:
    st.markdown("<div class='card'><p class='card-title'>📊 All Scored Farmers</p>", unsafe_allow_html=True)
    live_results = st.session_state.results
    if not live_results:
        st.info("No results yet. Score farmers in the other tabs first.")
    else:
        rows = []
        for key, data in live_results.items():
            fid, mdl = key.split("||", 1)
            name = next((f.get("farmer_name", fid) for f in farmers if str(f.get("farmer_id",""))==fid), fid)
            
            sc = safe_float(data.get("score", 0))
            bd = str(data.get("band", "—") or "—")
            rs = str(data.get("reasoning", "") or "")
            p    = parse_reasoning(rs)
            pos  = p.get("positives",[])
            drgs = p.get("drags",[])
            rows.append({
                "Farmer ID":    fid, "Farmer Name": name, "Model": mdl,
                "Score":        round(sc, 2), "Band": bd,
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
            sc = safe_float(data.get("score", 0))
            bd = str(data.get("band", "—") or "—")
            rs = str(data.get("reasoning", "") or "")
            with st.expander(f"**{name}** (ID {fid}) · {mdl} · {sc:.1f} — {bd}"):
                st.markdown(f"<div style='text-align:center;padding:0.8rem 0'><span style='font-family:DM Serif Display,serif;font-size:2.5rem;color:{score_color(sc)}'>{sc:.1f}</span>&nbsp;<span class='score-band {band_class(bd)}'>{bd}</span></div>", unsafe_allow_html=True)
                render_reasoning(parse_reasoning(rs))

        st.markdown("<hr style='margin:1rem 0'>", unsafe_allow_html=True)
        st.download_button("⬇ Download Results CSV", data=build_results_csv(live_results),
                           file_name=f"credit_scores_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)