# Functional Code Documentation

## 1. Overview
This document provides a detailed function-by-function explanation of the single-script automation engine located at **[linkedin_automation.py](file:///home/surya/Desktop/Mimic-iit/core/linkedin_automation.py)**. The codebase is implemented strictly using pure functional programming in Python.

---

## 2. Core Rate Limit & State Functions

### `load_rate_limit_state(file_path="rate_limit_state.json")`
- **Purpose**: Reads persistent usage counters (posts, comments, likes) and error flags from local JSON storage.
- **Parameters**: `file_path` (str) - Path to persistent state file.
- **Returns**: Dictionary containing date, usage counts, and safety error flag.

### `save_rate_limit_state(state, file_path="rate_limit_state.json")`
- **Purpose**: Writes current usage state and safety flags to local JSON storage for persistent multi-run tracking.
- **Parameters**: `state` (dict), `file_path` (str).
- **Returns**: None.

### `load_post_analysis_history(file_path="post_analysis_history.json")`
- **Purpose**: Reads historical post analysis entries from the root JSON file.
- **Parameters**: `file_path` (str) - Path to root analysis JSON file.
- **Returns**: List of post history record dictionaries.

### `append_post_analysis_record(record, file_path="post_analysis_history.json")`
- **Purpose**: Appends a newly published post's analytics entry (timestamp, content type, snippet, trends used, hashtag count) into the root JSON file.
- **Parameters**: `record` (dict), `file_path` (str).
- **Returns**: None.

### `check_rate_limit_budget(endpoint_key, state, max_daily_quota)`
- **Purpose**: Enforces the **< 80% daily quota threshold** rule. Halts execution if usage reaches 80% of daily max quota or if an error flag is set.
- **Parameters**: 
  - `endpoint_key` (str): Target endpoint ("posts", "comments", or "likes").
  - `state` (dict): Current rate limit state dictionary.
  - `max_daily_quota` (int): Maximum daily allowance per official API docs.
- **Returns**: Tuple `(is_safe: bool, remaining_safe_calls: int)`.

---

## 3. Content Strategy & Trend Ingestion Functions

### `fetch_github_trends(language="python")`
- **Purpose**: Dedicated function querying GitHub REST API to retrieve top trending open-source repositories.
- **Parameters**: `language` (str) - Target programming language filter.
- **Returns**: List of repository dictionaries containing name, description, stars, and URL.

### `fetch_tech_news_trends()`
- **Purpose**: Dedicated function querying HackerNews top stories API to fetch real-time AI and engineering news headlines.
- **Parameters**: None.
- **Returns**: List of tech news dictionaries containing title and URL.

### `call_llm_api(prompt, provider="groq", api_key=None)`
- **Purpose**: Dedicated LLM provider dispatcher supporting Groq API (`llama-3.3-70b-versatile`), Gemini API (`gemini-1.5-flash`), or OpenAI API via zero-dependency `urllib.request`. Defaults to Groq API. Falls back to local structured template if API key is not set.
- **Parameters**: `prompt` (str), `provider` (str, default `"groq"`), `api_key` (optional str).
- **Returns**: String response from LLM or None if unavailable.

### `select_content_type(state)`
- **Purpose**: Selects the post format according to the target strategy mix (80% Serious Technical, 10% Text Meme, 5% Image Meme, 5% Simulated Poll).
- **Parameters**: `state` (dict) - Usage state used to calculate modulo distribution.
- **Returns**: String key representing content format ("SERIOUS_TECHNICAL", "TEXT_MEME", "IMAGE_MEME", "SIMULATED_POLL").

### `generate_llm_post_content(content_type, trend_data, tech_news_data=None, llm_api_key=None)`
- **Purpose**: Constructs LLM prompt combining GitHub trends, Tech News, and content format rules, then calls `call_llm_api` or structured template fallback. Enforces zero hashtags.
- **Parameters**: `content_type` (str), `trend_data` (list), `tech_news_data` (list), `llm_api_key` (optional str).
- **Returns**: String containing formatted LinkedIn post text.

---

## 4. LinkedIn API Integration & Publishing Functions

### `prepare_linkedin_payload(author_urn, commentary_text, media_asset_urn=None)`
- **Purpose**: Formats JSON payload required by LinkedIn REST API version `202607` and RestLi protocol `2.0.0`.
- **Parameters**: `author_urn` (str), `commentary_text` (str), `media_asset_urn` (optional str).
- **Returns**: Dictionary representing post payload.

### `publish_linkedin_post(access_token, author_urn, commentary_text, state, max_daily_posts=500)`
- **Purpose**: Dispatches POST request to `https://api.linkedin.com/rest/posts`. Immediately sets error flag and halts on any HTTP failure (429, 403, 500).
- **Parameters**: `access_token` (str), `author_urn` (str), `commentary_text` (str), `state` (dict), `max_daily_posts` (int).
- **Returns**: Tuple `(success: bool, updated_state: dict, post_link: optional str)`.

### `engage_with_viral_post(access_token, post_urn, action_type, commentary_text, state, max_daily_actions=5000)`
- **Purpose**: Likes or posts value-add technical comments on target viral posts while tracking engagement quotas.
- **Parameters**: `access_token` (str), `post_urn` (str), `action_type` (str), `commentary_text` (str), `state` (dict), `max_daily_actions` (int).
- **Returns**: Tuple `(success: bool, updated_state: dict)`.

### `extract_urn_from_linkedin_url(url_or_urn)`
- **Purpose**: Parses full LinkedIn post URLs (e.g. `https://www.linkedin.com/posts/user_activity-7123456789012345678-abc`) into valid API URN strings (`urn:li:activity:7123456789012345678`).
- **Parameters**: `url_or_urn` (str).
- **Returns**: Formatted URN string or None if unparseable.

### `get_target_engagement_posts()`
- **Purpose**: Reads target engagement URLs from `TARGET_POST_URLS` in `.env` or local `target_posts.json`.
- **Parameters**: None.
- **Returns**: List of target post dictionary objects.

### `process_target_engagements(access_token, state, llm_api_key=None)`
- **Purpose**: Pipeline function that reads target URLs, extracts URNs, uses Groq LLM to generate value-add comments, and dispatches likes and comments.
- **Parameters**: `access_token` (str), `state` (dict), `llm_api_key` (optional str).
- **Returns**: Updated state dictionary.

---

## 5. Reporting & Orchestration Functions

### `build_weekly_report(state)`
- **Purpose**: Generates plain-text/markdown summary report of daily/weekly activity, account health status, and quota usage.
- **Parameters**: `state` (dict).
- **Returns**: Formatted markdown string.

### `send_weekly_email_report(smtp_config, recipient_email, report_content)`
- **Purpose**: Sends the generated report to specified recipient via SMTP email.
- **Parameters**: `smtp_config` (dict), `recipient_email` (str), `report_content` (str).
- **Returns**: Boolean status indicating email delivery success.

### `send_post_links_email(smtp_config, recipient_email, post_links)`
- **Purpose**: Sends a success email after a completed run with published LinkedIn post links.
- **Parameters**: `smtp_config` (dict), `recipient_email` (str), `post_links` (list[str]).
- **Returns**: Boolean status indicating email delivery success.

### `run_automation_flow(access_token, author_urn)`
- **Purpose**: Master orchestrator function running the end-to-end pipeline in sequential order.
- **Parameters**: `access_token` (str), `author_urn` (str).
- **Returns**: Tuple `(success: bool, published_post_links: list[str])`.
