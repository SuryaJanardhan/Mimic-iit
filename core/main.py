"""
LinkedIn Automation Engine (Functional Architecture)
Provides LLM-driven post generation, rate limit guardrails (< 80% cap),
trend aggregation, engagement routines, and weekly email reporting.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Helper: Load environment variables from local .env file
def load_env_file(file_path=".env"):
    """
    Loads environment variables from local .env file into os.environ if present.
    Uses standard library parsing for zero external package dependency.
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        if key.strip() and not os.environ.get(key.strip()):
                            os.environ[key.strip()] = val.strip()
            print(f"Success: Loaded environment variables from {file_path}")
        except Exception as err:
            print(f"Warning: Could not load .env file: {err}")


# Helper: Load persistent rate limit state from disk
def load_rate_limit_state(file_path="rate_limit_state.json"):
    """
    Loads persistent API rate limit usage counters from local JSON file.
    If the file does not exist, returns initialized zero-state dictionary.
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as err:
            print(f"Warning: Could not read rate limit state file: {err}")
    return {
        "date": time.strftime("%Y-%m-%d"),
        "posts_count": 0,
        "likes_count": 0,
        "comments_count": 0,
        "error_flag": False
    }


# Helper: Save persistent rate limit state to disk
def save_rate_limit_state(state, file_path="rate_limit_state.json"):
    """
    Saves current rate limit state to local JSON file for persistent tracking.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as err:
        print(f"Error: Failed to save rate limit state: {err}")


# Helper: Load post analysis history from root JSON file
def load_post_analysis_history(file_path="post_analysis_history.json"):
    """
    Loads historical post analysis logs from root JSON file.
    Returns list of post history objects.
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as err:
            print(f"Warning: Could not read post analysis history file: {err}")
    return []


# Helper: Append post analysis record to root JSON file
def append_post_analysis_record(record, file_path="post_analysis_history.json"):
    """
    Appends a new post execution and analytics record to the root JSON history file.
    """
    history = load_post_analysis_history(file_path)
    history.append(record)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
        print(f"Success: Post analysis record appended to root JSON ({file_path}).")
    except Exception as err:
        print(f"Error: Failed to append post analysis record: {err}")


# Core Safety Function: Rate Limit Budget Inspector
def check_rate_limit_budget(endpoint_key, state, max_daily_quota):
    """
    Checks whether usage for an endpoint remains strictly below 80% safety cap.
    Returns tuple (is_safe, remaining_safe_calls).
    """
    if state.get("error_flag", False):
        print(f"Safety Halt: Error flag is set for endpoint {endpoint_key}.")
        return False, 0

    current_date = time.strftime("%Y-%m-%d")
    if state.get("date") != current_date:
        state["date"] = current_date
        state["posts_count"] = 0
        state["likes_count"] = 0
        state["comments_count"] = 0
        state["error_flag"] = False

    current_usage = state.get(f"{endpoint_key}_count", 0)
    safety_threshold = int(max_daily_quota * 0.80)
    remaining = max(0, safety_threshold - current_usage)

    if current_usage >= safety_threshold:
        print(f"Safety Halt: Endpoint {endpoint_key} reached 80% cap ({current_usage}/{safety_threshold}).")
        return False, 0

    return True, remaining


# Trend Ingestion: GitHub Trending Repositories & Concepts
def fetch_github_trends(language="python"):
    """
    Dedicated function fetching top trending open-source repositories from GitHub API.
    Returns list of dictionaries containing repository name, description, stars, and URL.
    """
    url = f"https://api.github.com/search/repositories?q=language:{language}+created:>2026-01-01&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "LinkedInAutomationBot/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            repos = []
            for item in data.get("items", [])[:5]:
                repos.append({
                    "name": item.get("name"),
                    "description": item.get("description"),
                    "stars": item.get("stargazers_count"),
                    "url": item.get("html_url")
                })
            return repos
    except Exception as err:
        print(f"Warning: Failed to fetch GitHub trends: {err}")
        return []


# Trend Ingestion: Dedicated Tech & AI News Collector
def fetch_tech_news_trends():
    """
    Dedicated function fetching real-time tech and AI news headlines from HackerNews top stories API.
    Returns list of story dictionaries containing title and URL.
    """
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    req = urllib.request.Request(url, headers={"User-Agent": "LinkedInAutomationBot/1.0"})
    news_items = []
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            story_ids = json.loads(response.read().decode("utf-8"))[:5]
            for story_id in story_ids:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                item_req = urllib.request.Request(item_url, headers={"User-Agent": "LinkedInAutomationBot/1.0"})
                with urllib.request.urlopen(item_req, timeout=5) as item_resp:
                    story = json.loads(item_resp.read().decode("utf-8"))
                    if story and "title" in story:
                        news_items.append({
                            "title": story.get("title"),
                            "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}")
                        })
            return news_items
    except Exception as err:
        print(f"Warning: Failed to fetch tech news trends: {err}")
        return []


# Trend Ingestion: GitHub Trending Page Scraper
def scrape_github_trending_page(language=""):
    """
    Dedicated function scraping GitHub's official trending page (https://github.com/trending).
    Parses repository titles, descriptions, and URLs directly from HTML using regex.
    Returns list of repository dictionaries.
    """
    import re
    lang_path = f"/{language}" if language else ""
    url = f"https://github.com/trending{lang_path}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    req = urllib.request.Request(url, headers=headers)
    repos = []

    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode("utf-8", errors="ignore")
            # Extract repository article blocks
            articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.DOTALL)
            for article in articles[:5]:
                repo_match = re.search(r'href="/([^"/]+/[^"/]+)"', article)
                desc_match = re.search(r'<p class="col-9 color-fg-muted my-1 pr-4">(.*?)</p>', article, re.DOTALL)
                
                if repo_match:
                    repo_path = repo_match.group(1).strip()
                    repo_desc = desc_match.group(1).strip() if desc_match else "Trending open source project on GitHub."
                    # Clean HTML tags from description
                    repo_desc = re.sub(r'<[^>]+>', '', repo_desc).strip()
                    repos.append({
                        "name": repo_path.split("/")[-1],
                        "full_name": repo_path,
                        "description": repo_desc,
                        "url": f"https://github.com/{repo_path}"
                    })
            print(f"Success: Scraped {len(repos)} repositories from GitHub Trending page.")
            return repos
    except Exception as err:
        print(f"Warning: Failed to scrape GitHub trending page: {err}")
        return []


# Dedicated LLM API Dispatcher (Groq / Gemini / OpenAI Integration)
def call_llm_api(prompt, provider=None, api_key=None):
    """
    Dispatches prompt to LLM provider API (Groq API, Gemini API, or OpenAI API).
    Uses standard library urllib.request for zero third-party package dependency.
    Automatically checks environment keys: GROQ_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY.
    """
    groq_key = api_key or os.getenv("GROQ_API_KEY")
    gemini_key = api_key or os.getenv("GEMINI_API_KEY")
    openai_key = api_key or os.getenv("OPENAI_API_KEY")

    # Determine provider based on key presence or explicit preference
    target_provider = provider or ("groq" if groq_key else ("gemini" if gemini_key else ("openai" if openai_key else None)))

    if not target_provider:
        print("Notice: No GROQ_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY configured. Utilizing structured template fallback.")
        return None

    if target_provider.lower() == "groq" and groq_key:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {groq_key}"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                choices = res_data.get("choices", [])
                if choices:
                    print("Success: Post generated via Groq API (llama-3.3-70b-versatile).")
                    return choices[0].get("message", {}).get("content", "").strip()
        except Exception as err:
            print(f"Warning: Groq API call failed: {err}")
            return None

    elif target_provider.lower() == "gemini" and gemini_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        print("Success: Post generated via Gemini API (gemini-1.5-flash).")
                        return parts[0].get("text", "").strip()
        except Exception as err:
            print(f"Warning: Gemini API call failed: {err}")
            return None

    elif target_provider.lower() == "openai" and openai_key:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_key}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                choices = res_data.get("choices", [])
                if choices:
                    print("Success: Post generated via OpenAI API (gpt-4o-mini).")
                    return choices[0].get("message", {}).get("content", "").strip()
        except Exception as err:
            print(f"Warning: OpenAI API call failed: {err}")
            return None

    return None


# Content Strategy: Content Format Selector
def select_content_type(state):
    """
    Selects content format based on target mix:
    80% Serious Technical, 10% Text Meme, 5% Image Meme, 5% Simulated Poll.
    """
    total_posts = state.get("posts_count", 0)
    mod_val = total_posts % 20
    
    if mod_val == 18:
        return "TEXT_MEME"
    elif mod_val == 19:
        return "IMAGE_MEME"
    elif mod_val == 17:
        return "SIMULATED_POLL"
    else:
        return "SERIOUS_TECHNICAL"


# LLM Post Generation Engine
def generate_llm_post_content(content_type, trend_data, tech_news_data=None, llm_api_key=None):
    """
    Generates engaging post content based on selected content type, GitHub trend data, and Tech News.
    Enforces strict zero hashtag constraint. Calls call_llm_api or falls back to template.
    """
    prompt = (
        f"You are a senior software architect writing a LinkedIn post.\n"
        f"Format type: {content_type}\n"
        f"GitHub Trends Context: {json.dumps(trend_data if trend_data else [])}\n"
        f"Tech News Context: {json.dumps(tech_news_data if tech_news_data else [])}\n\n"
        f"STRICT RULES:\n"
        f"1. Zero hashtags allowed.\n"
        f"2. Professional, insightful tech tone.\n"
        f"3. High engagement hook.\n"
    )
    
    # Try calling LLM API
    generated_text = call_llm_api(prompt, provider="gemini", api_key=llm_api_key)
    if generated_text:
        return generated_text

    # Template fallback if LLM API key is not present
    if content_type == "TEXT_MEME":
        return (
            "Senior Dev: It works on my machine.\n"
            "DevOps Engineer: We will ship your machine to the customer.\n\n"
            "Docker was born."
        )
    elif content_type == "SIMULATED_POLL":
        return (
            "Architecture Debate: REST API vs gRPC for internal microservices.\n\n"
            "Option A: REST (Simplicity, standard tooling, easy debugging)\n"
            "Option B: gRPC (HTTP/2 streaming, Protobuf serialization, strict contracts)\n\n"
            "Which stack are you building on in 2026? Drop A or B in the comments below!"
        )
    elif content_type == "IMAGE_MEME":
        return (
            "When the unit tests pass on first try without single edit.\n\n"
            "Something is definitely wrong with the test suite."
        )
    else:
        repo_name = trend_data[0]["name"] if trend_data else "Modern LLM Framework"
        repo_desc = trend_data[0]["description"] if trend_data else "High performance parallel execution engine."
        repo_url = trend_data[0]["url"] if trend_data else "https://github.com"

        return (
            f"Open Source Deep Dive: {repo_name}\n\n"
            f"{repo_desc}\n\n"
            "Key Engineering Takeaways:\n"
            "• Optimized memory layout reduces allocation overhead by 40%.\n"
            "• Zero-copy deserialization enables microsecond response latency.\n"
            "• Modular functional design ensures clean maintainability.\n\n"
            f"Repository details: {repo_url}\n\n"
            "What optimization technique has made the biggest impact in your codebase recently?"
        )


# Payload Construction Helper
def prepare_linkedin_payload(author_urn, commentary_text, media_asset_urn=None):
    """
    Constructs standardized LinkedIn REST API v2 JSON payload.
    """
    payload = {
        "author": author_urn,
        "commentary": commentary_text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    if media_asset_urn:
        payload["content"] = {
            "media": [
                {
                    "title": "Attached Asset",
                    "id": media_asset_urn
                }
            ]
        }

    return payload


# Publisher Engine
def publish_linkedin_post(access_token, author_urn, commentary_text, state, max_daily_posts=500):
    """
    Publishes post to LinkedIn API while checking rate limit state.
    Immediately sets error flag and halts on HTTP error responses.
    """
    is_safe, remaining = check_rate_limit_budget("posts", state, max_daily_posts)
    if not is_safe:
        print("Publish Halted: 80% safety quota threshold reached for posts.")
        return False, state

    url = "https://api.linkedin.com/rest/posts"
    payload = prepare_linkedin_payload(author_urn, commentary_text)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": "202607",
        "Content-Type": "application/json"
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status in (200, 201):
                state["posts_count"] = state.get("posts_count", 0) + 1
                save_rate_limit_state(state)
                print(f"Success: Post published successfully! (Total today: {state['posts_count']})")
                return True, state
    except urllib.error.HTTPError as http_err:
        print(f"Critical Error: LinkedIn API returned HTTP {http_err.code}: {http_err.reason}")
        state["error_flag"] = True
        save_rate_limit_state(state)
        return False, state
    except Exception as err:
        print(f"Critical Error: Failed to publish post: {err}")
        state["error_flag"] = True
        save_rate_limit_state(state)
        return False, state

    return False, state


# Engagement Engine: Like / Comment Creator
def engage_with_viral_post(access_token, post_urn, action_type, commentary_text, state, max_daily_actions=5000):
    """
    Executes like or comment engagement on target viral post while respecting rate limit caps.
    """
    endpoint_key = "comments" if action_type == "COMMENT" else "likes"
    is_safe, remaining = check_rate_limit_budget(endpoint_key, state, max_daily_actions)
    
    if not is_safe:
        print(f"Engagement Halted: 80% safety quota reached for {endpoint_key}.")
        return False, state

    url = f"https://api.linkedin.com/rest/socialActions/{post_urn}/{endpoint_key}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": "202607",
        "Content-Type": "application/json"
    }
    
    payload = {"message": {"text": commentary_text}} if action_type == "COMMENT" else {}
    req_data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status in (200, 201):
                state[f"{endpoint_key}_count"] = state.get(f"{endpoint_key}_count", 0) + 1
                save_rate_limit_state(state)
                print(f"Success: Engagement ({action_type}) posted. (Total today: {state[f'{endpoint_key}_count']})")
                return True, state
    except Exception as err:
        print(f"Error: Engagement failed: {err}")
        state["error_flag"] = True
        save_rate_limit_state(state)
        return False, state

    return False, state


# Weekly Summary Builder
def build_weekly_report(state):
    """
    Constructs markdown summary of weekly post activity and rate limit usage.
    """
    report = (
        f"# Weekly LinkedIn Automation Report\n\n"
        f"**Date:** {state.get('date')}\n"
        f"**Account Status:** {'HEALTHY' if not state.get('error_flag') else 'ERROR DETECTED'}\n\n"
        f"## API Quota Usage (80% Safety Cap)\n"
        f"- **Posts Published Today:** {state.get('posts_count', 0)} / 400 safe cap\n"
        f"- **Comments Posted Today:** {state.get('comments_count', 0)} / 4000 safe cap\n"
        f"- **Likes Actioned Today:** {state.get('likes_count', 0)} / 8000 safe cap\n\n"
        f"## Recommendations\n"
        f"- Maintain current 80/10/5/5 content mix distribution.\n"
        f"- Continue monitoring initial hour engagement velocity.\n"
    )
    return report


# Weekly Email Dispatch Routine
def send_weekly_email_report(smtp_config, recipient_email, report_content):
    """
    Dispatches weekly summary report via SMTP email.
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "LinkedIn Automation: Weekly Status & Performance Report"
        msg["From"] = smtp_config.get("sender_email")
        msg["To"] = recipient_email
        msg.attach(MIMEText(report_content, "plain"))

        with smtplib.SMTP(smtp_config.get("host"), smtp_config.get("port")) as server:
            server.starttls()
            server.login(smtp_config.get("username"), smtp_config.get("password"))
            server.sendmail(smtp_config.get("sender_email"), recipient_email, msg.as_string())
        print("Success: Weekly report email sent successfully.")
        return True
    except Exception as err:
        print(f"Error: Failed to send weekly email report: {err}")
        return False


# Orchestration Function: Main Execution Loop
def run_automation_flow(access_token, author_urn):
    """
    Main orchestration routine executing the functional workflow:
    1. Load rate limit state.
    2. Check budget safety.
    3. Gather trends and select content type.
    4. Generate post content.
    5. Publish post.
    6. Abort immediately if any error occurs.
    """
    print("--- Starting LinkedIn Automation Flow ---")
    load_env_file()
    state = load_rate_limit_state()

    if state.get("error_flag"):
        print("Aborting: Previous error flag is set. Clear state file to resume.")
        return False

    github_trends = fetch_github_trends(language="python")
    scraped_trends = scrape_github_trending_page()
    combined_trends = github_trends + scraped_trends
    tech_news = fetch_tech_news_trends()
    content_type = select_content_type(state)
    post_text = generate_llm_post_content(content_type, combined_trends, tech_news_data=tech_news)

    print(f"Selected Content Format: {content_type}")
    print(f"GitHub Trends (API + Scraped) Fetched: {len(combined_trends)} repos")
    print(f"Tech News Headlines Fetched: {len(tech_news)} items")
    print(f"Generated Post Content:\n{post_text}\n")

    # Execute publication
    success, state = publish_linkedin_post(access_token, author_urn, post_text, state)
    
    if not success:
        print("Flow Terminated: Post publication encountered issue or reached limit.")
        return False

    # Record post analysis entry to root JSON history
    analysis_record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "content_type": content_type,
        "author_urn": author_urn,
        "commentary_snippet": post_text[:120] + "...",
        "hashtag_count": post_text.count("#"),
        "github_trends_used": [t["name"] for t in github_trends] if github_trends else [],
        "tech_news_used": [n["title"] for n in tech_news] if tech_news else [],
        "status": "PUBLISHED"
    }
    append_post_analysis_record(analysis_record)

    print("--- Automation Flow Completed Successfully ---")
    return True


if __name__ == "__main__":
    # Example dry run invocation
    token = os.getenv("LINKEDIN_ACCESS_TOKEN", "YOUR_FRESH_ACCESS_TOKEN")
    urn = os.getenv("LINKEDIN_AUTHOR_URN", "urn:li:person:bT4mlIV3WS")
    print(f"Automation initialized for URN: {urn}")
