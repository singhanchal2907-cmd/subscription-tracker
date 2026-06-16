"""
Subscription & Expense Tracker — Streamlit version
Run: streamlit run subscription_tracker_streamlit.py
"""
import streamlit as st
import json
from pathlib import Path
from datetime import date, datetime

# ── Config ────────────────────────────────────────────────────────────────────
DATA_FILE = Path.home() / ".subscription_tracker_data.json"
USD_TO_INR = 83.5
CATEGORIES = ["Entertainment", "Productivity", "Health",
              "Finance", "Shopping", "Education", "Other"]

# ── Dark theme via CSS ────────────────────────────────────────────────────────
st.set_page_config(page_title="Subscription Tracker", page_icon="💸", layout="wide")

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    .stApp { background-color: #0f0f1a; color: #eaeaea; }
    section[data-testid="stSidebar"] { background-color: #16213e; }
    .block-container { padding-top: 1.5rem; }

    /* Banner metric cards */
    [data-testid="stMetric"] {
        background: #16213e;
        border-radius: 10px;
        padding: 14px 20px;
        border: 1px solid #1e2d50;
    }
    [data-testid="stMetricLabel"] { color: #9ea3b0 !important; font-size: 12px !important; }
    [data-testid="stMetricValue"] { color: #e94560 !important; font-size: 24px !important; }

    /* Form inputs */
    input, select, textarea {
        background-color: #0f3460 !important;
        color: #eaeaea !important;
        border: 1px solid #1e2d50 !important;
        border-radius: 6px !important;
    }
    label { color: #9ea3b0 !important; }

    /* Buttons */
    .stButton > button {
        background: #e94560;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.45rem 1.4rem;
        width: 100%;
    }
    .stButton > button:hover { background: #c73451; }

    /* Divider */
    hr { border-color: #1e2d50; }

    /* Sub card styles */
    .sub-card {
        background: #0f3460;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
        border-left: 4px solid #533483;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sub-card.safe  { border-left-color: #0fba81; }
    .sub-card.warn  { border-left-color: #f5a623; }
    .sub-card.over  { border-left-color: #e94560; }
    .sub-name  { color: #eaeaea; font-weight: 600; font-size: 14px; }
    .sub-cost  { color: #e94560; font-weight: 600; }
    .sub-meta  { color: #9ea3b0; font-size: 12px; }
    .days-safe { color: #0fba81; font-weight: 600; }
    .days-warn { color: #f5a623; font-weight: 600; }
    .days-over { color: #e94560; font-weight: 600; }
    .empty-state { text-align: center; color: #9ea3b0; padding: 60px 0; font-size: 15px; }
</style>
""", unsafe_allow_html=True)

# ── Data helpers ──────────────────────────────────────────────────────────────
def load():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save(subs):
    with open(DATA_FILE, "w") as f:
        json.dump(subs, f, indent=2)

def to_inr(cost, cur):
    return float(cost) * (USD_TO_INR if cur == "USD" else 1.0)

def days_until(ds):
    try:
        d = datetime.strptime(ds, "%Y-%m-%d").date()
        return (d - date.today()).days
    except Exception:
        return 9999

def fmt(n):
    return f"₹{n:,.2f}"

# ── Session state ─────────────────────────────────────────────────────────────
if "subs" not in st.session_state:
    st.session_state.subs = load()

subs = st.session_state.subs

# ── Sort ──────────────────────────────────────────────────────────────────────
subs_sorted = sorted(subs, key=lambda s: days_until(s.get("date", "")))

# ── Banner ────────────────────────────────────────────────────────────────────
monthly = sum(to_inr(s["cost"], s["cur"]) for s in subs)
yearly  = monthly * 12

st.markdown("## 💸 Subscription & Expense Tracker")
c1, c2, c3 = st.columns([1, 1, 3])
with c1:
    st.metric("Total Monthly Bleed", fmt(monthly))
with c2:
    st.metric("Total Yearly Bleed", fmt(yearly))

st.markdown("---")

# ── Layout: sidebar form + main list ─────────────────────────────────────────
col_form, col_list = st.columns([1, 2.5])

# ── Add form ──────────────────────────────────────────────────────────────────
with col_form:
    st.markdown("#### Add Subscription")
    name = st.text_input("Service name", placeholder="e.g. Netflix, Spotify")
    cost = st.number_input("Monthly cost", min_value=0.0, step=1.0, format="%.2f")
    cur  = st.radio("Currency", ["INR (₹)", "USD ($)"], horizontal=True)
    cur_code = "INR" if "INR" in cur else "USD"
    renewal  = st.date_input("Next renewal date", value=date.today())
    cat      = st.selectbox("Category", CATEGORIES)

    if st.button("＋ Add Subscription"):
        if not name.strip():
            st.error("Please enter a service name.")
        elif cost <= 0:
            st.error("Enter a cost greater than 0.")
        else:
            subs.append({
                "name": name.strip(),
                "cost": cost,
                "cur":  cur_code,
                "date": str(renewal),
                "cat":  cat,
            })
            save(subs)
            st.success(f"Added {name}!")
            st.rerun()

# ── Subscription list ─────────────────────────────────────────────────────────
with col_list:
    st.markdown("#### Active Subscriptions")

    if not subs_sorted:
        st.markdown('<div class="empty-state">No subscriptions yet.<br>Add one using the form.</div>',
                    unsafe_allow_html=True)
    else:
        for i, s in enumerate(subs_sorted):
            days = days_until(s.get("date", ""))
            status_cls = "over" if days < 0 else "warn" if days <= 7 else "safe"
            day_cls    = "days-over" if days < 0 else "days-warn" if days <= 7 else "days-safe"
            day_label  = f"{abs(days)}d overdue" if days < 0 else ("Today" if days == 0 else f"{days}d")
            inr_cost   = to_inr(s["cost"], s["cur"])

            row = st.columns([3, 2, 1.5, 1.5, 1.5, 1])
            row[0].markdown(f"**{s['name']}**")
            row[1].markdown(f"<span style='color:#e94560;font-weight:600'>{fmt(inr_cost)}/mo</span>", unsafe_allow_html=True)
            row[2].markdown(f"<span style='color:#9ea3b0'>{s['cur']}</span>", unsafe_allow_html=True)
            row[3].markdown(f"<span style='color:#9ea3b0'>{s.get('cat','—')}</span>", unsafe_allow_html=True)
            row[4].markdown(f"<span style='color:#eaeaea'>{s.get('date','—')}</span>", unsafe_allow_html=True)

            color = "#e94560" if days < 0 else ("#f5a623" if days <= 7 else "#0fba81")
            row[5].markdown(f"<span style='color:{color};font-weight:600'>{day_label}</span>",
                            unsafe_allow_html=True)

            # Unique key using index in original list
            orig_idx = subs.index(s) if s in subs else None
            if orig_idx is not None:
                if st.button("✕ Remove", key=f"del_{orig_idx}_{s['name']}"):
                    subs.pop(orig_idx)
                    save(subs)
                    st.rerun()

            st.markdown("<hr style='margin:6px 0;border-color:#1e2d50'>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;color:#533483;font-size:11px;margin-top:32px;padding-bottom:16px'>
Data auto-saved to ~/.subscription_tracker_data.json
</div>
""", unsafe_allow_html=True)
