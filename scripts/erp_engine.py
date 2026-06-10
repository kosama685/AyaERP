"""
AyaERP — Marketing Automation Engine
======================================
Selenium-based daily reporting, AI content generation,
social media scheduling, and strategy automation.
Author: Aya 🦅 | Built for Usama Khan
"""

import json
import os
import time
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

# ─── Configuration ───────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "clients.json"
REPORTS_DIR = BASE_DIR / "reports"
STRATEGIES_DIR = BASE_DIR / "strategies"
CONTENT_DIR = BASE_DIR / "templates" / "content"

@dataclass
class Client:
    """Client configuration for automation"""
    name: str
    domain: str
    region: str  # SA, UK, EU, US, PK
    industry: str
    platforms: list  # ['instagram', 'linkedin', 'facebook', 'tiktok', 'x']
    target_keywords: list
    content_languages: list  # ['en', 'ar', 'ur']
    posting_schedule: dict   # {platform: {days: [], times: []}}
    selenium_selectors: dict # CSS selectors for scraping analytics
    email_report_to: str
    monthly_budget: float = 0.0
    active: bool = True

# ─── CLIENT DATABASE ─────────────────────────────────────────
CLIENTS = {
    "fandaqah": Client(
        name="Fandaqah",
        domain="fandaqah.com",
        region="SA",
        industry="Hospitality",
        platforms=["instagram", "tiktok", "facebook", "x"],
        target_keywords=[
            "فندق", "حجز فنادق السعودية", "Saudi hotels",
            "best hotels Saudi Arabia", " luxury stay Saudi",
            "accommodation Riyadh", "hotel booking KSA"
        ],
        content_languages=["ar", "en"],
        posting_schedule={
            "instagram": {"days": [0,1,2,3,4,5,6], "times": ["20:00", "18:00"]},
            "tiktok": {"days": [0,2,4,6], "times": ["20:00", "21:00"]},
            "facebook": {"days": [0,1,3,5], "times": ["19:00"]},
            "x": {"days": [1,2,3,4,5], "times": ["09:00", "16:00"]},
        },
        selenium_selectors={
            "google_analytics": "#viewSelector",
            "search_console": ".metric-value",
            "social_insights": "[data-testid='insights']"
        },
        email_report_to="usama@example.com",
        monthly_budget=3000.0,
    ),
    "dyafa": Client(
        name="Dyafa",
        domain="dyafa.com",
        region="SA",
        industry="Hospitality",
        platforms=["linkedin", "instagram", "x"],
        target_keywords=[
            "ضيافة", "hospitality Saudi Arabia", "Saudi catering",
            "event management KSA", "corporate hospitality Riyadh"
        ],
        content_languages=["ar", "en"],
        posting_schedule={
            "linkedin": {"days": [0,1,2,3,4], "times": ["09:00", "16:00"]},
            "instagram": {"days": [0,1,3,5,6], "times": ["20:00"]},
            "x": {"days": [0,1,2,3,4], "times": ["10:00", "17:00"]},
        },
        selenium_selectors={
            "google_analytics": "#viewSelector",
            "search_console": ".metric-value",
            "social_insights": "[data-testid='insights']"
        },
        email_report_to="usama@example.com",
        monthly_budget=2500.0,
    ),
    "bestwebdeveloper": Client(
        name="BestWebDeveloper",
        domain="bestwebdeveloper.org",
        region="UK/EU/US",
        industry="Web Development / IT",
        platforms=["linkedin", "x", "instagram"],
        target_keywords=[
            "web developer UK", "best web development agency",
            "custom website development", "WordPress developer Europe",
            "eCommerce development USA", "web design company"
        ],
        content_languages=["en"],
        posting_schedule={
            "linkedin": {"days": [0,1,2,3,4], "times": ["08:00", "12:00", "17:00"]},
            "x": {"days": [0,1,2,3,4,5], "times": ["09:00", "14:00", "18:00"]},
            "instagram": {"days": [0,2,4,6], "times": ["19:00"]},
        },
        selenium_selectors={
            "google_analytics": "#viewSelector",
            "search_console": ".metric-value",
            "social_insights": "[data-testid='insights']"
        },
        email_report_to="usama@example.com",
        monthly_budget=2000.0,
    ),
    "sastamilaga": Client(
        name="SastaMilaga",
        domain="sastamilaga.com",
        region="PK",
        industry="E-commerce",
        platforms=["facebook", "instagram", "tiktok", "x"],
        target_keywords=[
            "سستا ملاگا", "online shopping Pakistan",
            "best deals Pakistan", "cheap products online Pakistan",
            "eCommerce Pakistan", "buy online Karachi Lahore"
        ],
        content_languages=["ur", "en"],
        posting_schedule={
            "facebook": {"days": [0,1,2,3,4,5,6], "times": ["19:00", "21:00"]},
            "instagram": {"days": [0,1,2,3,4,5,6], "times": ["20:00"]},
            "tiktok": {"days": [0,2,4,6], "times": ["21:00"]},
            "x": {"days": [0,1,3,5], "times": ["10:00", "22:00"]},
        },
        selenium_selectors={
            "google_analytics": "#viewSelector",
            "search_console": ".metric-value",
            "social_insights": "[data-testid='insights']"
        },
        email_report_to="usama@example.com",
        monthly_budget=3500.0,
    ),
}

# ─── PLATFORM BEST TIMES DATABASE ────────────────────────────
BEST_TIMES = {
    "SA": {
        "instagram": {"best": ["20:00", "21:00", "18:00"], "days": [4,5,6,0]},
        "tiktok": {"best": ["20:00", "21:00", "22:00"], "days": [4,5,6]},
        "linkedin": {"best": ["09:00", "10:00", "16:00"], "days": [0,1,2,3]},
        "facebook": {"best": ["19:00", "20:00", "13:00"], "days": [4,5,6]},
        "x": {"best": ["09:00", "10:00", "16:00", "22:00"], "days": [0,1,2,3,4]},
    },
    "UK": {
        "instagram": {"best": ["19:00", "20:00", "12:00"], "days": [3,4,5,6]},
        "linkedin": {"best": ["08:00", "09:00", "12:00", "17:00"], "days": [1,2,3]},
        "x": {"best": ["08:00", "09:00", "12:00", "17:00"], "days": [1,2,3,4]},
        "facebook": {"best": ["13:00", "15:00", "19:00"], "days": [4,5,6]},
    },
    "US": {
        "instagram": {"best": ["11:00", "13:00", "19:00"], "days": [3,4,5,6]},
        "linkedin": {"best": ["08:00", "10:00", "12:00"], "days": [1,2,3,4]},
        "x": {"best": ["08:00", "09:00", "12:00", "17:00"], "days": [1,2,3,4]},
        "facebook": {"best": ["09:00", "13:00", "15:00"], "days": [4,5,6]},
    },
    "EU": {
        "instagram": {"best": ["18:00", "19:00", "21:00"], "days": [4,5,6]},
        "linkedin": {"best": ["08:00", "09:00", "12:00", "17:00"], "days": [1,2,3]},
        "x": {"best": ["08:00", "09:00", "12:00"], "days": [1,2,3,4]},
        "facebook": {"best": ["12:00", "15:00", "19:00"], "days": [4,5,6]},
    },
    "PK": {
        "instagram": {"best": ["19:00", "20:00", "21:00"], "days": [4,5,6,0]},
        "tiktok": {"best": ["21:00", "22:00", "20:00"], "days": [4,5,6]},
        "facebook": {"best": ["19:00", "20:00", "21:00"], "days": [4,5,6,0]},
        "x": {"best": ["10:00", "22:00", "21:00"], "days": [0,1,2,3,4]},
    },
}

# ─── BEST MONTHS BY REGION & INDUSTRY ────────────────────────
BEST_MONTHS = {
    "SA": {
        "Hospitality": ["Nov", "Dec", "Jan", "Feb", "Ramadan", "Hajj season"],
        "general": ["Sep", "Oct", "Nov", "Jan", "Feb", "Mar"],
        "exhibitions": ["LEAP (Feb)", "Saudi Food Show (May)", "Arabian Travel Market (Apr-May)", "Cityscape (Nov)"],
    },
    "UK": {
        "general": ["Jan", "Feb", "Mar", "Sep", "Oct"],
        "exhibitions": ["London Tech Week (Jun)", "Birmingham Tech (Oct)", "Marketing Week Live (Oct)"],
    },
    "EU": {
        "general": ["Jan", "Feb", "Mar", "Sep", "Oct", "Nov"],
        "exhibitions": ["Web Summit Lisbon (Nov)", "MWC Barcelona (Feb-Mar)", "DMEXCO Cologne (Sep)"],
    },
    "US": {
        "general": ["Jan", "Feb", "Mar", "Sep", "Oct"],
        "exhibitions": ["CES Las Vegas (Jan)", "SXSW Austin (Mar)", "INBOUND Boston (Sep)"],
    },
    "PK": {
        "E-commerce": ["Ramadan", "Eid seasons", "Nov", "Dec", "Jan"],
        "general": ["Nov", "Dec", "Jan", "Feb", "Mar", "Ramadan", "Eid"],
        "exhibitions": ["ITCN Asia Karachi (Sep)", "eCommerce Expo Lahore"],
    },
}


# ═══════════════════════════════════════════════════════════════
# 1. SELENIUM DAILY REPORT ENGINE
# ═══════════════════════════════════════════════════════════════

# NOTE: Selenium requires:
#   pip install selenium webdriver-manager
#   Chrome/Chromium browser installed

SELENIUM_SCRIPT_TEMPLATE = '''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
import time
from datetime import datetime

class DailyReportScraper:
    """Automated daily report scraping using Selenium.
    
    Opens browser tabs, logs into analytics platforms,
    scrapes data, saves reports.
    """
    
    def __init__(self, client_key, headless=True):
        self.client_key = client_key
        self.client_config = {}  # loaded from CLIENTS dict
        self.options = Options()
        if headless:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.options
        )
        self.wait = WebDriverWait(self.driver, 20)
        self.report = {"date": datetime.now().isoformat(), "platforms": {}}
    
    def login_google_analytics(self):
        """Login to Google Analytics 4"""
        self.driver.get("https://analytics.google.com/")
        # Auto-fill login (uses saved session/cookies)
        try:
            # Load saved cookies
            with open(f"cookies/{self.client_key}_ga.json", "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        except:
            print("[!] Manual login may be required first time")
    
    def scrape_ga4_metrics(self):
        """Scrape key GA4 metrics"""
        metrics = {}
        try:
            # Users
            users_el = self.driver.find_element(By.CSS_SELECTOR, "[data-metric='activeUsers'] .value")
            metrics["active_users"] = users_el.text
            
            # Sessions
            sessions_el = self.driver.find_element(By.CSS_SELECTOR, "[data-metric='sessions'] .value")
            metrics["sessions"] = sessions_el.text
            
            # Conversions
            conv_el = self.driver.find_element(By.CSS_SELECTOR, "[data-metric='conversions'] .value")
            metrics["conversions"] = conv_el.text
            
            # Bounce Rate
            bounce_el = self.driver.find_element(By.CSS_SELECTOR, "[data-metric='bounceRate'] .value")
            metrics["bounce_rate"] = bounce_el.text
        except Exception as e:
            metrics["error"] = str(e)
        return metrics
    
    def login_search_console(self):
        """Login to Google Search Console"""
        self.driver.get("https://search.google.com/search-console")
        try:
            with open(f"cookies/{self.client_key}_gsc.json", "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        except:
            print("[!] Manual login may be required first time")
    
    def scrape_gsc_metrics(self):
        """Scrape Search Console performance"""
        metrics = {}
        try:
            clicks = self.driver.find_element(By.CSS_SELECTOR, ".metric.clicks .value")
            impressions = self.driver.find_element(By.CSS_SELECTOR, ".metric.impressions .value")
            ctr = self.driver.find_element(By.CSS_SELECTOR, ".metric.ctr .value")
            position = self.driver.find_element(By.CSS_SELECTOR, ".metric.position .value")
            
            metrics = {
                "clicks": clicks.text,
                "impressions": impressions.text,
                "ctr": ctr.text,
                "avg_position": position.text
            }
        except Exception as e:
            metrics["error"] = str(e)
        return metrics
    
    def login_social_platform(self, platform):
        """Login to social media platform"""
        urls = {
            "instagram": "https://www.instagram.com/",
            "facebook": "https://business.facebook.com/",
            "linkedin": "https://www.linkedin.com/company/",
            "x": "https://analytics.twitter.com/",
            "tiktok": "https://www.tiktok.com/business/"
        }
        self.driver.get(urls.get(platform, ""))
        try:
            with open(f"cookies/{self.client_key}_{platform}.json", "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        except:
            print(f"[!] Manual {platform} login may be required first time")
    
    def scrape_social_metrics(self, platform):
        """Scrape social media insights"""
        # Generic selectors — customize per platform
        selectors = {
            "instagram": {
                "followers": "._ac2a span",
                "engagement": ".x1lliihq span",
                "reach": ".x78zum5 span"
            },
            "facebook": {
                "followers": "[data-testid='page_likes']",
                "reach": "[data-testid='page_post_reach']",
                "engagement": "[data-testid='page_engagement']"
            }
        }
        metrics = {}
        try:
            for metric, selector in selectors.get(platform, {}).items():
                el = self.driver.find_element(By.CSS_SELECTOR, selector)
                metrics[metric] = el.text
        except Exception as e:
            metrics["error"] = str(e)
        return metrics
    
    def run_daily_report(self):
        """Execute full daily report scrape"""
        print(f"[🔄] Starting daily report for {self.client_key}")
        
        # GA4
        print("  → Google Analytics 4...")
        self.login_google_analytics()
        time.sleep(3)
        self.report["platforms"]["google_analytics"] = self.scrape_ga4_metrics()
        
        # Search Console
        print("  → Google Search Console...")
        self.login_search_console()
        time.sleep(3)
        self.report["platforms"]["search_console"] = self.scrape_gsc_metrics()
        
        # Social Platforms
        for platform in ["instagram", "facebook", "linkedin", "x"]:
            print(f"  → {platform.title()}...")
            self.login_social_platform(platform)
            time.sleep(3)
            self.report["platforms"][platform] = self.scrape_social_metrics(platform)
        
        # Save report
        filename = f"reports/{self.client_key}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, "w") as f:
            json.dump(self.report, f, indent=2, default=str)
        
        print(f"[✅] Report saved: {filename}")
        self.driver.quit()
        return self.report

# Usage: DailyReportScraper("fandaqah").run_daily_report()
'''

# ═══════════════════════════════════════════════════════════════
# 2. AI CONTENT GENERATION ENGINE
# ═══════════════════════════════════════════════════════════════

def generate_content_prompt(client_key: str, platform: str, content_type: str) -> str:
    """
    Generate a structured AI prompt for content creation.
    
    Supports: Grok, Gemini Pro, Claude Pro Max, ChatGPT Pro
    The output prompt includes SEO/AEO/GEO tags, keywords,
    titles, descriptions, hashtags, and image/video specs.
    """
    client = CLIENTS.get(client_key)
    if not client:
        return f"Client '{client_key}' not found."
    
    times = BEST_TIMES.get(client.region, {}).get(platform, {})
    best_time = times.get("best", ["09:00"])[0] if times else "09:00"
    
    prompt = f'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI CONTENT GENERATION BRIEF
Client: {client.name} ({client.domain})
Region: {client.region} | Industry: {client.industry}
Platform: {platform.upper()} | Content Type: {content_type}
Best Post Time: {best_time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TASK: Generate 1 {platform} post for {client.name}

REQUIREMENTS:
1. Title/Hook: Attention-grabbing, under 60 chars
2. Body: {200 if platform in ['linkedin', 'facebook'] else 150} words max
3. SEO Tags: Include these target keywords naturally:
   {', '.join(client.target_keywords[:5])}
4. AEO (Answer Engine Optimization): Structure for Google SGE/AI overviews
5. GEO (Generative Engine Optimization): Include entities, facts, stats
6. Hashtags: 5-10 relevant hashtags (mix broad + niche)
7. CTA: Clear call-to-action
8. Language: {', '.join(client.content_languages)}
9. Image Spec: 1080x1080 (square) / 1080x1920 (story/reel)
10. Alt Text: Descriptive for SEO

OUTPUT FORMAT:
[TITLE]
[CONTENT BODY]
[HASHTAGS]
[IMAGE PROMPT for DALL-E/Midjourney]
[ALT TEXT]
[META DESCRIPTION for SEO]
'''
    return prompt.strip()


def generate_bulk_content_prompts(client_key: str) -> list:
    """Generate a week's worth of content prompts for all platforms."""
    client = CLIENTS.get(client_key)
    if not client:
        return []
    
    content_types = ["educational", "promotional", "engagement", "testimonial", "behind-scenes", "trending", "educational"]
    prompts = []
    
    for i, platform in enumerate(client.platforms):
        ct = content_types[i % len(content_types)]
        for day_offset in range(min(7, len(client.posting_schedule.get(platform, {}).get("days", [0])))):
            prompt = generate_content_prompt(client_key, platform, ct)
            prompts.append({
                "day": day_offset,
                "platform": platform,
                "type": ct,
                "prompt": prompt
            })
    
    return prompts


# ═══════════════════════════════════════════════════════════════
# 3. STRATEGY GENERATOR
# ═══════════════════════════════════════════════════════════════

def generate_marketing_strategy(client_key: str) -> dict:
    """
    Generate a complete marketing strategy document for any client.
    Includes: platform mix, monthly plan, exhibition calendar,
    budget allocation, KPI targets.
    """
    client = CLIENTS.get(client_key)
    if not client:
        return {"error": f"Client '{client_key}' not found"}
    
    region_data = BEST_MONTHS.get(client.region, {})
    industry_months = region_data.get(client.industry, region_data.get("general", []))
    exhibitions = region_data.get("exhibitions", [])
    
    # Platform scoring
    platform_scores = _score_platforms(client.region, client.industry)
    
    strategy = {
        "client": client.name,
        "domain": client.domain,
        "generated": datetime.now().isoformat(),
        "executive_summary": f"Marketing strategy for {client.name} targeting {client.region} in {client.industry}",
        
        "platform_strategy": {
            "primary": platform_scores[:1],
            "secondary": platform_scores[1:3],
            "experimental": platform_scores[3:],
        },
        
        "monthly_plan": {
            month: {
                "focus": _get_monthly_focus(month, client.industry),
                "content_themes": _get_content_themes(month, client.region, client.industry),
                "budget_percentage": _get_budget_allocation(month),
                "exhibitions": [e for e in exhibitions if month[:3].lower() in e.lower()],
                "expected_kpi": {
                    "traffic_growth": "5-15%",
                    "engagement_rate": "3-7%",
                    "lead_generation": "10-30 leads",
                }
            }
            for month in ["January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November", "December"]
        },
        
        "content_calendar": {
            "weekly_posts": len(client.platforms) * 7,
            "content_mix": {
                "educational": "40%",
                "promotional": "20%",
                "engagement": "20%",
                "user_generated": "10%",
                "behind_scenes": "10%"
            },
            "ai_tools": ["Grok (research)", "Claude Pro Max (long-form)", "ChatGPT Pro (social)", "Gemini Pro (SEO/AEO)"],
        },
        
        "seo_aeo_geo_strategy": {
            "target_keywords": client.target_keywords,
            "aeo_focus": "Structure content as Q&A for Google AI Overviews",
            "geo_focus": "Include entity markup, structured data, E-E-A-T signals",
            "technical_seo": ["Schema.org markup", "Core Web Vitals", "Mobile-first", "XML sitemap"],
        },
        
        "exhibition_calendar": exhibitions,
        
        "budget_allocation": {
            "content_creation": "30%",
            "paid_ads": "25%",
            "tools_subscriptions": "15%",
            "exhibitions_events": "20%",
            "miscellaneous": "10%",
        },
        
        "kpi_targets": {
            "organic_traffic": "+25% in 6 months",
            "social_followers": "+15% quarterly",
            "engagement_rate": ">4%",
            "lead_conversion": ">3%",
            "client_retention": ">90%",
        },
        
        "reminders": [
            {"type": "daily", "items": ["Check analytics", "Reply to comments", "Post scheduled content"]},
            {"type": "weekly", "items": ["Competitor analysis", "Content planning", "Team sync"]},
            {"type": "monthly", "items": ["Full report generation", "Strategy review", "Client QBR prep"]},
            {"type": "quarterly", "items": ["Strategy pivot check", "Budget review", "Exhibition planning"]},
        ]
    }
    
    return strategy


def _score_platforms(region: str, industry: str) -> list:
    """Score platforms by region + industry fit."""
    base_scores = {
        "SA": {"instagram": 9.5, "tiktok": 8.5, "x": 7.5, "linkedin": 8.0, "facebook": 7.0},
        "UK": {"linkedin": 9.5, "x": 8.0, "instagram": 7.5, "facebook": 6.5},
        "US": {"linkedin": 9.0, "instagram": 8.5, "x": 8.0, "tiktok": 7.5, "facebook": 7.0},
        "EU": {"linkedin": 9.0, "x": 7.5, "instagram": 7.5, "facebook": 6.5},
        "PK": {"facebook": 9.5, "instagram": 8.5, "tiktok": 8.0, "x": 6.0},
    }
    scores = base_scores.get(region, {"linkedin": 8, "instagram": 7, "facebook": 7})
    
    # Industry modifiers
    if industry == "Hospitality":
        scores = {k: v + (1.0 if k in ["instagram", "tiktok"] else 0) for k, v in scores.items()}
    elif industry == "Web Development / IT":
        scores = {k: v + (1.0 if k in ["linkedin", "x"] else 0) for k, v in scores.items()}
    elif industry == "E-commerce":
        scores = {k: v + (1.0 if k in ["facebook", "instagram", "tiktok"] else 0) for k, v in scores.items()}
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def _get_monthly_focus(month: str, industry: str) -> str:
    focuses = {
        "January": "New year strategy launch, goal setting",
        "February": "Valentine's campaigns, LEAP conference (SA)",
        "March": "Spring campaigns, Ramadan prep",
        "April": "Q1 review, Arabian Travel Market",
        "May": "Summer campaign prep",
        "June": "Mid-year review, summer content",
        "July": "Summer engagement, back-to-school prep",
        "August": "Pre-Q4 planning, content bank build",
        "September": "Q4 ramp-up, fall campaigns",
        "October": "Peak season campaigns",
        "November": "Black Friday / White Friday, Web Summit",
        "December": "Year-end, holiday campaigns, annual review"
    }
    return focuses.get(month, "General marketing activities")


def _get_content_themes(month: str, region: str, industry: str) -> list:
    """Get content themes based on month, region, and industry."""
    themes = {
        "SA": {
            "January": ["Winter travel", "New year deals", "Saudi Seasons"],
            "February": ["LEAP tech event", "Valentine's", "Winter escapes"],
            "March": ["Ramadan preparation", "Spring travel"],
            "April": ["Eid al-Fitr", "Spring campaigns"],
            "May": ["Summer preview", "Travel planning"],
            "June": ["Eid al-Adha", "Summer travel", "Hajj"],
            "July": ["Summer deals", "Staycation"],
            "August": ["Back to school", "Pre-fall planning"],
            "September": ["National Day (Sep 23)", "Fall campaigns"],
            "October": ["Riyadh Season", "Autumn travel"],
            "November": ["Winter preview", "Early bookings"],
            "December": ["Winter holidays", "New Year"]
        }
    }
    return themes.get(region, {}).get(month, ["Industry trends", "Client success stories", "Educational content"])


def _get_budget_allocation(month: str) -> str:
    peak = ["October", "November", "December", "February", "March"]
    mid = ["January", "April", "May", "September"]
    if month in peak: return "15%"
    elif month in mid: return "8%"
    return "5%"


# ═══════════════════════════════════════════════════════════════
# 4. DAILY REPORT EMAILER
# ═══════════════════════════════════════════════════════════════

def generate_daily_report(client_key: str) -> str:
    """Generate a formatted daily report."""
    client = CLIENTS.get(client_key)
    if not client:
        return f"Client not found: {client_key}"
    
    report = f'''
╔══════════════════════════════════════════════════════════════╗
║  DAILY MARKETING REPORT — {client.name} ({client.domain})
║  Date: {datetime.now().strftime("%Y-%m-%d")}
║  Region: {client.region} | Industry: {client.industry}
╚══════════════════════════════════════════════════════════════╝

📊 SEO PERFORMANCE
  Keywords Tracked: {len(client.target_keywords)}
  Top Keywords: {', '.join(client.target_keywords[:3])}
  [Run Selenium scraper for live data]

📱 SOCIAL MEDIA
  Platforms Active: {', '.join(client.platforms)}
  Posts Today: Auto-scheduled
  Best Posting Times: See platform matrix

💰 BUDGET STATUS
  Monthly Budget: ${client.monthly_budget:,.2f}
  Spent to Date: [Selenium scrape needed]
  Remaining: [Calculate from scraped data]

🎯 UPCOMING ACTIONS
  Next Exhibition: {_get_next_exhibition(client.region)}
  Reminders: Check reminders list below

🔔 REMINDERS
  ☐ Reply to pending comments & messages
  ☐ Review today's content performance
  ☐ Check competitor activity
  ☐ Update pipeline in CRM

──────────────────────────────────────────────────────────────
Report auto-generated by AyaERP 🦅 | {datetime.now().isoformat()}
'''
    return report


def _get_next_exhibition(region: str) -> str:
    exhibitions = {
        "SA": "Arabian Travel Market (Apr-May) or LEAP (Feb)",
        "UK": "London Tech Week (Jun) or Birmingham Tech (Oct)",
        "EU": "Web Summit Lisbon (Nov) or MWC Barcelona (Feb-Mar)",
        "US": "SXSW Austin (Mar) or INBOUND Boston (Sep)",
        "PK": "ITCN Asia Karachi (Sep) or eCommerce Expo Lahore",
    }
    return exhibitions.get(region, "Check regional calendar")


def send_email_report(to_email: str, subject: str, body: str, smtp_config: dict = None):
    """
    Send report via email.
    
    SMTP_CONFIG = {
        "server": "smtp.gmail.com",
        "port": 587,
        "user": "your-email@gmail.com",
        "password": "app-password"
    }
    """
    if not smtp_config:
        print("[!] SMTP not configured. Report saved locally instead.")
        return False
    
    msg = MIMEMultipart()
    msg["From"] = smtp_config["user"]
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP(smtp_config["server"], smtp_config["port"]) as server:
        server.starttls()
        server.login(smtp_config["user"], smtp_config["password"])
        server.send_message(msg)
    
    return True


# ═══════════════════════════════════════════════════════════════
# 5. MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════

def run_daily_automation(client_keys: list = None):
    """
    Main orchestrator — runs daily automation for all clients.
    
    Flow:
    1. Generate content prompts for all clients
    2. Generate/update marketing strategies
    3. Create daily report
    4. Save everything
    """
    if client_keys is None:
        client_keys = list(CLIENTS.keys())
    
    results = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    for key in client_keys:
        print(f"\n{'='*60}")
        print(f"🦅 Processing: {CLIENTS[key].name}")
        print(f"{'='*60}")
        
        # 1. Content prompts
        print("  📝 Generating content prompts...")
        prompts = generate_bulk_content_prompts(key)
        
        # 2. Strategy
        print("  📋 Generating marketing strategy...")
        strategy = generate_marketing_strategy(key)
        
        # 3. Daily report
        print("  📊 Generating daily report...")
        report = generate_daily_report(key)
        
        # 4. Save outputs
        out_dir = REPORTS_DIR / key / timestamp
        out_dir.mkdir(parents=True, exist_ok=True)
        
        with open(out_dir / "content_prompts.json", "w") as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)
        
        with open(out_dir / "strategy.json", "w") as f:
            json.dump(strategy, f, indent=2, ensure_ascii=False)
        
        with open(out_dir / "daily_report.txt", "w") as f:
            f.write(report)
        
        results[key] = {
            "prompts_generated": len(prompts),
            "strategy_saved": True,
            "report_saved": True,
            "output_dir": str(out_dir)
        }
        
        print(f"  ✅ Done! Output: {out_dir}")
    
    # Master summary
    summary_path = REPORTS_DIR / f"master_summary_{timestamp}.json"
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n{'='*60}")
    print(f"🦅 ALL DONE — Master summary: {summary_path}")
    print(f"{'='*60}")
    
    return results


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════╗
║  AyaERP 🦅 — Marketing Automation Command Center
╠══════════════════════════════════════════════════════════════║
║  Usage:
║    python erp_engine.py run              — Full daily automation
║    python erp_engine.py content CLIENT   — Generate content prompts
║    python erp_engine.py strategy CLIENT  — Generate strategy doc
║    python erp_engine.py report CLIENT    — Generate daily report
║    python erp_engine.py clients          — List all clients
║    python erp_engine.py selenium-script  — Print Selenium script
╚══════════════════════════════════════════════════════════════╝
        """)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "run":
        run_daily_automation()
    
    elif cmd == "content" and len(sys.argv) > 2:
        prompts = generate_bulk_content_prompts(sys.argv[2])
        print(json.dumps(prompts, indent=2, ensure_ascii=False))
    
    elif cmd == "strategy" and len(sys.argv) > 2:
        strategy = generate_marketing_strategy(sys.argv[2])
        print(json.dumps(strategy, indent=2, ensure_ascii=False))
    
    elif cmd == "report" and len(sys.argv) > 2:
        print(generate_daily_report(sys.argv[2]))
    
    elif cmd == "clients":
        for k, v in CLIENTS.items():
            print(f"  {v.name} ({v.domain}) — {v.region} | {v.industry}")
    
    elif cmd == "selenium-script":
        print(SELENIUM_SCRIPT_TEMPLATE)
    
    else:
        print(f"Unknown command: {cmd}")
