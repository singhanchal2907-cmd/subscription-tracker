"""
╔══════════════════════════════════════════════════════════════╗
║   SubTrack Pro — B2B SaaS Subscription Intelligence Suite   ║
║   Production-Ready • Freemium Gated • Viral Growth Built-In ║
╚══════════════════════════════════════════════════════════════╝
Run: streamlit run saas_tracker.py
"""

import streamlit as st
import json
from pathlib import Path
from datetime import date, datetime, timedelta
import math

# ═══════════════════════════════════════════════════════════════
#  CONSTANTS & CONFIG
# ═══════════════════════════════════════════════════════════════
DATA_FILE         = Path("saas_tracker_data.json")
FREE_LIMIT        = 3
VALID_LICENSE_KEY = "MILLIONAIRE2026"
USD_TO_INR        = 85.0
EUR_TO_INR        = 92.0
USD_TO_EUR        = 0.92

CURRENCIES = ["INR (₹)", "USD ($)", "EUR (€)"]

CATEGORIES_PERSONAL = [
    "🎬 Entertainment", "🎵 Music", "📚 Education", "💪 Health & Fitness",
    "🛒 Shopping", "📰 News & Media", "🎮 Gaming", "☁️ Cloud Storage",
    "🔐 Security & VPN", "🍔 Food Delivery", "🚗 Transport", "💼 Other"
]

CATEGORIES_CORPORATE = [
    "☁️ Cloud Infrastructure", "💬 Communication", "🔧 DevOps & CI/CD",
    "📊 Analytics & BI", "🎨 Design & Creative", "🤝 CRM & Sales",
    "📣 Marketing & Ads", "🔐 Security & Compliance", "🧰 Productivity Suite",
    "📦 Logistics & Supply Chain", "💰 Finance & Accounting", "🏢 HR & Payroll"
]

RENEWAL_CYCLES = ["Monthly", "Annual"]

# ── Cheaper alternatives suggestion engine ──────────────────────
ALTERNATIVES = {
    "netflix":       ("Disney+ Hotstar", "₹1,499/yr vs ₹649/mo — save ~87%"),
    "spotify":       ("YouTube Music", "Free with YouTube Premium family plan"),
    "adobe":         ("Canva Pro", "₹3,999/yr vs ₹35,999/yr — save 89%"),
    "slack":         ("Discord or Zulip", "Free tiers cover most small teams"),
    "zoom":          ("Google Meet", "Free for 60-min meetings — zero cost"),
    "github":        ("GitLab Free Tier", "Unlimited private repos + CI minutes"),
    "jira":          ("Linear or Trello", "Free up to 10 users"),
    "aws":           ("Hetzner Cloud or DigitalOcean", "Up to 70% cheaper for same specs"),
    "salesforce":    ("HubSpot CRM", "Generous free tier for startups"),
    "microsoft 365": ("Google Workspace Starter", "~40% cheaper for teams <10"),
    "notion":        ("Obsidian + Logseq", "100% free, local-first"),
    "figma":         ("Penpot", "Open-source, fully free for teams"),
    "heroku":        ("Railway or Render", "More generous free tiers"),
    "dropbox":       ("Google Drive or Internxt", "15GB free vs 2GB"),
    "lastpass":      ("Bitwarden", "100% free, open-source, more secure"),
    "monday":        ("Asana Free or ClickUp", "Free forever plans available"),
    "hubspot":       ("Zoho CRM", "Free for 3 users, more features"),
    "mailchimp":     ("Brevo (Sendinblue)", "Free up to 9k emails/month"),
    "canva":         ("Adobe Express", "Free tier available"),
    "grammarly":     ("LanguageTool", "Open-source, free browser extension"),
}

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG & DARK THEME CSS
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SubTrack Pro — SaaS Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Segoe UI', 'Inter', sans-serif;
    color: #eaeaea;
}
.stApp { background-color: #0a0a14; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }
.main .block-container { max-width: 1200px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #111827 100%);
    border-right: 1px solid #1e293b;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label { color: #94a3b8 !important; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] p { color: #64748b !important; font-size: 12px !important; }
[data-testid="stMetricValue"]   { color: #f1f5f9 !important; font-size: 22px !important; }
[data-testid="stMetricDelta"]   { font-size: 11px !important; }

/* ── Buttons ── */
.stButton > button {
    background: #6366f1;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1.2rem;
    transition: background 0.2s;
    width: 100%;
}
.stButton > button:hover { background: #4f46e5; }

/* ── Inputs ── */
input[type="text"], input[type="number"], input[type="email"] {
    background: #0f172a !important;
    color: #f1f5f9 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
}
.stSelectbox > div > div, .stDateInput > div {
    background: #0f172a !important;
    border-color: #1e293b !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
}
.stRadio > div > label { color: #94a3b8 !important; }

/* ── Section headers ── */
.section-title {
    font-size: 13px; font-weight: 700; letter-spacing: .1em;
    color: #6366f1; text-transform: uppercase; margin: 0 0 12px;
}

/* ── Alert cards ── */
.alert-urgent {
    background: #1a0a0a;
    border: 1px solid #ef4444;
    border-left: 4px solid #ef4444;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { border-left-color: #ef4444; }
    50%       { border-left-color: #fca5a5; }
}
.alert-warning {
    background: #140f00;
    border: 1px solid #f59e0b;
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}

/* ── Sub cards ── */
.sub-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.sub-card-safe   { border-left: 4px solid #22c55e; }
.sub-card-warn   { border-left: 4px solid #f59e0b; }
.sub-card-urgent { border-left: 4px solid #ef4444; }
.sub-card-neutral{ border-left: 4px solid #6366f1; }

/* ── Premium banner ── */
.premium-banner {
    background: linear-gradient(135deg, #1a0533 0%, #0f1729 50%, #001a0f 100%);
    border: 1px solid #7c3aed;
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    margin: 16px 0;
}

/* ── Viral card ── */
.viral-card {
    background: #0a1a0a;
    border: 1px solid #22c55e;
    border-radius: 14px;
    padding: 20px;
    margin: 16px 0;
}

/* ── Savings badge ── */
.savings-badge {
    background: linear-gradient(135deg, #064e3b, #065f46);
    border: 2px solid #10b981;
    border-radius: 50px;
    padding: 8px 20px;
    display: inline-block;
    font-weight: 700;
    font-size: 18px;
    color: #6ee7b7;
    margin: 8px 0;
}

/* ── Alternative chip ── */
.alt-chip {
    background: #0c1a2e;
    border: 1px solid #0ea5e9;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 12px;
    color: #7dd3fc;
    margin-top: 8px;
}

/* ── Team seat card ── */
.seat-card {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px;
    margin-top: 12px;
}

/* ── Dividers ── */
hr { border-color: #1e293b !important; }

/* ── Expander ── */
details { background: #0f172a !important; border-radius: 10px !important; }
summary { color: #94a3b8 !important; }

/* ── License unlock ── */
.unlocked-banner {
    background: #052e16;
    border: 1px solid #16a34a;
    border-radius: 10px;
    padding: 12px 16px;
    color: #4ade80;
    font-weight: 600;
    text-align: center;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  DATA LAYER
# ═══════════════════════════════════════════════════════════════
def init_data() -> dict:
    return {
        "workspaces": {
            "personal":  {"name": "My Personal Workspace",  "subs": []},
            "corporate": {"name": "My Corporate Workspace", "subs": []},
        },
        "team_emails":    [],
        "total_cancelled_inr": 0.0,
        "cancelled_log": [],
    }

def load_data() -> dict:
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE) as f:
                data = json.load(f)
            # back-compat: ensure keys exist
            data.setdefault("team_emails", [])
            data.setdefault("total_cancelled_inr", 0.0)
            data.setdefault("cancelled_log", [])
            return data
        except Exception:
            pass
    return init_data()

def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ═══════════════════════════════════════════════════════════════
#  CURRENCY HELPERS
# ═══════════════════════════════════════════════════════════════
def to_inr(cost: float, cur: str) -> float:
    if "USD" in cur:   return cost * USD_TO_INR
    if "EUR" in cur:   return cost * EUR_TO_INR
    return cost

def to_display(cost_inr: float, cur: str) -> str:
    if "USD" in cur:   return f"${cost_inr / USD_TO_INR:,.2f}"
    if "EUR" in cur:   return f"€{cost_inr / EUR_TO_INR:,.2f}"
    return f"₹{cost_inr:,.2f}"

def fmt_inr(v: float) -> str:
    return f"₹{v:,.0f}"

def annual_inr(cost_inr: float, cycle: str) -> float:
    return cost_inr * 12 if cycle == "Monthly" else cost_inr


# ═══════════════════════════════════════════════════════════════
#  DATE HELPERS
# ═══════════════════════════════════════════════════════════════
def days_until(ds: str) -> int:
    try:
        d = datetime.strptime(ds, "%Y-%m-%d").date()
        return (d - date.today()).days
    except Exception:
        return 999

def urgency_class(days: int) -> str:
    if days < 0:    return "urgent"
    if days <= 7:   return "urgent"
    if days <= 30:  return "warn"
    return "safe"


# ═══════════════════════════════════════════════════════════════
#  ALTERNATIVE SUGGESTION ENGINE
# ═══════════════════════════════════════════════════════════════
def get_alternative(name: str, category: str) -> tuple[str, str] | None:
    key = name.lower().strip()
    for k, v in ALTERNATIVES.items():
        if k in key:
            return v
    cat_lower = category.lower()
    if "design" in cat_lower:
        return ("Penpot (Free)", "Open-source Figma alternative — 100% free for teams")
    if "cloud" in cat_lower or "infra" in cat_lower:
        return ("Hetzner Cloud", "Up to 70% cheaper than AWS/GCP for comparable specs")
    if "communication" in cat_lower or "slack" in cat_lower:
        return ("Zulip Open Source", "Free self-hosted; topic-threaded like Slack")
    if "crm" in cat_lower:
        return ("HubSpot Free CRM", "0 cost, unlimited contacts & deals")
    return None


# ═══════════════════════════════════════════════════════════════
#  SESSION STATE BOOTSTRAP
# ═══════════════════════════════════════════════════════════════
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "show_viral" not in st.session_state:
    st.session_state.show_viral = False
if "last_cancelled" not in st.session_state:
    st.session_state.last_cancelled = None
if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = False

data = st.session_state.data


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🚀 SubTrack Pro")
    st.markdown("<p style='color:#475569;font-size:12px'>SaaS Intelligence Suite</p>", unsafe_allow_html=True)
    st.divider()

    # ── Workspace toggle ────────────────────────────────────────
    st.markdown('<p class="section-title">🏢 Workspace Mode</p>', unsafe_allow_html=True)
    ws_mode = st.radio(
        "Select workspace",
        ["🙋 Personal Workspace", "🏢 Corporate SaaS Workspace"],
        label_visibility="collapsed"
    )
    is_corporate = "Corporate" in ws_mode
    ws_key       = "corporate" if is_corporate else "personal"
    ws_label     = "Corporate SaaS" if is_corporate else "Personal"

    st.divider()

    # ── License key ─────────────────────────────────────────────
    st.markdown('<p class="section-title">🔑 Activate License</p>', unsafe_allow_html=True)
    license_input = st.text_input(
        "Enter license key",
        type="password",
        placeholder="e.g. MILLIONAIRE2026",
        label_visibility="collapsed"
    )
    if license_input.strip().upper() == VALID_LICENSE_KEY:
        st.session_state.premium_unlocked = True
    if st.session_state.premium_unlocked:
        st.markdown('<div class="unlocked-banner">✅ Enterprise Unlocked</div>', unsafe_allow_html=True)
    else:
        st.info("🔒 Free plan: 3 subscriptions max")

    st.divider()

    # ── Team seats ──────────────────────────────────────────────
    st.markdown('<p class="section-title">👥 Team Seats</p>', unsafe_allow_html=True)
    new_email = st.text_input("Add team member email", placeholder="colleague@company.com", label_visibility="collapsed")
    if st.button("➕ Invite Member"):
        if new_email and "@" in new_email:
            if new_email not in data["team_emails"]:
                data["team_emails"].append(new_email)
                save_data(data)
                st.success(f"Invited {new_email}")
            else:
                st.warning("Email already added.")
        else:
            st.error("Enter a valid email address.")

    if data["team_emails"]:
        st.markdown('<div class="seat-card">', unsafe_allow_html=True)
        for email in data["team_emails"]:
            col_e, col_x = st.columns([5, 1])
            col_e.markdown(f"<p style='color:#94a3b8;font-size:12px;margin:2px 0'>✉️ {email}</p>", unsafe_allow_html=True)
            if col_x.button("✕", key=f"rem_{email}"):
                data["team_emails"].remove(email)
                save_data(data)
                st.rerun()
        seat_count = len(data["team_emails"])
        st.markdown(f"<p style='color:#6366f1;font-size:11px;margin-top:8px'>{seat_count} seat(s) active</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        # Simulate download trigger
        st.download_button(
            "📥 Export Seat List (.txt)",
            data="\n".join(data["team_emails"]),
            file_name="team_seats.txt",
            mime="text/plain"
        )

    st.divider()
    st.markdown("<p style='color:#334155;font-size:11px;text-align:center'>Built with ❤️ for founders & students who want financial freedom</p>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  MAIN AREA HEADER
# ═══════════════════════════════════════════════════════════════
ws_data  = data["workspaces"][ws_key]
ws_subs  = ws_data["subs"]
ws_icon  = "🏢" if is_corporate else "🙋"
cats     = CATEGORIES_CORPORATE if is_corporate else CATEGORIES_PERSONAL

st.markdown(
    f"<h1 style='font-size:26px;font-weight:700;color:#f1f5f9;margin-bottom:4px'>"
    f"{ws_icon} {ws_label} Subscription Intelligence</h1>"
    f"<p style='color:#475569;font-size:13px;margin-bottom:20px'>"
    f"Track • Optimise • Cancel • Grow Wealth</p>",
    unsafe_allow_html=True
)

# ═══════════════════════════════════════════════════════════════
#  DASHBOARD METRICS (top bar)
# ═══════════════════════════════════════════════════════════════
monthly_total_inr = sum(
    (s["cost_inr"] if s["cycle"] == "Monthly" else s["cost_inr"] / 12)
    for s in ws_subs
)
yearly_total_inr  = sum(annual_inr(s["cost_inr"], s["cycle"]) for s in ws_subs)
urgent_count      = sum(1 for s in ws_subs if 0 <= days_until(s["date"]) <= 7)
total_subs        = len(ws_subs)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("📦 Active Subs",     total_subs)
m2.metric("🔴 Renew in 7 Days", urgent_count)
m3.metric("💸 Monthly Bleed",   fmt_inr(monthly_total_inr))
m4.metric("📅 Annual Bleed",    fmt_inr(yearly_total_inr))
m5.metric("💰 Total Saved",     fmt_inr(data["total_cancelled_inr"]))

st.divider()

# ═══════════════════════════════════════════════════════════════
#  VIRAL / SAVINGS BADGE (appears after cancellation)
# ═══════════════════════════════════════════════════════════════
if st.session_state.show_viral and st.session_state.last_cancelled:
    lc       = st.session_state.last_cancelled
    saved    = lc["annual_inr"]
    svc_name = lc["name"]
    total_s  = data["total_cancelled_inr"]

    st.markdown(f"""
    <div class="viral-card">
        <h3 style="color:#4ade80;margin:0 0 6px">🎉 Subscription Cancelled!</h3>
        <p style="color:#94a3b8;margin:0 0 12px">You just freed up real money from your budget.</p>
        <div class="savings-badge">💰 {fmt_inr(saved)} saved annually</div>
        <p style="color:#6ee7b7;font-size:13px;margin:12px 0 0">
            Total lifetime savings via SubTrack Pro: <strong>{fmt_inr(total_s)}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Shareable text
    share_text = (
        f"🚀 I just eliminated {fmt_inr(saved)}/year from my recurring expenses "
        f"by cancelling {svc_name} using Smart Subscription Tracker!\n\n"
        f"Total savings so far: {fmt_inr(total_s)} 💸\n\n"
        f"Try it free 👉 [Insert Your Streamlit URL Here]\n"
        f"#FinancialFreedom #SaaS #SubTrackPro"
    )
    st.markdown('<p class="section-title">📢 Share Your Win</p>', unsafe_allow_html=True)
    st.code(share_text, language=None)
    st.caption("Copy this ↑ and paste it directly on WhatsApp, X (Twitter), or LinkedIn.")

    if st.button("✕  Close celebration"):
        st.session_state.show_viral      = False
        st.session_state.last_cancelled  = None
        st.rerun()

    st.divider()


# ═══════════════════════════════════════════════════════════════
#  SMART PRIORITY ALERT SYSTEM
# ═══════════════════════════════════════════════════════════════
urgent_subs = [s for s in ws_subs if -1 <= days_until(s["date"]) <= 7]
if urgent_subs:
    st.markdown('<p class="section-title">🚨 Smart Priority Alerts — Action Required</p>', unsafe_allow_html=True)
    for s in sorted(urgent_subs, key=lambda x: days_until(x["date"])):
        days = days_until(s["date"])
        if days < 0:
            label = f"🔴 OVERDUE by {abs(days)} days — Renewal missed!"
            cls   = "alert-urgent"
        elif days == 0:
            label = "🔴 RENEWS TODAY — Cancel now to avoid charge!"
            cls   = "alert-urgent"
        else:
            label = f"🟠 Renews in {days} day{'s' if days > 1 else ''} — Review before it auto-bills"
            cls   = "alert-warning"
        st.markdown(f"""
        <div class="{cls}">
            <strong style="color:#fca5a5">{s['name']}</strong>
            <span style="color:#6b7280;font-size:12px;margin-left:10px">{s['category']}</span><br>
            <span style="font-size:13px;color:#f87171">{label}</span>
            <span style="float:right;font-weight:700;color:#fb923c">{fmt_inr(annual_inr(s['cost_inr'], s['cycle']))}/yr</span>
        </div>
        """, unsafe_allow_html=True)
    st.divider()


# ═══════════════════════════════════════════════════════════════
#  ADD SUBSCRIPTION FORM
# ═══════════════════════════════════════════════════════════════
freemium_wall = not st.session_state.premium_unlocked and total_subs >= FREE_LIMIT

with st.expander("➕  Add New Subscription", expanded=(total_subs == 0)):
    if freemium_wall:
        # ── PAYWALL BANNER ──────────────────────────────────────
        st.markdown("""
        <div class="premium-banner">
            <h2 style="color:#a78bfa;margin:0 0 10px">⚠️ Freemium Limit Reached</h2>
            <p style="color:#c4b5fd;margin:0 0 16px">
                You've used all 3 free subscription slots.
            </p>
            <h3 style="color:#7c3aed;margin:0 0 6px">🚀 Upgrade to Premium Enterprise</h3>
            <ul style="color:#94a3b8;text-align:left;display:inline-block;margin:0 0 16px">
                <li>✅ Unlimited subscription tracking</li>
                <li>✅ Unlimited team seats &amp; shared workspaces</li>
                <li>✅ Automated WhatsApp / Email ledger integration</li>
                <li>✅ Priority renewal alerts via SMS</li>
                <li>✅ Multi-currency portfolio dashboard</li>
                <li>✅ AI-powered spend optimisation reports</li>
            </ul>
            <br>
            <p style="color:#6d28d9;font-size:13px;margin:0">
                🔑 Enter license key <strong>MILLIONAIRE2026</strong> in the sidebar to unlock instantly — free during beta.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        c1, c2 = st.columns(2)
        with c1:
            sub_name = st.text_input("📛 Subscription / Service Name", placeholder="e.g. AWS, Notion, Spotify")
            cost_val = st.number_input("💰 Cost", min_value=0.01, step=1.0, format="%.2f")
            currency = st.selectbox("💱 Currency", CURRENCIES)
            cycle    = st.selectbox("🔄 Renewal Cycle", RENEWAL_CYCLES)
        with c2:
            vendor   = st.selectbox("🏷️ Category / Vendor Type", cats)
            ren_date = st.date_input("📅 Next Renewal Date", value=date.today() + timedelta(days=30))
            ws_name_input = st.text_input("🏢 Workspace / Project Label", placeholder="e.g. Main App, Team Alpha")

        if st.button("✅ Add Subscription"):
            if not sub_name.strip():
                st.error("Please enter a subscription name.")
            else:
                cost_inr = to_inr(cost_val, currency)
                new_sub  = {
                    "name":       sub_name.strip(),
                    "cost_raw":   cost_val,
                    "currency":   currency,
                    "cost_inr":   cost_inr,
                    "cycle":      cycle,
                    "category":   vendor,
                    "date":       str(ren_date),
                    "workspace":  ws_name_input.strip() or ws_label,
                    "added":      str(date.today()),
                }
                ws_subs.append(new_sub)
                save_data(data)
                st.success(f"✅ {sub_name} added to {ws_label}!")
                st.rerun()


# ═══════════════════════════════════════════════════════════════
#  SUBSCRIPTION LIST
# ═══════════════════════════════════════════════════════════════
st.markdown('<p class="section-title" style="margin-top:16px">📋 Active Subscriptions</p>', unsafe_allow_html=True)

if not ws_subs:
    st.markdown("""
    <div style="text-align:center;padding:60px 0;color:#334155">
        <p style="font-size:40px;margin:0">📭</p>
        <p style="font-size:16px;color:#64748b;margin:8px 0">No subscriptions tracked yet.</p>
        <p style="font-size:13px;color:#475569">Open the form above to add your first one.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Sort by renewal date (soonest first)
    sorted_subs = sorted(ws_subs, key=lambda s: days_until(s["date"]))

    for idx_sorted, s in enumerate(sorted_subs):
        idx_original = ws_subs.index(s)
        days         = days_until(s["date"])
        ucls         = urgency_class(days)
        card_cls     = f"sub-card sub-card-{ucls}" if ucls != "safe" else "sub-card sub-card-safe"

        if   days < 0:    day_label = f"⛔ {abs(days)}d overdue"
        elif days == 0:   day_label = "🔴 TODAY"
        elif days <= 7:   day_label = f"🟠 {days}d left"
        elif days <= 30:  day_label = f"🟡 {days}d"
        else:             day_label = f"🟢 {days}d"

        annual_cost = annual_inr(s["cost_inr"], s["cycle"])
        alt         = get_alternative(s["name"], s["category"])

        # ── card header ────────────────────────────────────────
        col_name, col_cost, col_cycle, col_cat, col_date, col_days, col_del = st.columns(
            [2.5, 1.5, 1.2, 2, 1.4, 1.4, 0.8]
        )
        col_name.markdown(
            f"<p style='color:#f1f5f9;font-weight:600;font-size:14px;margin:8px 0 2px'>{s['name']}</p>"
            f"<p style='color:#475569;font-size:11px;margin:0'>{s.get('workspace','—')}</p>",
            unsafe_allow_html=True
        )
        col_cost.markdown(
            f"<p style='color:#a78bfa;font-weight:700;font-size:14px;margin:8px 0 2px'>{fmt_inr(s['cost_inr'])}</p>"
            f"<p style='color:#475569;font-size:11px;margin:0'>{fmt_inr(annual_cost)}/yr</p>",
            unsafe_allow_html=True
        )
        col_cycle.markdown(
            f"<p style='color:#64748b;font-size:12px;margin:8px 0'>{'🔁' if s['cycle']=='Monthly' else '📆'} {s['cycle']}</p>",
            unsafe_allow_html=True
        )
        col_cat.markdown(
            f"<p style='color:#64748b;font-size:12px;margin:8px 0'>{s['category']}</p>",
            unsafe_allow_html=True
        )
        col_date.markdown(
            f"<p style='color:#64748b;font-size:12px;margin:8px 0'>{s['date']}</p>",
            unsafe_allow_html=True
        )
        col_days.markdown(
            f"<p style='font-size:12px;font-weight:600;margin:8px 0'>{day_label}</p>",
            unsafe_allow_html=True
        )

        # ── delete button ──────────────────────────────────────
        del_key = f"del_{ws_key}_{idx_original}_{s['name']}"
        if col_del.button("🗑️", key=del_key, help=f"Cancel {s['name']}"):
            annual_save = annual_inr(s["cost_inr"], s["cycle"])
            data["total_cancelled_inr"] += annual_save
            data["cancelled_log"].append({
                "name":       s["name"],
                "annual_inr": annual_save,
                "date":       str(date.today()),
            })
            ws_subs.pop(idx_original)
            save_data(data)
            st.session_state.show_viral     = True
            st.session_state.last_cancelled = {"name": s["name"], "annual_inr": annual_save}
            st.rerun()

        # ── alternative suggestion ─────────────────────────────
        if alt:
            st.markdown(
                f"<div class='alt-chip'>💡 <strong>Cheaper alternative:</strong> {alt[0]} — {alt[1]}</div>",
                unsafe_allow_html=True
            )

        st.markdown("<hr style='border-color:#0f1729;margin:10px 0'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  BLEED MATRIX — portfolio breakdown
# ═══════════════════════════════════════════════════════════════
if ws_subs:
    st.divider()
    st.markdown('<p class="section-title">📊 Spend Matrix & Optimisation Engine</p>', unsafe_allow_html=True)

    # Category breakdown
    cat_spend: dict[str, float] = {}
    for s in ws_subs:
        cat = s["category"]
        cat_spend[cat] = cat_spend.get(cat, 0) + annual_inr(s["cost_inr"], s["cycle"])

    cat_sorted = sorted(cat_spend.items(), key=lambda x: x[1], reverse=True)
    top_n      = min(len(cat_sorted), 5)

    cols = st.columns(top_n)
    max_spend = cat_sorted[0][1] if cat_sorted else 1
    for i, (cat, spend) in enumerate(cat_sorted[:top_n]):
        pct = (spend / yearly_total_inr * 100) if yearly_total_inr else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        cols[i].markdown(
            f"<div style='background:#0f172a;border:1px solid #1e293b;border-radius:10px;padding:12px;text-align:center'>"
            f"<p style='font-size:11px;color:#64748b;margin:0 0 4px'>{cat}</p>"
            f"<p style='font-size:16px;font-weight:700;color:#a78bfa;margin:0 0 4px'>{fmt_inr(spend)}/yr</p>"
            f"<p style='font-size:9px;color:#334155;letter-spacing:.05em;margin:0'>{bar}</p>"
            f"<p style='font-size:11px;color:#64748b;margin:4px 0 0'>{pct:.1f}% of spend</p>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Optimisation score
    st.markdown("<br>", unsafe_allow_html=True)
    sub_with_alt    = sum(1 for s in ws_subs if get_alternative(s["name"], s["category"]))
    optimise_pct    = int((sub_with_alt / total_subs) * 100) if total_subs else 0
    score_color     = "#ef4444" if optimise_pct > 50 else ("#f59e0b" if optimise_pct > 20 else "#22c55e")

    st.markdown(
        f"<div style='background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:16px 24px'>"
        f"<p style='color:#64748b;font-size:12px;margin:0 0 4px'>🔍 Optimisation Opportunity Score</p>"
        f"<p style='font-size:24px;font-weight:700;color:{score_color};margin:0'>{optimise_pct}% of subs have cheaper alternatives</p>"
        f"<p style='color:#475569;font-size:12px;margin:8px 0 0'>"
        f"{sub_with_alt} out of {total_subs} subscriptions can be replaced with free or cheaper tools — "
        f"saving you up to {fmt_inr(yearly_total_inr * 0.6)}/yr based on typical migration savings.</p>"
        f"</div>",
        unsafe_allow_html=True
    )


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.divider()
st.markdown(
    "<p style='text-align:center;color:#1e293b;font-size:11px'>"
    "SubTrack Pro • Data stored in saas_tracker_data.json • "
    "Built for ambitious founders, students &amp; teams 🚀"
    "</p>",
    unsafe_allow_html=True
)
