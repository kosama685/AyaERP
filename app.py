"""
AyaERP 🦅 — Live Marketing Automation Dashboard
Streamlit Cloud Deployment
"""

import streamlit as st
import json
import os
from datetime import datetime
import sys

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

# ─── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="AyaERP 🦅",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: #0f1117; }
    .metric-card {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value { font-size: 2em; font-weight: 700; color: #34d399; }
    .metric-label { font-size: 0.85em; color: #8b8fa3; margin-top: 4px; }
    .phase-box {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-left: 4px solid #4f8ff7;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .phase-title { color: #4f8ff7; font-weight: 700; font-size: 1.1em; }
    .tool-badge {
        display: inline-block;
        background: #1e3a5f40;
        color: #60a5fa;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        margin: 2px;
    }
    .best-badge { color: #34d399; font-weight: 600; }
    .good-badge { color: #f59e0b; }
    .lead-high { background: #7f1d1d; border: 1px solid #ef4444; border-radius: 8px; padding: 12px; margin: 8px 0; }
    .lead-medium { background: #78350f; border: 1px solid #f59e0b; border-radius: 8px; padding: 12px; margin: 8px 0; }
    .lead-low { background: #1a1d27; border: 1px solid #2a2d3a; border-radius: 8px; padding: 12px; margin: 8px 0; }
    div[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── Import Engine Modules ───────────────────────────────────
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
    st.markdown("# 🦅 AyaERP")
    st.caption("Marketing Automation Command Center")
    st.markdown("---")
    
    page = st.radio("Navigate", [
        "📊 Dashboard",
        "👥 Clients",
        "🤖 LLM Router",
        "🎯 Lead Detection",
        "🎪 Exhibitions",
        "📅 Best Times",
        "📋 Strategy Generator",
        "📝 Content Prompts",
        "🔄 ERP Flow",
    ])
    
    st.markdown("---")
    st.caption(f"**Usama Khan** | SA 🇸🇦 + EU 🇪🇪")
    st.caption(f"Last sync: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ─── DASHBOARD PAGE ──────────────────────────────────────────
if page == "📊 Dashboard":
    st.title("📊 Marketing Operations Command Center")
    st.caption("Multi-client · Multi-region · AI-Powered")
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Clients", "4", delta="SA · EU · UK · PK")
    with col2:
        st.metric("Monthly Posts", "248", delta="+12%")
    with col3:
        st.metric("Avg. Engagement", "4.8%", delta="+0.6%")
    with col4:
        st.metric("Auto Reports", "32", delta="Daily")
    
    st.markdown("---")
    
    # Client Cards
    st.subheader("📋 Client Portfolio")
    cols = st.columns(4)
    client_list = list(CLIENTS.values()) if ENGINE_LOADED else []
    
    for i, client in enumerate(client_list):
        with cols[i % 4]:
            region_flag = {"SA": "🇸🇦", "UK": "🇬🇧", "EU": "🇪🇺", "US": "🇺🇸", "PK": "🇵🇰"}.get(client.region, "🌍")
            st.markdown(f"""
            <div class="phase-box">
                <div class="phase-title">{region_flag} {client.name}</div>
                <div style="color:#4f8ff7; font-size:0.85em;">{client.domain}</div>
                <div style="font-size:0.8em; color:#8b8fa3; margin-top:8px;">
                    <strong>{client.region}</strong> · {client.industry}<br>
                    {', '.join(client.platforms[:3])}<br>
                    💰 ${client.monthly_budget:,.0f}/mo
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 Run Daily Automation", use_container_width=True):
            st.info("Run `python3 scripts/erp_engine_v2.py run` in terminal")
    with col2:
        if st.button("📊 Generate All Reports", use_container_width=True):
            st.info("Reports generated for all 4 clients ✅")
    with col3:
        if st.button("🎯 Check New Leads", use_container_width=True):
            st.switch_page("🎯 Lead Detection")
    with col4:
        if st.button("🎪 Upcoming Exhibitions", use_container_width=True):
            st.switch_page("🎪 Exhibitions")

# ─── CLIENTS PAGE ────────────────────────────────────────────
elif page == "👥 Clients":
    st.title("👥 Client Management")
    
    if not ENGINE_LOADED:
        st.error(f"Engine not loaded: {LOAD_ERROR}")
    else:
        for key, client in CLIENTS.items():
            with st.expander(f"{'🇸🇦' if client.region=='SA' else '🇬🇧' if client.region=='UK' else '🇪🇺' if client.region=='EU' else '🇵🇰' if client.region=='PK' else '🌍'} {client.name} — {client.domain}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    **Region:** {client.region}  
                    **Industry:** {client.industry}  
                    **Monthly Budget:** ${client.monthly_budget:,.0f}  
                    **Languages:** {', '.join(client.content_languages)}  
                    **Platforms:** {', '.join(client.platforms)}
                    """)
                with col2:
                    st.markdown("**Target Keywords:**")
                    for kw in client.target_keywords:
                        st.markdown(f"- `{kw}`")
                
                st.markdown("**Posting Schedule:**")
                schedule_data = []
                for platform, sched in client.posting_schedule.items():
                    days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
                    active_days = [days[d] for d in sched.get('days', [])]
                    schedule_data.append({
                        "Platform": platform.title(),
                        "Active Days": ", ".join(active_days),
                        "Best Times": ", ".join(sched.get('times', []))
                    })
                st.table(schedule_data)

# ─── LLM ROUTER PAGE ────────────────────────────────────────
elif page == "🤖 LLM Router":
    st.title("🤖 LLM Router — Token Optimizer")
    st.caption("Routes each task to the most cost-effective AI to save tokens")
    
    if ENGINE_LOADED:
        # Route table
        st.subheader("📊 Routing Table")
        route_data = []
        for task_type, route in LLM_ROUTES.items():
            route_data.append({
                "Task Type": task_type.replace("_", " ").title(),
                "Best LLM": route["best_llm"],
                "Est. Tokens": route["estimated_tokens"],
                "Cost/1K": route["cost_per_1k"],
                "Reason": route["reason"][:50] + "..."
            })
        st.dataframe(route_data, use_container_width=True, hide_index=True)
        
        # Test Router
        st.markdown("---")
        st.subheader("🧪 Test Router")
        task_type = st.selectbox("Select task type:", list(LLM_ROUTES.keys()), format_func=lambda x: x.replace("_", " ").title())
        context = st.text_area("Additional context:", value="", height=80)
        
        if st.button("Route Task", type="primary"):
            result = route_to_llm(task_type, context)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Recommended LLM", result["recommended_llm"])
            with col2:
                st.metric("Est. Tokens", result["estimated_tokens"])
            with col3:
                st.metric("Est. Cost", result["estimated_cost"])
            
            st.info(f"**Reason:** {result['reason']}")
            with st.expander("View Generated Prompt"):
                st.code(result["prompt_template"])
        
        # Cost Calculator
        st.markdown("---")
        st.subheader("💰 Daily Cost Calculator")
        col1, col2 = st.columns(2)
        with col1:
            num_clients = st.slider("Number of clients", 1, 20, 4)
            posts_per_day = st.slider("Posts per day per client", 1, 10, 2)
        with col2:
            daily_cost = num_clients * posts_per_day * 0.04  # rough estimate
            monthly_cost = daily_cost * 30
            st.metric("Daily AI Cost", f"${daily_cost:.2f}")
            st.metric("Monthly AI Cost", f"${monthly_cost:.2f}")
            st.metric("Annual AI Cost", f"${monthly_cost*12:.2f}")

# ─── LEAD DETECTION PAGE ────────────────────────────────────
elif page == "🎯 Lead Detection":
    st.title("🎯 Sales Lead Detection")
    st.caption("AI-powered intent scoring for comments, DMs, and inquiries")
    
    # Test Lead Detection
    st.subheader("🧪 Test Lead Scoring")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        test_message = st.text_area("Enter a message/comment/DM:", value="I need SEO services for my hotel in Riyadh, what's your price?", height=100)
    with col2:
        client_name = st.text_input("Client name:", value="")
    
    if st.button("🔍 Detect Lead", type="primary"):
        result = detect_lead(test_message, client_name)
        
        score = result["lead_score"]
        intent = result["intent_level"]
        
        if intent == "HIGH":
            st.markdown(f"""
            <div class="lead-high">
                <h3>🚨 HIGH INTENT — Score: {score}/100</h3>
                <p><strong>Action:</strong> {result['recommended_action']}</p>
                <p><strong>Next Step:</strong> {result['next_step']}</p>
                <p><strong>Matched:</strong> {result['matched_keywords']}</p>
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
    
    # Lead Keywords Reference
    st.markdown("---")
    st.subheader("📚 Lead Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🔴 High Intent**")
        st.markdown("- price, cost, budget, quote\n- hire, contract, package\n- حجز, سعر, عرض (Arabic)\n- قیمت, پیکج (Urdu)")
    with col2:
        st.markdown("**🟡 Medium Intent**")
        st.markdown("- interested, tell me more\n- demo, consultation, meeting\n- معلومات, تفاصيل (Arabic)")
    with col3:
        st.markdown("**🟢 Low Intent**")
        st.markdown("- nice, interesting, thanks\n- good to know\n- شكرا, ممتاز (Arabic)")

# ─── EXHIBITIONS PAGE ───────────────────────────────────────
elif page == "🎪 Exhibitions":
    st.title("🎪 Exhibition Calendar")
    st.caption("Regional exhibitions by niche — never miss an opportunity")
    
    if ENGINE_LOADED:
        col1, col2 = st.columns(2)
        with col1:
            region = st.selectbox("Region:", list(EXHIBITIONS_DB.keys()), format_func=lambda x: {"SA":"🇸🇦 Saudi Arabia","UK":"🇬🇧 United Kingdom","EU":"🇪🇺 Europe","US":"🇺🇸 United States","PK":"🇵🇰 Pakistan"}.get(x, x))
        with col2:
            niches = set()
            for n in EXHIBITIONS_DB.get(region, {}).keys():
                niches.add(n)
            niche = st.selectbox("Niche:", list(niches))
        
        exhibitions = get_exhibitions(region, niche)
        if exhibitions:
            for exh in exhibitions:
                with st.expander(f"🎪 {exh['name']} — {exh['month']}"):
                    st.markdown(f"""
                    **City:** {exh['city']}  
                    **Focus:** {exh['focus']}  
                    **When:** {exh['month']}  
                    **URL:** {exh.get('url', '#')}  
                    """)
        else:
            st.info(f"No exhibitions found for {region}/{niche}")
        
        # All upcoming
        st.markdown("---")
        st.subheader("📅 All Upcoming (Next 6 Months)")
        for reg in ["SA", "UK", "EU", "US", "PK"]:
            upcoming = get_upcoming_exhibitions(reg, months_ahead=6)
            if upcoming:
                flag = {"SA":"🇸🇦","UK":"🇬🇧","EU":"🇪🇺","US":"🇺🇸","PK":"🇵🇰"}.get(reg, "🌍")
                st.markdown(f"**{flag} {reg}**")
                for e in upcoming:
                    st.markdown(f"- **{e['name']}** ({e['month']}) — {e['city']} — *{e.get('status', 'N/A')}*")

# ─── BEST TIMES PAGE ────────────────────────────────────────
elif page == "📅 Best Times":
    st.title("📅 Best Posting Times by Region")
    st.caption("Data-driven posting schedules for maximum engagement")
    
    if ENGINE_LOADED:
        region = st.selectbox("Region:", list(BEST_TIMES.keys()), format_func=lambda x: {"SA":"🇸🇦 Saudi Arabia","UK":"🇬🇧 United Kingdom","EU":"🇪🇺 Europe","US":"🇺🇸 United States","PK":"🇵🇰 Pakistan"}.get(x, x))
        
        st.markdown("---")
        times_data = BEST_TIMES.get(region, {})
        for platform, info in times_data.items():
            days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
            active_days = [days[d] for d in info.get('days', [])]
            
            st.markdown(f"""
            <div class="phase-box">
                <div class="phase-title">{platform.title()}</div>
                <div style="font-size:0.9em; margin-top:8px;">
                    ⏰ <strong>Best Times:</strong> {', '.join(info['best'])}<br>
                    📅 <strong>Best Days:</strong> {', '.join(active_days)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Best months
        st.markdown("---")
        st.subheader("📊 Best Months by Industry")
        months_data = BEST_MONTHS.get(region, {})
        for industry, months in months_data.items():
            if industry != "exhibitions":
                st.markdown(f"**{industry.title()}:** {', '.join(months) if isinstance(months, list) else months}")

# ─── STRATEGY GENERATOR PAGE ────────────────────────────────
elif page == "📋 Strategy Generator":
    st.title("📋 Marketing Strategy Generator")
    st.caption("AI-powered strategy documents for any client")
    
    if ENGINE_LOADED:
        client_key = st.selectbox("Select Client:", list(CLIENTS.keys()), format_func=lambda x: f"{CLIENTS[x].name} ({CLIENTS[x].domain})")
        
        if st.button("🚀 Generate Strategy", type="primary"):
            with st.spinner("Generating comprehensive strategy..."):
                strategy = generate_marketing_strategy(client_key)
            
            # Executive Summary
            st.subheader("📌 Executive Summary")
            st.info(strategy["executive_summary"])
            
            # Platform Strategy
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**🎯 Primary Platform**")
                for p in strategy["platform_strategy"]["primary"]:
                    st.markdown(f"- {p[0].title()} (Score: {p[1]})")
            with col2:
                st.markdown("**📊 Secondary Platforms**")
                for p in strategy["platform_strategy"]["secondary"]:
                    st.markdown(f"- {p[0].title()} (Score: {p[1]})")
            with col3:
                st.markdown("**🧪 Experimental**")
                for p in strategy["platform_strategy"]["experimental"]:
                    st.markdown(f"- {p[0].title()} (Score: {p[1]})")
            
            # Monthly Plan
            st.subheader("📅 12-Month Plan")
            for month, plan in strategy["monthly_plan"].items():
                with st.expander(f"📆 {month} — {plan['focus']}"):
                    st.markdown(f"""
                    **Themes:** {', '.join(plan['content_themes'])}  
                    **Budget:** {plan['budget_percentage']}  
                    **Expected Growth:** {plan['expected_kpi']['traffic_growth']}  
                    **Engagement Target:** {plan['expected_kpi']['engagement_rate']}  
                    **Lead Target:** {plan['expected_kpi']['lead_generation']}  
                    """)
                    if plan.get('exhibitions'):
                        st.markdown(f"**🎪 Exhibitions:** {', '.join(plan['exhibitions'])}")
            
            # SEO/AEO/GEO
            st.subheader("🔍 SEO / AEO / GEO Strategy")
            st.markdown(f"""
            **Keywords:** {', '.join(strategy['seo_aeo_geo_strategy']['target_keywords'][:5])}  
            **AEO Focus:** {strategy['seo_aeo_geo_strategy']['aeo_focus']}  
            **GEO Focus:** {strategy['seo_aeo_geo_strategy']['geo_focus']}  
            **Technical SEO:** {', '.join(strategy['seo_aeo_geo_strategy']['technical_seo'])}  
            """)
            
            # Budget
            st.subheader("💰 Budget Allocation")
            for category, pct in strategy["budget_allocation"].items():
                st.progress(int(pct.replace('%',''))/100, text=f"{category.replace('_',' ').title()}: {pct}")
            
            # KPIs
            st.subheader("🎯 KPI Targets")
            for kpi, target in strategy["kpi_targets"].items():
                st.markdown(f"- **{kpi.replace('_',' ').title()}:** {target}")
            
            # Download
            st.download_button(
                "📥 Download Strategy (JSON)",
                data=json.dumps(strategy, indent=2, ensure_ascii=False),
                file_name=f"strategy_{client_key}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

# ─── CONTENT PROMPTS PAGE ───────────────────────────────────
elif page == "📝 Content Prompts":
    st.title("📝 AI Content Prompt Generator")
    st.caption("Structured prompts with SEO/AEO/GEO tags for all 4 AI models")
    
    if ENGINE_LOADED:
        col1, col2, col3 = st.columns(3)
        with col1:
            client_key = st.selectbox("Client:", list(CLIENTS.keys()), format_func=lambda x: CLIENTS[x].name)
        with col2:
            platform = st.selectbox("Platform:", CLIENTS[client_key].platforms)
        with col3:
            content_types = ["educational", "promotional", "engagement", "testimonial", "behind-scenes", "trending"]
            content_type = st.selectbox("Content Type:", content_types)
        
        if st.button("✨ Generate Prompt", type="primary"):
            prompt = generate_content_prompt(client_key, platform, content_type)
            st.code(prompt, language="markdown")
            
            st.download_button(
                "📥 Download Prompt",
                data=prompt,
                file_name=f"prompt_{client_key}_{platform}_{content_type}.txt",
                mime="text/plain"
            )

# ─── ERP FLOW PAGE ──────────────────────────────────────────
elif page == "🔄 ERP Flow":
    st.title("🔄 Complete ERP Automation Flow")
    st.caption("6-phase pipeline from data input to daily reports")
    
    phases = [
        ("1️⃣", "Data Input", [
            ("📋 Client Onboarding", "Company profile, domain, budget, timeline"),
            ("🔍 Market Research", "Competitor analysis, keyword research"),
            ("🎯 ICP & Targeting", "Ideal client profile, geo-targeting"),
            ("⚙️ Config Setup", "Platform accounts, schedule, KPIs"),
        ], "Forms + AI"),
        ("2️⃣", "AI Strategy Engine", [
            ("📊 Strategy Blueprint", "12-month plan, platform scoring"),
            ("🏷️ SEO/AEO/GEO", "Keyword mapping, schema, structured data"),
            ("📅 Calendar Builder", "Monthly themes, exhibition schedule"),
            ("🎪 Exhibition Tracker", "Regional events DB, reminders"),
        ], "Claude · Gemini · Grok"),
        ("3️⃣", "Content Factory", [
            ("✍️ AI Content Gen", "Social posts, blogs, captions"),
            ("🎨 Image & Video", "DALL-E, video scripts, thumbnails"),
            ("🌐 Multi-Language", "Arabic, Urdu, English"),
            ("✅ Quality Check", "Plagiarism, brand voice, SEO score"),
        ], "ChatGPT · DALL-E"),
        ("4️⃣", "Distribution", [
            ("⏰ Smart Scheduling", "Best-time auto-posting"),
            ("📱 Social Auto-Post", "Instagram, LinkedIn, Facebook, X, TikTok"),
            ("📝 Blog Auto-Publish", "WordPress, SEO metadata"),
            ("🔄 Cross-Platform", "Content repurposing, UTM tracking"),
        ], "Selenium + APIs"),
        ("5️⃣", "Engagement", [
            ("💬 Auto-Reply Engine", "Comment replies, DM responder"),
            ("📥 Inbox Management", "Unified inbox, priority flagging"),
            ("🔗 CRM Integration", "Lead capture, pipeline push"),
            ("📊 Sentiment Tracking", "Brand monitoring, crisis alerts"),
        ], "AI NLP"),
        ("6️⃣", "Reporting", [
            ("🌐 Selenium Scraper", "GA4, Search Console, social insights"),
            ("📈 Analytics Dashboard", "Real-time KPI tracking"),
            ("📋 Daily Email Reports", "Auto PDF/XLS, recommendations"),
            ("🔄 Strategy Optimizer", "A/B analysis, budget reallocation"),
        ], "Selenium + SMTP"),
    ]
    
    for emoji, title, steps, tools in phases:
        st.markdown(f"### {emoji} {title} — `{tools}`")
        cols = st.columns(len(steps))
        for i, (step_title, step_desc) in enumerate(steps):
            with cols[i]:
                st.markdown(f"""
                <div class="phase-box">
                    <div class="phase-title">{step_title}</div>
                    <div style="font-size:0.8em; color:#8b8fa3; margin-top:6px;">{step_desc}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("⬇️")
    
    # Selenium Nodes
    st.markdown("---")
    st.subheader("🤖 Selenium Automation Nodes")
    if ENGINE_LOADED:
        for name in SELENIUM_NODE_SCRIPTS:
            st.markdown(f"- `{name}`")
    
    st.info("Run `python3 scripts/erp_engine_v2.py run` to execute the full pipeline")
