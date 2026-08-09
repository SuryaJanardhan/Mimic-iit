# Mimic-IIT

> Autonomous, zero-dependency LinkedIn growth and engagement engine built for software engineers, architects, and technical creators.

Mimic-IIT automates tech-focused LinkedIn posting and targeted engagement. It pulls real-time trends from GitHub repositories and HackerNews headlines, generates high-quality posts using Groq LLM (llama-3.3-70b-versatile), and interacts with target tech creators while strictly respecting rate limit guardrails.

---

## Highlights

- **Zero Heavy Dependencies**: Built purely with Python standard library (`urllib.request`, `json`, `re`, `smtplib`). No heavy third-party SDK bloat.
- **Groq LLM Engine with Failover**: Dispatches generation prompts to Groq API with automatic fallback support (`GROQ_API_KEY` to `GROQ_API_KEY_2`).
- **Humanized Technical Content Strategy**:
  - **80% Deep Technical**: System design, distributed architecture, and open-source GitHub trends.
  - **10% Witty Text Memes**: Short engineering humor snippets.
  - **5% Image Memes & 5% Simulated Polls**: High-engagement choice debates.
- **Strict Content Quality Rules**: Enforces zero hashtags and zero emojis for clean, professional post bodies.
- **Hybrid Post Discovery**: Discovers target posts from a curated list of creator profiles (`target_creators.json`) or via live web search fallback.
- **Strict Rate Limit Guardrails**: Enforces an 80% quota safety threshold and caps outbound feed interactions to a maximum of 2 likes and 2 comments per day.
- **Weekly Email Health Reports**: Dispatches automated markdown summary emails covering account health and quota metrics via SMTP.

---

## Repository Structure

```
Mimic-iit/
├── core/
│   └── main.py                     # Master functional automation script
├── docs/
│   ├── content_capability_plan.md  # Detailed content format mix strategy
│   ├── content_strategy.md         # Voice and post structure guidelines
│   ├── engagement_module.md        # Like and comment execution pipeline
│   ├── function_documentation.md   # Complete reference for all Python routines
│   ├── github_actions_setup.md     # GitHub Actions workflow secret configuration
│   ├── growth_strategy_engagement_models.md  # Growth metrics and engagement models
│   ├── rate_limit_safety.md        # API quota limits and safety thresholds
│   ├── system_architecture.md      # Core architectural diagram and flow
│   └── weekly_email_reporting.md   # SMTP email dispatch documentation
├── .env.example                    # Environment variable configuration template
├── target_creators.json            # Target creator profiles and page URLs
├── rate_limit_state.json           # Daily API quota usage counters
├── post_analysis_history.json      # Historical log of published posts
├── task.md                         # Task specification notes
└── README.md                       # Project overview and setup instructions
```

---

## Getting Started

### 1. Prerequisites

- Python 3.9+ installed on your system.
- Groq API Key (get one at [groq.com](https://groq.com)).
- LinkedIn API Access Token with `w_member_social` or `w_organization_social` scope.

### 2. Environment Configuration

Copy `.env.example` to `.env` and fill in your API credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# LinkedIn API Credentials
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token_here
LINKEDIN_AUTHOR_URN=urn:li:person:your_person_urn_id

# Groq LLM API Keys (Primary & Fallback)
GROQ_API_KEY=gsk_primary_key_here
GROQ_API_KEY_2=gsk_fallback_key_here

# Weekly Email SMTP Settings (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
RECIPIENT_EMAIL=report_recipient@example.com

# Target Outbound Engagement Post URLs (Optional)
TARGET_POST_URLS=https://www.linkedin.com/posts/example_activity-1234567890
```

### 3. Target Creators List (Optional)

Configure profiles or pages you want to track in `target_creators.json`:

```json
[
  {
    "name": "Satya Nadella",
    "url": "https://www.linkedin.com/in/satyanadella",
    "topic": "Cloud Infrastructure & Enterprise AI"
  },
  {
    "name": "OpenAI",
    "url": "https://www.linkedin.com/company/openai",
    "topic": "Frontier AI Models & Machine Learning"
  }
]
```

---

## Execution

Run the main automation cycle directly from the root workspace directory:

```bash
python3 core/main.py
```

### What Happens During Execution

1. **Environment & State Check**: Loads environment keys and verifies daily rate limit quotas in `rate_limit_state.json`.
2. **Trend Aggregation**: Queries GitHub Search API, scrapes trending repositories, and pulls HackerNews tech headlines.
3. **Format Selection**: Chooses the post type according to the content mix matrix.
4. **LLM Content Generation**: Invokes Groq API (`llama-3.3-70b-versatile`) to generate post commentary, enforcing zero-hashtag and zero-emoji constraints.
5. **Post Publication**: Formats LinkedIn REST API payload and dispatches post to `https://api.linkedin.com/rest/posts`.
6. **Target Engagement**: Discovers posts from `target_creators.json` or live web search fallback, generating technical comments and liking posts (capped at 2 likes and 2 comments per day).
7. **Analytics Logging**: Appends post analytics to `post_analysis_history.json`.

---

## Documentation Index

For detailed architectural and strategy breakdowns, refer to the documentation inside the [`/docs`](file:///home/surya/Desktop/Mimic-iit/docs) folder:

- [Function Documentation](file:///home/surya/Desktop/Mimic-iit/docs/function_documentation.md): API details for all routines in `core/main.py`.
- [Rate Limit Safety](file:///home/surya/Desktop/Mimic-iit/docs/rate_limit_safety.md): Quota caps and 80% safety logic.
- [Engagement Module](file:///home/surya/Desktop/Mimic-iit/docs/engagement_module.md): Target post URL parsing and discovery mechanisms.
- [Content Capability Plan](file:///home/surya/Desktop/Mimic-iit/docs/content_capability_plan.md): Content mix breakdown and schedule.
- [GitHub Actions Setup](file:///home/surya/Desktop/Mimic-iit/docs/github_actions_setup.md): Guide for automated CRON workflow dispatches.
