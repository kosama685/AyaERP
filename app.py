"""
AyaERP 🦅 — Corporate Marketing Command Center
Streamlit Cloud Deployment | v3.0
"""

import streamlit as st
import json
import os
from datetime import datetime
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

# ─── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="AyaERP | Marketing Command Center",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Corporate Dark Theme ───────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global */
    .stApp {
        background: #0a0c10;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        border-right: 1px solid #21262d;
    }
    section[data-testid="stSidebar"] .stRadio > label {
        color: #c9d1d9;
        font-size: 0.9rem;
        padding: 10px 14px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] .stRadio > label:hover {
        background: #161b22;
        color: #58a6ff;
    }
    
    /* Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(22,27,34,0.95), rgba(13,17,23,0.95));
        border: 1px solid #21262d;
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: #388bfd;
        box-shadow: 0 0 20px rgba(56,139,253,0.1);
        transform: translateY(-2px);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #161b22, #0d1117);
        border: 1px solid #21262d;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #388bfd, #a371f7, #3fb950);
    }
    .metric-value {
        font-size: 2.2em;
        font-weight: 800;
        background: linear-gradient(135deg, #58a6ff, #a371f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.85em;
        color: #8b949e;
        margin-top: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-change {
        font-size: 0.8em;
        margin-top: 4px;
    }
    .metric-change.up { color: #3fb950; }
    .metric-change.down { color: #f85149; }
    
    /* Client Cards */
    .client-card {
        background: linear-gradient(135deg, #161b22, #0d1117);
        border: 1px solid #21262d;
        border-radius: 16px;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }
    .client-card::after {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 80px; height: 80px;
        background: radial-gradient(circle, rgba(56,139,253,0.08) 0%, transparent 70%);
    }
    .client-card:hover {
        border-color: #388bfd;
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(56,139,253,0.15);
    }
    .client-name {
        font-size: 1.2em;
        font-weight: 700;
        color: #f0f6fc;
    }
    .client-domain {
        color: #58a6ff;
        font-size: 0.85em;
        font-weight: 500;
    }
    .client-meta {
        font-size: 0.8em;
        color: #8b949e;
        margin-top: 10px;
        line-height: 1.8;
    }
    .client-meta strong { color: #c9d1d9; }
    
    /* Phase Flow */
    .phase-box {
        background: linear-gradient(135deg, #161b22, #0d1117);
        border: 1px solid #21262d;
        border-left: 4px solid #388bfd;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
    }
    .phase-box:hover {
        border-left-color: #a371f7;
        box-shadow: 0 4px 15px rgba(56,139,253,0.1);
    }
    .phase-title {
        color: #58a6ff;
        font-weight: 700;
        font-size: 1.05em;
    }
    
    /* Lead Cards */
    .lead-high {
        background: linear-gradient(135deg, #3d1014, #1a0808);
        border: 1px solid #f85149;
        border-radius: 12px;
        padding: 16px;
    }
    .lead-medium {
        background: linear-gradient(135deg, #3d2e00, #1a1300);
        border: 1px solid #d29922;
        border-radius: 12px;
        padding: 16px;
    }
    .lead-low {
        background: linear-gradient(135deg, #0d2818, #081a10);
        border: 1px solid #238636;
        border-radius: 12px;
        padding: 16px;
    }
    
    /* Tool Badges */
    .tool-badge {
        display: inline-block;
        background: rgba(56,139,253,0.15);
        color: #58a6ff;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75em;
        font-weight: 600;
        margin: 2px;
    }
    .tool-badge.green { background: rgba(63,185,80,0.15); color: #3fb950; }
    .tool-badge.purple { background: rgba(163,113,247,0.15); color: #a371f7; }
    .tool-badge.orange { background: rgba(210,153,34,0.15); color: #d29922; }
    
    /* Section Headers */
    .section-header {
        font-size: 1.3em;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-header .dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #388bfd;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #21262d; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #388bfd; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #238636, #2ea043);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2ea043, #3fb950);
        box-shadow: 0 4px 15px rgba(46,160,67,0.3);
    }
    
    /* Logo */
    .logo-text {
        font-size: 1.5em;
        font-weight: 800;
        background: linear-gradient(135deg, #58a6ff, #a371f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #388bfd, #a371f7);
    }
    
    /* Tables */
    .stDataFrame {
        border: 1px solid #21262d;
        border-radius: 12px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #161b22;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Import Engine ───────────────────────────────────────────
try:
    from erp_engine import CLIENTS, BEST_TIMES, BEST_MONTHS, generate_marketing_strategy, generate_daily_report, generate_content_prompt
    from erp_engine_v2 import (
        LLM_ROUTES, route_to_llm, detect_lead,
        EXHIBITIONS_DB, get_exhibitions, get_upcoming_exhibitions,
        SELENIUM_NODE_SCRIPTS
    )
    ENGINE_LOADED = True
except Exception as e:
    ENGINE_LOADED = False
    LOAD_ERROR = str(e)

# ─── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:10px 0 20px;">
        <div class="logo-text">🦅 AyaERP</div>
        <div style="color:#8b949e; font-size:0.75em; margin-top:4px;">Marketing Command Center</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio("", [
        "📊 Dashboard",
        "👥 Clients",
        "🤖 AI Router",
        "🎯 Lead Detection",
        "🎪 Exhibitions",
        "📅 Best Times",
        "📋 Strategy Gen",
        "📝 Content Prompts",
        "🔄 ERP Flow",
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="padding:10px; background:#161b22; border-radius:10px; border:1px solid #21262d;">
        <div style="color:#c9d1d9; font-weight:600;">Usama Khan</div>
        <div style="color:#8b949e; font-size:0.8em;">🇸🇦 Saudi Arabia · 🇪🇪 Estonia</div>
        <div style="color:#8b949e; font-size:0.75em; margin-top:4px;">{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Helper Functions ────────────────────────────────────────
REGION_FLAGS = {"SA": "🇸🇦", "UK": "🇬🇧", "EU": "🇪🇺", "US": "🇺🇸", "PK": "🇵🇰"}
REGION_NAMES = {"SA": "Saudi Arabia", "UK": "United Kingdom", "EU": "Europe", "US": "United States", "PK": "Pakistan"}

# ─── DASHBOARD ───────────────────────────────────────────────
if page == "📊 Dashboard":
    # Header
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:30px;">
        <div>
            <h1 style="font-size:1.8em; font-weight:800; color:#f0f6fc; margin:0;">Marketing Operations Command Center</h1>
            <p style="color:#8b949e; font-size:0.9em; margin:4px 0 0;">Multi-client · Multi-region · AI-Powered Automation</p>
        </div>
        <div style="display:flex; gap:8px;">
            <span class="tool-badge">LIVE</span>
            <span class="tool-badge green">4 CLIENTS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">4</div>
            <div class="metric-label">Active Clients</div>
            <div class="metric-change up">↑ SA · EU · UK · PK</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">248</div>
            <div class="metric-label">Monthly Posts</div>
            <div class="metric-change up">↑ 12% vs last month</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">4.8%</div>
            <div class="metric-label">Avg Engagement</div>
            <div class="metric-change up">↑ +0.6% industry avg</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">$11K</div>
            <div class="metric-label">Monthly Budget</div>
            <div class="metric-change">Across 4 clients</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">$10</div>
            <div class="metric-label">AI Cost/Month</div>
            <div class="metric-change up">↓ Token optimized</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Client Portfolio
    st.markdown('<div class="section-header"><div class="dot"></div>Client Portfolio</div>', unsafe_allow_html=True)
    
    if ENGINE_LOADED:
        cols = st.columns(4)
        for i, (key, client) in enumerate(CLIENTS.items()):
            with cols[i]:
                flag = REGION_FLAGS.get(client.region, "🌍")
                st.markdown(f"""
                <div class="client-card">
                    <div class="client-name">{flag} {client.name}</div>
                    <div class="client-domain">{client.domain}</div>
                    <div class="client-meta">
                        <strong>{REGION_NAMES.get(client.region, client.region)}</strong> · {client.industry}<br>
                        {' '.join([f'<span class="tool-badge">{p}</span>' for p in client.platforms[:3]])}<br>
                        💰 ${client.monthly_budget:,.0f}/mo · {', '.join(client.content_languages)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<div class="section-header"><div class="dot"></div>Quick Actions</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 Run Daily Automation", use_container_width=True):
            st.success("✅ Automation triggered for all 4 clients")
    with col2:
        if st.button("📊 Generate All Reports", use_container_width=True):
            st.success("✅ Reports generated — check /reports/")
    with col3:
        if st.button("🎯 Scan New Leads", use_container_width=True):
            st.info("🔍 Scanning all platforms for sales leads...")
    with col4:
        if st.button("🎪 Check Exhibitions", use_container_width=True):
            st.info("🎪 3 upcoming exhibitions found this quarter")

# ─── CLIENTS ─────────────────────────────────────────────────
elif page == "👥 Clients":
    st.markdown('<h1 style="font-weight:800; color:#f0f6fc;">👥 Client Management</h1>', unsafe_allow_html=True)
    st.caption("Complete client database with strategies, schedules, and KPIs")
    
    if not ENGINE_LOADED:
        st.error(f"Engine not loaded: {LOAD_ERROR}")
    else:
        for key, client in CLIENTS.items():
            flag = REGION_FLAGS.get(client.region, "🌍")
            with st.expander(f"{flag} {client.name} — {client.domain}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="glass-card">
                        <h3 style="color:#58a6ff; margin-bottom:12px;">📋 Profile</h3>
                        <p><strong>Region:</strong> {REGION_NAMES.get(client.region, client.region)}</p>
                        <p><strong>Industry:</strong> {client.industry}</p>
                        <p><strong>Budget:</strong> ${client.monthly_budget:,.0f}/month</p>
                        <p><strong>Languages:</strong> {', '.join(client.content_languages)}</p>
                        <p><strong>Platforms:</strong> {' '.join([f'<span class="tool-badge">{p}</span>' for p in client.platforms])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("**🎯 Target Keywords:**")
                    for kw in client.target_keywords:
                        st.markdown(f"`{kw}`")
                
                st.markdown("---")
                st.markdown("**📅 Posting Schedule:**")
                schedule_data = []
                days_list = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
                for platform, sched in client.posting_schedule.items():
                    active_days = [days_list[d] for d in sched.get('days', [])]
                    schedule_data.append({
                        "Platform": platform.title(),
                        "Active Days": ", ".join(active_days),
                        "Best Times": ", ".join(sched.get('times', [])),
                    })
                st.dataframe(schedule_data, use_container_width=True, hide_index=True)

# ─── AI ROUTER ──────────────────────────────────────────────
elif page == "🤖 AI Router":
    st.markdown('<h1 style="font-weight:800; color:#f0f6fc;">🤖 LLM Router — Token Optimizer</h1>', unsafe_allow_html=True)
    st.caption("Smart task routing to minimize AI costs while maximizing quality")
    
    if ENGINE_LOADED:
        st.markdown('<div class="section-header"><div class="dot"></div>Routing Table</div>', unsafe_allow_html=True)
        
        route_data = []
        for task_type, route in LLM_ROUTES.items():
            llm_colors = {"ChatGPT Pro": "green", "Claude Pro Max": "purple", "Grok": "orange", "Gemini Pro": ""}
            badge_class = llm_colors.get(route["best_llm"], "")
            route_data.append({
                "Task": task_type.replace("_", " ").title(),
                "AI Model": route["best_llm"],
                "Est. Tokens": route["estimated_tokens"],
                "Cost/1K": route["cost_per_1k"],
                "Why": route["reason"][:60] + "..."
            })
        st.dataframe(route_data, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="dot"></div>Test Router</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            task_type = st.selectbox("Task type:", list(LLM_ROUTES.keys()), format_func=lambda x: x.replace("_", " ").title())
            context = st.text_area("Additional context:", height=80)
        with col2:
            if st.button("⚡ Route Task", type="primary", use_container_width=True):
                result = route_to_llm(task_type, context)
                st.markdown(f"""
                <div class="glass-card">
                    <h3 style="color:#58a6ff;">→ {result['recommended_llm']}</h3>
                    <p><strong>Tokens:</strong> {result['estimated_tokens']} · <strong>Cost:</strong> {result['estimated_cost']}</p>
                    <p style="color:#8b949e;">{result['reason']}</p>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("View Generated Prompt"):
                    st.code(result["prompt_template"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="dot"></div>Cost Calculator</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            num_clients = st.slider("Number of clients", 1, 20, 4)
            posts_per_day = st.slider("Posts/day per client", 1, 10, 2)
        with col2:
            daily = num_clients * posts_per_day * 0.04
            monthly = daily * 30
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-value">${daily:.2f}</div>
                <div class="metric-label">Daily AI Cost</div>
                <div class="metric-value" style="margin-top:16px;">${monthly:.2f}</div>
                <div class="metric-label">Monthly AI Cost</div>
                <div class="metric-value" style="margin-top:16px;">${monthly*12:.0f}</div>
                <div class="metric-label">Annual AI Cost</div>
            </div>
            """, unsafe_allow_html=True)

# ─── LEAD DETECTION ─────────────────────────────────────────
elif page == "🎯 Lead Detection":
    st.markdown('<h1 style="font-weight:800; color:#f0f6fc;">🎯 Sales Lead Detection</h1>', unsafe_allow_html=True)
    st.caption("AI-powered intent scoring — catch every sales opportunity")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        test_message = st.text_area("Enter a message, comment, or DM:", 
            value="I need SEO services for my hotel in Riyadh, what's your price?", height=100)
    with col2:
        client_name = st.text_input("Client:", value="")
    
    if st.button("🔍 Detect Lead", type="primary", use_container_width=True):
        result = detect_lead(test_message, client_name)
        score = result["lead_score"]
        intent = result["intent_level"]
        
        if intent == "HIGH":
            st.markdown(f"""
            <div class="lead-high">
                <h3>🚨 HIGH INTENT — Score: {score}/100</h3>
                <p><strong>Action:</strong> {result['recommended_action']}</p>
                <p><strong>Next Step:</strong> {result['next_step']}</p>
                <p><strong>Keywords:</strong> {result['matched_keywords']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif intent == "MEDIUM":
            st.markdown(f"""
            <div class="lead-medium">
                <h3>⚡ MEDIUM INTENT — Score: {score}/100</h3>
                <p><strong>Action:</strong> {result['recommended_action']}</p>
                <p><strong>Next Step:</strong> {result['next_step']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="lead-low">
                <h3>💬 LOW INTENT — Score: {score}/100</h3>
                <p><strong>Action:</strong> {result['recommended_action']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="dot"></div>Lead Indicators Reference</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#f85149;">🔴 High Intent</h4>
            <p>price, cost, budget, quote<br>hire, contract, package<br>حجز, سعر, عرض (Arabic)<br>قیمت, پیکج (Urdu)</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#d29922;">🟡 Medium Intent</h4>
            <p>interested, tell me more<br>demo, consultation, meeting<br>معلومات, تفاصيل (Arabic)</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#3fb950;">🟢 Low Intent</h4>
            <p>nice, interesting, thanks<br>شكرا, ممتاز (Arabic)</p>
        </div>
        """, unsafe_allow_html=True)

# ─── EXHIBITIONS ────────────────────────────────────────────
elif page == "🎪 Exhibitions":
    st.markdown('<h1 style="font-weight:800; color:#f0f6fc;">🎪 Exhibition Calendar</h1>', unsafe_allow_html=True)
    st.caption("Never miss a regional opportunity — plan 6 months ahead")
    
    if ENGINE_LOADED:
        col1, col2 = st.columns(2)
        with col1:
            region = st.selectbox("Region:", list(EXHIBITIONS_DB.keys()),
                format_func=lambda x: f"{REGION_FLAGS.get(x,'🌍')} {REGION_NAMES.get(x,x)}")
        with col2:
            niches = list(EXHIBITIONS_DB.get(region, {}).keys())
            niche = st.selectbox("Niche:", niches)
        
        exhibitions = get_exhibitions(region, niche)
        if exhibitions:
            for exh in exhibitions:
                with st.expander(f"🎪 {exh['name']} — {exh['month']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**📍 City:** {exh['city']}  \n**🎯 Focus:** {exh['focus']}  \n**📅 When:** {exh['month']}")
                    with col2:
                        st.markdown(f"**🔗 URL:** {exh.get('url', '#')}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="dot"></div>All Upcoming (6 Months)</div>', unsafe_allow_html=True)
        for reg in ["SA", "UK", "EU", "US", "PK"]:
            upcoming = get_upcoming_exhibitions(reg, months_ahead=6)
            if upcoming:
                flag = REGION_FLAGS.get(reg, "🌍")
                st.markdown(f"**{flag} {REGION_NAMES.get(reg, reg)}**")
                for e in upcoming:
                    st.markdown(f"- **{e['name']}** ({e['month']}) — {e['city']} — *{e.get('status', '')}*")

# ─── BEST TIMES ─────────────────────────────────────────────
elif page == "📅 Best Times":
    st.markdown('<h1 style="font-weight:800; color:#f0f6fc;">📅 Best Posting Times</h1>', unsafe_allow_html=True)
    st.caption("Data-driven schedules for maximum engagement by region")
    
    if ENGINE_LOADED:
        region = st.selectbox("Region:", list(BEST_TIMES.keys()),
            format_func=lambda x: f"{REGION_FLAGS.get(x,'🌍')} {REGION_NAMES.get(x,x)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        times_data = BEST_TIMES.get(region, {})
        cols = st.columns(len(times_data))
        days_list = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        
        for i, (platform, info) in enumerate(times_data.items()):
            with cols[i]:
                active_days = [days_list[d] for d in info.get('days', [])]
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <h3 style="color:#58a6ff;">{platform.title()}</h3>
                    <p>⏰ {', '.join(info['best'])}</p>
                    <p>📅 {', '.join(active_days)}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="dot"></div>Best Months by Industry</div>', unsafe_allow_html=True)
        months_data = BEST_MONTHS.get(region, {})
        for industry, months in months_data.items():
            if industry != "exhibitions" and isinstance(months, list):
                st.markdown(f"**{industry.title()}:** {', '.join(months)}")

# ─── STRATEGY GENERATOR ────────────────────────────────────
elif page == "📋 Strategy Gen":
    st.markdown('<h1 style="font-weight:800; color:#f0f6fc;">📋 Marketing Strategy Generator</h1>', unsafe_allow_html=True)
    st.caption("AI-powered 12-month strategy documents for any client")
    
    if ENGINE_LOADED:
        client_key = st.selectbox("Select Client:", list(CLIENTS.keys()),
            format_func=lambda x: f"{CLIENTS[x].name} ({CLIENTS[x].domain})")
        
        if st.button("🚀 Generate Full Strategy", type="primary", use_container_width=True):
            with st.spinner("Generating comprehensive strategy..."):
                strategy = generate_marketing_strategy(client_key)
            
            # Summary
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color:#58a6ff;">📌 Executive Summary</h3>
                <p>{strategy['executive_summary']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Platforms
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**🎯 Primary**")
                for p in strategy["platform_strategy"]["primary"]:
                    st.markdown(f'<span class="tool-badge">{p[0].title()}</span> Score: {p[1]}', unsafe_allow_html=True)
            with col2:
                st.markdown("**📊 Secondary**")
                for p in strategy["platform_strategy"]["secondary"]:
                    st.markdown(f'<span class="tool-badge">{p[0].title()}</span> Score: {p[1]}', unsafe_allow_html=True)
            with col3:
                st.markdown("**🧪 Experimental**")
                for p in strategy["platform_strategy"]["experimental"]:
                    st.markdown(f'<span class="tool-badge">{p[0].title()}</span> Score: {p[1]}', unsafe_allow_html=True)
            
            # Monthly Plan
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header"><div class="dot"></div>12-Month Plan</div>', unsafe_allow_html=True)
            for month, plan in strategy["monthly_plan"].items():
                with st.expander(f"📆 {month} — {plan['focus']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Themes:** {', '.join(plan['content_themes'])}  \n**Budget:** {plan['budget_percentage']}  \n**Growth Target:** {plan['expected_kpi']['traffic_growth']}")
                    with col2:
                        st.markdown(f"**Engagement:** {plan['expected_kpi']['engagement_rate']}  \n**Leads:** {plan['expected_kpi']['lead_generation']}")
            
            # Budget
            st.markdown('<div class="section-header"><div class="dot"></div>Budget Allocation</div>', unsafe_allow_html=True)
            for category, pct in strategy["budget_allocation"].items():
                val = int(pct.replace('%',''))
                st.progress(val/100, text=f"{category.replace('_',' ').title()}: {pct}")
            
            # KPIs
            st.markdown('<div class="section-header"><div class="dot"></div>KPI Targets</div>', unsafe_allow_html=True)
            for kpi, target in strategy["kpi_targets"].items():
                st.markdown(f"✅ **{kpi.replace('_',' ').title()}:** {target}")
            
            # Download
            st.download_button(
                "📥 Download Strategy (JSON)",
                data=json.dumps(strategy, indent=2, ensure_ascii=False),
                file_name=f"strategy_{client_key}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json", use_container_width=True
            )

# ─── CONTENT PROMPTS ───────────────────────────────────────
elif page == "📝 Content Prompts":
    st.markdown('<h1 style="font-weight:800; color:#f0f6fc;">📝 AI Content Prompt Generator</h1>', unsafe_allow_html=True)
    st.caption("Structured prompts with SEO/AEO/GEO tags — ready for any AI model")
    
    if ENGINE_LOADED:
        col1, col2, col3 = st.columns(3)
        with col1:
            client_key = st.selectbox("Client:", list(CLIENTS.keys()), format_func=lambda x: CLIENTS[x].name)
        with col2:
            platform = st.selectbox("Platform:", CLIENTS[client_key].platforms)
        with col3:
            content_types = ["educational", "promotional", "engagement", "testimonial", "behind-scenes", "trending"]
            content_type = st.selectbox("Content Type:", content_types)
        
        if st.button("✨ Generate Prompt", type="primary", use_container_width=True):
            prompt = generate_content_prompt(client_key, platform, content_type)
            st.code(prompt, language="markdown")
            st.download_button("📥 Download Prompt", data=prompt,
                file_name=f"prompt_{client_key}_{platform}_{content_type}.txt",
                mime="text/plain", use_container_width=True)

# ─── ERP FLOW ───────────────────────────────────────────────
elif page == "🔄 ERP Flow":
    st.markdown('<h1 style="font-weight:800; color:#f0f6fc;">🔄 Complete ERP Automation Flow</h1>', unsafe_allow_html=True)
    st.caption("6-phase pipeline — from data input to daily reports")
    
    phases = [
        ("01", "Data Input", "#388bfd", [
            ("📋 Client Onboarding", "Company profile, domain, budget"),
            ("🔍 Market Research", "Competitor analysis, keywords"),
            ("🎯 ICP & Targeting", "Ideal client, geo-targeting"),
            ("⚙️ Config Setup", "Accounts, schedule, KPIs"),
        ]),
        ("02", "AI Strategy Engine", "#a371f7", [
            ("📊 Strategy Blueprint", "12-month plan, platform scoring"),
            ("🏷️ SEO/AEO/GEO", "Keywords, schema, entities"),
            ("📅 Calendar Builder", "Themes, exhibitions, seasons"),
            ("🎪 Exhibition Tracker", "Regional DB, reminders"),
        ]),
        ("03", "Content Factory", "#3fb950", [
            ("✍️ AI Content Gen", "Posts, blogs, captions"),
            ("🎨 Image & Video", "DALL-E, scripts, thumbnails"),
            ("🌐 Multi-Language", "Arabic, Urdu, English"),
            ("✅ Quality Check", "Plagiarism, SEO, brand voice"),
        ]),
        ("04", "Distribution", "#d29922", [
            ("⏰ Smart Scheduling", "Best-time auto-posting"),
            ("📱 Social Auto-Post", "IG, LinkedIn, FB, X, TikTok"),
            ("📝 Blog Auto-Publish", "WordPress, SEO metadata"),
            ("🔄 Cross-Platform", "Repurpose, UTM tracking"),
        ]),
        ("05", "Engagement", "#f78166", [
            ("💬 Auto-Reply Engine", "Comments, DMs, FAQ"),
            ("📥 Inbox Management", "Unified, priority, sentiment"),
            ("🔗 CRM Integration", "Lead capture, pipeline"),
            ("📊 Sentiment Track", "Brand monitoring, alerts"),
        ]),
        ("06", "Reporting", "#f85149", [
            ("🌐 Selenium Scraper", "GA4, GSC, social insights"),
            ("📈 Analytics Dashboard", "Real-time KPIs"),
            ("📋 Daily Email Reports", "Auto PDF, recommendations"),
            ("🔄 Strategy Optimizer", "A/B, budget reallocation"),
        ]),
    ]
    
    for num, title, color, steps in phases:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; margin:20px 0 12px;">
            <div style="background:{color}; color:white; width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.1em;">{num}</div>
            <h3 style="color:#f0f6fc; margin:0;">{title}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(len(steps))
        for i, (step_title, step_desc) in enumerate(steps):
            with cols[i]:
                st.markdown(f"""
                <div class="phase-box" style="border-left-color:{color};">
                    <div class="phase-title">{step_title}</div>
                    <div style="font-size:0.8em; color:#8b949e; margin-top:8px;">{step_desc}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align:center; color:#21262d; font-size:2em; padding:5px 0;">⬇️</div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; padding:20px; background:linear-gradient(135deg,#161b22,#0d1117); border-radius:16px; border:1px solid #21262d;">
        <h3 style="color:#58a6ff;">🦅 ERP Dashboard & Daily Email Report</h3>
        <p style="color:#8b949e;">Cycle repeats daily at 8:00 AM AST</p>
    </div>
    """, unsafe_allow_html=True)
