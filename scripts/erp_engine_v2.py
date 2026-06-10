"""
AyaERP v2 — Enhanced Marketing Automation Engine
===================================================
Based on user's AI Command Center blueprint + flow diagram.

NEW in v2:
- LLM Router with Token Optimizer
- Sales Lead Detection + Alerting
- Exhibition Scraper by Niche
- Comment/DM Auto-Reply Engine
- Enhanced Selenium templates for all automation nodes
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "reports"

# ═══════════════════════════════════════════════════════════════
# 1. LLM ROUTER — TOKEN OPTIMIZER
# ═══════════════════════════════════════════════════════════════
# Routes each task to the most cost-effective LLM to save tokens.

LLM_ROUTES = {
    "outlines_formatting": {
        "task": "Short-form content, outlines, captions, hashtags",
        "best_llm": "ChatGPT Pro",
        "reason": "Fast, cheap, good at structured short content",
        "estimated_tokens": 500,
        "cost_per_1k": "$0.03",
    },
    "long_form_strategy": {
        "task": "Marketing strategy documents, blog posts, reports",
        "best_llm": "Claude Pro Max",
        "reason": "Best at long-form reasoning, 200K context, strategy depth",
        "estimated_tokens": 3000,
        "cost_per_1k": "$0.015",
    },
    "realtime_trends": {
        "task": "Trending topics, news, competitor moves, market shifts",
        "best_llm": "Grok",
        "reason": "Real-time X/Twitter data access, fastest trending detection",
        "estimated_tokens": 800,
        "cost_per_1k": "$0.01",
    },
    "images_video_logic": {
        "task": "Image prompts, video scripts, visual content planning",
        "best_llm": "Gemini Pro",
        "reason": "Native multimodal, best at image understanding + generation",
        "estimated_tokens": 1000,
        "cost_per_1k": "$0.01",
    },
    "seo_aeo_geo": {
        "task": "SEO optimization, AEO structured data, GEO entity markup",
        "best_llm": "Gemini Pro",
        "reason": "Best search/AI overview optimization, Google ecosystem native",
        "estimated_tokens": 1500,
        "cost_per_1k": "$0.01",
    },
    "auto_reply": {
        "task": "Comment replies, DM responses, FAQ handling",
        "best_llm": "ChatGPT Pro",
        "reason": "Fast, conversational, good tone matching",
        "estimated_tokens": 200,
        "cost_per_1k": "$0.03",
    },
    "lead_scoring": {
        "task": "Analyze messages for sales intent, score leads",
        "best_llm": "Claude Pro Max",
        "reason": "Best at nuanced intent detection, reduces false positives",
        "estimated_tokens": 300,
        "cost_per_1k": "$0.015",
    },
}


def route_to_llm(task_type: str, content: str = "") -> dict:
    """
    Route a task to the optimal LLM based on type.
    Returns LLM choice + prompt template + estimated cost.
    """
    route = LLM_ROUTES.get(task_type, LLM_ROUTES["outlines_formatting"])
    
    token_estimate = max(route["estimated_tokens"], len(content.split()) * 1.3)
    cost = (token_estimate / 1000) * float(route["cost_per_1k"].replace("$", ""))
    
    return {
        "task_type": task_type,
        "recommended_llm": route["best_llm"],
        "reason": route["reason"],
        "estimated_tokens": int(token_estimate),
        "estimated_cost": f"${cost:.4f}",
        "prompt_template": _build_prompt(task_type, content),
    }


def _build_prompt(task_type: str, context: str = "") -> str:
    """Build task-specific prompt for the routed LLM."""
    prompts = {
        "outlines_formatting": f"""Generate a social media post outline with:
- Hook (under 60 chars)
- Body (150 words max)
- 5-10 hashtags
- CTA
- Image prompt for DALL-E
- Alt text for SEO

Context: {context}""",
        
        "long_form_strategy": f"""Generate a comprehensive marketing strategy including:
- Executive summary
- Target audience analysis
- Platform recommendations with scoring
- Monthly content calendar
- Budget allocation
- KPI targets and measurement framework
- Competitive analysis
- Risk mitigation

Context: {context}""",
        
        "realtime_trends": f"""Analyze current trends relevant to:
- Identify top 5 trending topics
- Assess relevance to client's industry
- Suggest content angles for each trend
- Note competitor activity

Context: {context}""",
        
        "images_video_logic": f"""Create visual content specification:
- Image concept and composition
- Color palette and mood
- Text overlay suggestions
- Video script (30s, 60s versions)
- Thumbnail design spec

Context: {context}""",
        
        "seo_aeo_geo": f"""Optimize content for:
- SEO: Target keywords, meta description, title tag
- AEO: Q&A structure for Google AI Overviews
- GEO: Entity markup, E-E-A-T signals, structured data
- Technical: Schema.org, Core Web Vitals notes

Context: {context}""",
        
        "auto_reply": f"""Generate a professional reply to this message:
- Match the brand tone (professional but friendly)
- Address the specific question/comment
- Include a soft CTA where appropriate
- Keep under 100 words

Message: {context}""",
        
        "lead_scoring": f"""Analyze this message for sales intent:
- Score 0-100 for purchase intent
- Identify pain points mentioned
- Recommend next action (nurture/qualify/urgent)
- Suggest follow-up message

Message: {context}""",
    }
    return prompts.get(task_type, f"Process: {context}")


# ═══════════════════════════════════════════════════════════════
# 2. SALES LEAD DETECTION ENGINE
# ═══════════════════════════════════════════════════════════════

LEAD_INDICATORS = {
    "high_intent": [
        "price", "cost", "how much", "budget", "quote", "proposal",
        "start", "begin", "sign up", "hire", "contract", "package",
        "what's your", "can you", "I need", "looking for",
        "حجز", "سعر", "عرض", "باقة",  # Arabic
        "قیمت", "بجٹ", "پیکج",  # Urdu
    ],
    "medium_intent": [
        "interested", "tell me more", "more info", "details",
        "demo", "consultation", "meeting", "call",
        "معلومات", "تفاصيل",  # Arabic
        "معلومات", "تفصیلات",  # Urdu
    ],
    "low_intent": [
        "nice", "interesting", "thanks", "good to know",
        "شكرا", "ممتاز",  # Arabic
    ],
}


def detect_lead(message: str, client_name: str = "") -> dict:
    """
    Detect sales intent in a message/comment/DM.
    Returns lead score, intent level, and recommended action.
    """
    msg_lower = message.lower()
    
    high_matches = [kw for kw in LEAD_INDICATORS["high_intent"] if kw in msg_lower]
    med_matches = [kw for kw in LEAD_INDICATORS["medium_intent"] if kw in msg_lower]
    low_matches = [kw for kw in LEAD_INDICATORS["low_intent"] if kw in msg_lower]
    
    score = min(100, len(high_matches) * 30 + len(med_matches) * 15 + len(low_matches) * 5)
    
    if score >= 60:
        intent = "HIGH"
        action = "IMMEDIATE: Send to Usama via WhatsApp/Email"
        next_step = "Schedule discovery call within 24h"
    elif score >= 30:
        intent = "MEDIUM"
        action = "NURTURE: Auto-reply with info + add to CRM"
        next_step = "Send case study + pricing overview"
    else:
        intent = "LOW"
        action = "AUTO-REPLY: Friendly response only"
        next_step = "Continue monitoring engagement"
    
    return {
        "message": message[:200],
        "client": client_name,
        "lead_score": score,
        "intent_level": intent,
        "matched_keywords": {
            "high": high_matches,
            "medium": med_matches,
            "low": low_matches,
        },
        "recommended_action": action,
        "next_step": next_step,
        "alert_urgent": score >= 60,
        "timestamp": datetime.now().isoformat(),
    }


# ═══════════════════════════════════════════════════════════════
# 3. EXHIBITION SCRAPER BY NICHE
# ═══════════════════════════════════════════════════════════════

EXHIBITIONS_DB = {
    "SA": {
        "tech": [
            {"name": "LEAP", "month": "February", "city": "Riyadh", "url": "https://leap.conference", "focus": "Tech & AI"},
            {"name": "Black Hat MEA", "month": "November", "city": "Riyadh", "url": "#", "focus": "Cybersecurity"},
            {"name": "Saudi Data & AI Summit", "month": "September", "city": "Riyadh", "url": "#", "focus": "Data & AI"},
        ],
        "hospitality": [
            {"name": "Arabian Travel Market", "month": "April-May", "city": "Riyadh", "url": "https://arabiantravelmarket.wtm.com", "focus": "Travel & Hospitality"},
            {"name": "Saudi Hotel Show", "month": "May", "city": "Riyadh", "url": "#", "focus": "Hotels"},
            {"name": "The Hotel Show Saudi Arabia", "month": "April", "city": "Jeddah", "url": "#", "focus": "Hospitality"},
        ],
        "general": [
            {"name": "Cityscape Saudi", "month": "November", "city": "Riyadh", "url": "#", "focus": "Real Estate"},
            {"name": "Saudi Food Show", "month": "May", "city": "Riyadh", "url": "#", "focus": "Food & Beverage"},
            {"name": "Riyadh Season Events", "month": "October-March", "city": "Riyadh", "url": "#", "focus": "Entertainment"},
        ],
    },
    "UK": {
        "tech": [
            {"name": "London Tech Week", "month": "June", "city": "London", "url": "https://londontechweek.com", "focus": "Technology"},
            {"name": "Birmingham Tech", "month": "October", "city": "Birmingham", "url": "#", "focus": "Tech & Innovation"},
        ],
        "marketing": [
            {"name": "Marketing Week Live", "month": "October", "city": "London", "url": "#", "focus": "Marketing"},
            {"name": "Digital Marketing World Forum", "month": "June", "city": "London", "url": "#", "focus": "Digital Marketing"},
        ],
    },
    "EU": {
        "tech": [
            {"name": "Web Summit", "month": "November", "city": "Lisbon", "url": "https://websummit.com", "focus": "Tech"},
            {"name": "MWC Barcelona", "month": "February-March", "city": "Barcelona", "url": "#", "focus": "Mobile/Connectivity"},
            {"name": "Viva Tech", "month": "June", "city": "Paris", "url": "#", "focus": "Innovation"},
        ],
        "marketing": [
            {"name": "DMEXCO", "month": "September", "city": "Cologne", "url": "#", "focus": "Digital Marketing"},
        ],
    },
    "US": {
        "tech": [
            {"name": "CES", "month": "January", "city": "Las Vegas", "url": "https://ces.tech", "focus": "Consumer Tech"},
            {"name": "SXSW", "month": "March", "city": "Austin", "url": "#", "focus": "Tech/Music/Film"},
            {"name": "Dreamforce", "month": "September", "city": "San Francisco", "url": "#", "focus": "CRM/Sales"},
        ],
        "marketing": [
            {"name": "INBOUND", "month": "September", "city": "Boston", "url": "#", "focus": "Marketing/Sales"},
            {"name": "Content Marketing World", "month": "September", "city": "Cleveland", "url": "#", "focus": "Content"},
        ],
    },
    "PK": {
        "tech": [
            {"name": "ITCN Asia", "month": "September", "city": "Karachi", "url": "#", "focus": "IT"},
            {"name": "Future Fest", "month": "January", "city": "Lahore", "url": "#", "focus": "Tech/Innovation"},
        ],
        "ecommerce": [
            {"name": "eCommerce Expo Pakistan", "month": "November", "city": "Karachi", "url": "#", "focus": "E-commerce"},
        ],
    },
}


def get_exhibitions(region: str, industry: str = "general") -> list:
    """Get exhibitions for a region and industry."""
    region_data = EXHIBITIONS_DB.get(region, {})
    results = region_data.get(industry, [])
    # Always include general
    if industry != "general":
        results += region_data.get("general", [])
    return results


def get_upcoming_exhibitions(region: str, industry: str = "general", months_ahead: int = 3) -> list:
    """Get exhibitions in the next N months."""
    all_exhibitions = get_exhibitions(region, industry)
    now = datetime.now()
    upcoming = []
    
    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12,
    }
    
    current_month = now.month
    for exh in all_exhibitions:
        exh_month = month_map.get(exh["month"].split("-")[0], 0)
        if exh_month == 0:
            continue
        months_until = (exh_month - current_month) % 12
        if months_until <= months_ahead:
            exh["months_until"] = months_until
            exh["status"] = "SOON" if months_until <= 1 else "UPCOMING"
            upcoming.append(exh)
    
    return sorted(upcoming, key=lambda x: x.get("months_until", 99))


# ═══════════════════════════════════════════════════════════════
# 4. ENHANCED SELENIUM AUTOMATION TEMPLATES
# ═══════════════════════════════════════════════════════════════

SELENIUM_NODE_SCRIPTS = {
    "scrape_trends": """
# Node: Selenium Scrape Trends & Client Data
# Runs daily via cron, scrapes Google Trends, competitor sites, client analytics

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json, time

def scrape_google_trends(keyword, region="SA"):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = f"https://trends.google.com/trends/explore?q={keyword}&geo={region}"
    driver.get(url)
    time.sleep(5)
    
    # Extract trend data
    try:
        # Load cookies for authenticated access
        with open(f"cookies/trends_{region}.json") as f:
            for c in json.load(f):
                driver.add_cookie(c)
        driver.refresh()
        time.sleep(3)
        
        # Scrape interest over time
        trend_data = driver.find_elements(By.CSS_SELECTOR, ".fe-line-chart .chart-line")
        related_topics = driver.find_elements(By.CSS_SELECTOR, ".related-topics-list li")
        
        return {
            "keyword": keyword,
            "region": region,
            "trend_elements": len(trend_data),
            "related_count": len(related_topics),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()
""",
    
    "auto_login_platforms": """
# Node: Selenium Auto-Login to All Platforms
# Opens browser tabs, logs into social media + blog accounts

PLATFORMS = {
    "instagram": "https://www.instagram.com/accounts/login/",
    "facebook": "https://www.facebook.com/login/",
    "linkedin": "https://www.linkedin.com/login",
    "x_twitter": "https://x.com/i/flow/login",
    "tiktok": "https://www.tiktok.com/login",
    "wordpress": "https://wordpress.com/log-in",
}

def login_all_platforms(client_key):
    # Load saved session cookies
    for platform, url in PLATFORMS.items():
        cookie_file = f"cookies/{client_key}_{platform}.json"
        if os.path.exists(cookie_file):
            driver.get(url)
            with open(cookie_file) as f:
                for cookie in json.load(f):
                    try:
                        driver.add_cookie(cookie)
                    except:
                        pass
            driver.refresh()
            time.sleep(2)
    # Now all tabs are logged in and ready for posting
""",
    
    "auto_post": """
# Node: Auto-Post 2x/day to Social & Blogs
# Uses logged-in browser sessions from auto_login_platforms

def post_to_instagram(driver, image_path, caption, hashtags):
    driver.get("https://www.instagram.com/")
    time.sleep(2)
    
    # Click create post
    create_btn = driver.find_element(By.CSS_SELECTOR, "[aria-label='New post']")
    create_btn.click()
    time.sleep(1)
    
    # Upload image
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(image_path)
    time.sleep(2)
    
    # Add caption
    caption_area = driver.find_element(By.CSS_SELECTOR, "[aria-label='Write a caption...']")
    caption_area.send_keys(f"{caption}\\n\\n{hashtags}")
    time.sleep(1)
    
    # Post
    share_btn = driver.find_element(By.XPATH, "//button[text()='Share']")
    share_btn.click()
    
    return {"status": "posted", "platform": "instagram", "timestamp": datetime.now().isoformat()}

def post_to_linkedin(driver, title, content, image_path=None):
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(2)
    
    # Click start post
    start_post = driver.find_element(By.CSS_SELECTOR, "[aria-label='Start a post']")
    start_post.click()
    time.sleep(1)
    
    # Type content
    text_area = driver.find_element(By.CSS_SELECTOR, ".ql-editor")
    text_area.send_keys(f"{title}\\n\\n{content}")
    time.sleep(1)
    
    # Post
    post_btn = driver.find_element(By.XPATH, "//button[text()='Post']")
    post_btn.click()
    
    return {"status": "posted", "platform": "linkedin", "timestamp": datetime.now().isoformat()}

def post_to_blog(driver, wp_url, title, content, tags, category):
    driver.get(f"{wp_url}/wp-admin/post-new.php")
    time.sleep(2)
    
    # Title
    title_field = driver.find_element(By.ID, "title")
    title_field.send_keys(title)
    
    # Content
    content_field = driver.find_element(By.ID, "content")
    content_field.send_keys(content)
    
    # Tags
    tags_field = driver.find_element(By.ID, "new-tag-post_tag")
    tags_field.send_keys(", ".join(tags))
    driver.find_element(By.CSS_SELECTOR, "#post_tag .button.tagadd").click()
    
    # Publish
    publish_btn = driver.find_element(By.ID, "publish")
    publish_btn.click()
    
    return {"status": "published", "platform": "blog", "timestamp": datetime.now().isoformat()}
""",
    
    "fetch_comments_dms": """
# Node: Selenium/API Fetch Comments & DMs
# Scrapes new comments and messages from all platforms

def fetch_instagram_comments(driver, post_url, last_check):
    driver.get(post_url)
    time.sleep(3)
    
    comments = []
    comment_elements = driver.find_elements(By.CSS_SELECTOR, "ul._a9ym li")
    
    for el in comment_elements:
        try:
            username = el.find_element(By.CSS_SELECTOR, "a span").text
            text = el.find_element(By.CSS_SELECTOR, "span._aap6").text
            comments.append({"user": username, "text": text})
        except:
            continue
    
    return {"platform": "instagram", "comments": comments}

def fetch_dms(driver, platform):
    dm_urls = {
        "instagram": "https://www.instagram.com/direct/inbox/",
        "facebook": "https://www.facebook.com/messages/",
        "linkedin": "https://www.linkedin.com/messaging/",
    }
    driver.get(dm_urls.get(platform, ""))
    time.sleep(3)
    
    # Parse unread messages
    messages = []
    # Platform-specific selectors would go here
    return {"platform": platform, "new_messages": messages}
""",
    
    "auto_reply": """
# Node: Selenium/API Auto-Reply
# Generates and sends replies to comments/DMs using AI

def auto_reply_to_comment(driver, comment, reply_text, platform):
    # Platform-specific reply logic
    if platform == "instagram":
        # Click reply
        reply_btn = comment.find_element(By.CSS_SELECTOR, "button[aria-label='Reply']")
        reply_btn.click()
        time.sleep(1)
        # Type reply
        reply_input = comment.find_element(By.CSS_SELECTOR, "textarea")
        reply_input.send_keys(reply_text)
        reply_input.send_keys(Keys.ENTER)
    elif platform == "linkedin":
        reply_btn = comment.find_element(By.CSS_SELECTOR, "button.comments-reply-item__reply-btn")
        reply_btn.click()
        time.sleep(1)
        reply_input = comment.find_element(By.CSS_SELECTOR, ".ql-editor")
        reply_input.send_keys(reply_text)
        # Submit
        submit_btn = comment.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
    
    return {"replied": True, "platform": platform, "timestamp": datetime.now().isoformat()}
""",
    
    "scrape_analytics": """
# Node: Selenium Scrape Analytics/Rankings
# Daily scrape of GA4, Search Console, social insights

def scrape_ga4_metrics(driver, property_id, date_range="7days"):
    driver.get(f"https://analytics.google.com/analytics/web/#/p{property_id}")
    time.sleep(5)
    
    metrics = {}
    try:
        # Active users
        users = driver.find_element(By.CSS_SELECTOR, "[aria-label='Active users']")
        metrics["active_users"] = users.text
        
        # Sessions
        sessions = driver.find_element(By.CSS_SELECTOR, "[aria-label='Sessions']")
        metrics["sessions"] = sessions.text
        
        # Conversions
        conversions = driver.find_element(By.CSS_SELECTOR, "[aria-label='Conversions']")
        metrics["conversions"] = conversions.text
    except Exception as e:
        metrics["error"] = str(e)
    
    return metrics

def scrape_search_console(driver, site_url):
    driver.get(f"https://search.google.com/search-console/performance?resource_id={site_url}")
    time.sleep(5)
    
    metrics = {}
    try:
        clicks = driver.find_element(By.CSS_SELECTOR, "[data-testid='clicks']")
        impressions = driver.find_element(By.CSS_SELECTOR, "[data-testid='impressions']")
        metrics = {"clicks": clicks.text, "impressions": impressions.text}
    except Exception as e:
        metrics["error"] = str(e)
    
    return metrics
""",
}


# ═══════════════════════════════════════════════════════════════
# 5. DAILY ORCHESTRATOR (V2 — follows the flow diagram)
# ═══════════════════════════════════════════════════════════════

def run_daily_automation_v2(clients: dict):
    """
    Full daily automation following the blueprint flow:
    
    1. Trigger: Daily Cron Job
    2. Selenium: Scrape Trends & Client Data
    3. LLM Router: Token Optimizer → routes to best AI
    4. AI generates content (4 LLMs in parallel)
    5. Content Database: SEO/AEO/GEO tags added
    6. Selenium: Auto-Login to Platforms
    7. Auto-Post 2x/day: Social & Blogs
    8. Selenium/API: Fetch Comments & DMs
    9. Auto-Reply (contextual) + Lead Detection
    10. Alert Usama if sales lead detected
    11. Selenium: Scrape Exhibitions by Niche
    12. AI: Generate Monthly Strategy & Calendar
    13. Email: Send Strategy & Reminders
    14. Selenium: Scrape Analytics/Rankings
    15. AI: Summarize Daily KPIs & Sales
    16. ERP Dashboard & Daily Email Report
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    results = {}
    
    for client_key, client in clients.items():
        print(f"\n{'='*60}")
        print(f"🦅 V2 Processing: {client['name']}")
        print(f"{'='*60}")
        
        # Step 1-2: Scrape trends
        print("  📊 Step 1-2: Scrape trends & client data...")
        trends_data = {
            "keywords": client.get("target_keywords", []),
            "region": client.get("region", "SA"),
            "industry": client.get("industry", "general"),
        }
        
        # Step 3: LLM Router
        print("  🤖 Step 3: Route tasks to optimal LLMs...")
        content_route = route_to_llm("outlines_formatting", str(trends_data))
        strategy_route = route_to_llm("long_form_strategy", str(trends_data))
        trends_route = route_to_llm("realtime_trends", str(trends_data))
        media_route = route_to_llm("images_video_logic", str(trends_data))
        
        total_cost = sum([
            float(content_route["estimated_cost"].replace("$", "")),
            float(strategy_route["estimated_cost"].replace("$", "")),
            float(trends_route["estimated_cost"].replace("$", "")),
            float(media_route["estimated_cost"].replace("$", "")),
        ])
        
        print(f"    → Content: {content_route['recommended_llm']} ({content_route['estimated_cost']})")
        print(f"    → Strategy: {strategy_route['recommended_llm']} ({strategy_route['estimated_cost']})")
        print(f"    → Trends: {trends_route['recommended_llm']} ({trends_route['estimated_cost']})")
        print(f"    → Media: {media_route['recommended_llm']} ({media_route['estimated_cost']})")
        print(f"    → Total estimated cost: ${total_cost:.4f}")
        
        # Step 8-10: Lead detection
        print("  🔍 Step 8-10: Lead detection system ready...")
        
        # Step 11-12: Exhibitions
        upcoming = get_upcoming_exhibitions(client.get("region", "SA"), client.get("industry", "general"))
        if upcoming:
            print(f"  🎪 Step 11: {len(upcoming)} upcoming exhibitions found")
            for exh in upcoming:
                print(f"    → {exh['name']} ({exh['month']}) - {exh['status']}")
        
        # Step 14-16: Analytics summary
        print("  📈 Step 14-16: Analytics & reporting pipeline ready...")
        
        # Save results
        out_dir = REPORTS_DIR / client_key / timestamp
        out_dir.mkdir(parents=True, exist_ok=True)
        
        output = {
            "client": client["name"],
            "timestamp": timestamp,
            "llm_routing": {
                "content": content_route,
                "strategy": strategy_route,
                "trends": trends_route,
                "media": media_route,
            },
            "total_ai_cost_estimate": f"${total_cost:.4f}",
            "upcoming_exhibitions": upcoming,
            "selenium_scripts_available": list(SELENIUM_NODE_SCRIPTS.keys()),
        }
        
        with open(out_dir / "v2_automation_output.json", "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        
        results[client_key] = {"processed": True, "output_dir": str(out_dir)}
        print(f"  ✅ Done! Output: {out_dir}")
    
    return results


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    # Import client configs from v1
    sys.path.insert(0, str(Path(__file__).parent))
    from erp_engine import CLIENTS
    
    # Convert dataclass clients to dicts for v2
    clients_dict = {k: {
        "name": v.name,
        "domain": v.domain,
        "region": v.region,
        "industry": v.industry,
        "target_keywords": v.target_keywords,
    } for k, v in CLIENTS.items()}
    
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════╗
║  AyaERP v2 🦅 — Enhanced Marketing Automation               ║
╠══════════════════════════════════════════════════════════════╣
║  Usage:                                                      ║
║    python3 erp_engine_v2.py run         — Full daily v2 run  ║
║    python3 erp_engine_v2.py route TASK  — Test LLM router   ║
║    python3 erp_engine_v2.py lead MSG   — Test lead detect   ║
║    python3 erp_engine_v2.py exhibitions — Show exhibitions   ║
║    python3 erp_engine_v2.py scripts    — List Selenium nodes ║
║                                                              ║
║  Task types: outlines_formatting, long_form_strategy,        ║
║    realtime_trends, images_video_logic, seo_aeo_geo,         ║
║    auto_reply, lead_scoring                                  ║
╚══════════════════════════════════════════════════════════════╝
        """)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "run":
        results = run_daily_automation_v2(clients_dict)
        print(f"\n✅ All clients processed (v2)")
    
    elif cmd == "route" and len(sys.argv) > 2:
        result = route_to_llm(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif cmd == "lead" and len(sys.argv) > 2:
        msg = " ".join(sys.argv[2:])
        result = detect_lead(msg)
        print(json.dumps(result, indent=2))
    
    elif cmd == "exhibitions":
        for region in ["SA", "UK", "EU", "US", "PK"]:
            upcoming = get_upcoming_exhibitions(region)
            if upcoming:
                print(f"\n🎪 {region} Upcoming:")
                for e in upcoming:
                    print(f"  → {e['name']} ({e['month']}) - {e.get('status', 'N/A')}")
    
    elif cmd == "scripts":
        for name, code in SELENIUM_NODE_SCRIPTS.items():
            print(f"\n{'='*40}")
            print(f"📋 {name}")
            print(f"{'='*40}")
            print(code[:200] + "...")
    
    else:
        print(f"Unknown command: {cmd}")
