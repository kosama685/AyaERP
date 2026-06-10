# AyaERP 🦅 — Marketing Automation Engine

**Built for:** Usama Khan | Director of Sales & Marketing  
**Regions:** Saudi Arabia, Estonia (EU), UK, USA, Pakistan  
**Clients:** fandaqah.com, dyafa.com, bestwebdeveloper.org, sastamilaga.com

---

## Quick Start

```bash
# Install dependencies (for Selenium features)
pip install selenium webdriver-manager

# Run full daily automation (all clients)
python3 scripts/erp_engine.py run

# Run v2 with LLM Router + Lead Detection
python3 scripts/erp_engine_v2.py run

# Generate strategy for one client
python3 scripts/erp_engine.py strategy fandaqah

# Generate content prompts
python3 scripts/erp_engine.py content sastamilaga

# Test LLM routing (which AI to use for what)
python3 scripts/erp_engine_v2.py route seo_aeo_geo

# Test lead detection
python3 scripts/erp_engine_v2.py lead "I need SEO for my hotel in Riyadh"

# View Selenium automation templates
python3 scripts/erp_engine_v2.py scripts

# List all clients
python3 scripts/erp_engine.py clients
```

## Project Structure

```
marketing-erp/
├── dashboard/
│   ├── index.html          ← Live command center (open in browser)
│   └── flowchart.html      ← 6-phase automation flow visualization
├── scripts/
│   ├── erp_engine.py       ← V1: Core engine (strategy, content, reports, Selenium)
│   └── erp_engine_v2.py    ← V2: LLM Router, Lead Detection, Exhibitions, Selenium templates
├── assets/
│   └── diagram1.svg        ← Reference flow diagram
└── reports/                ← Auto-generated reports per client
    ├── fandaqah/
    ├── dyafa/
    ├── bestwebdeveloper/
    ├── sastamilaga/
    └── master_summary.json
```

## V1 Features (erp_engine.py)
- Client config for all 4 clients with region/industry/keywords
- Marketing strategy generator (12-month plans)
- AI content prompt generator with SEO/AEO/GEO tags
- Best posting times by region (SA, UK, EU, US, PK)
- Platform scoring by region + industry
- Monthly content themes (Ramadan, LEAP, Hajj, etc.)
- Budget allocation by month
- Daily report generator with email support
- Selenium scraper template for GA4, Search Console, Social

## V2 Features (erp_engine_v2.py)
- **LLM Router**: Routes tasks to cheapest/best AI to save tokens
  - ChatGPT Pro → Outlines, captions, auto-replies
  - Claude Pro Max → Long-form strategy, lead scoring
  - Grok → Real-time trends, competitor news
  - Gemini Pro → Images, video, SEO/AEO/GEO
- **Lead Detection**: Auto-scores comments/DMs for sales intent (0-100)
  - HIGH (60+): Immediate WhatsApp/Email alert
  - MEDIUM (30-59): Auto-reply + CRM
  - LOW (<30): Auto-reply only
  - Supports Arabic + Urdu keywords
- **Exhibition Database**: 25+ exhibitions across SA, UK, EU, US, PK
  - Filterable by niche (tech, hospitality, marketing, ecommerce)
  - Upcoming exhibition tracking
- **6 Selenium Templates**: Trends, Login, Posting, Comments, Reply, Analytics

## Going Live Checklist
1. Save browser cookies for each platform (first manual login)
2. Add SMTP credentials for email reports
3. Add social media API keys for native posting
4. Set up daily cron: `0 8 * * * cd /path/to/marketing-erp && python3 scripts/erp_engine_v2.py run`
5. Add AI API keys (OpenAI, Anthropic, Google, xAI)

## Estimated Costs
- AI tokens per client per day: ~$0.08
- All 4 clients per day: ~$0.32
- Monthly AI cost: ~$10

---
Built by Aya 🦅 | 2026
