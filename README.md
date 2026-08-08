# Mimic-iit

Functional Python automation project for generating and publishing LinkedIn content using GitHub/tech trends, LLM-assisted drafting, and strict API safety guardrails.

## What this repository contains

- `core/main.py`: single-script functional automation engine.
- `.github/workflows/linkedin_automation.yml`: scheduled GitHub Actions workflow.
- `docs/`: architecture, strategy, safety, engagement, and reporting documentation.
- `.env.example`: required local environment variable template.
- `post_analysis_history.json`: persisted post analysis history.

## Core capabilities implemented

- Rate-limit safety enforcement with a hard **80% daily cap**.
- Persistent state tracking via `rate_limit_state.json`.
- Trend ingestion from:
  - GitHub Search API
  - GitHub Trending page scraping
  - Hacker News top stories API
- LLM provider dispatch support:
  - Groq
  - Gemini
  - OpenAI
- LinkedIn post payload generation and publish request flow.
- Weekly text report generation + SMTP email dispatch helper.

## Repository structure

```text
Mimic-iit/
├── core/
│   └── main.py
├── docs/
│   ├── content_capability_plan.md
│   ├── content_strategy.md
│   ├── engagement_module.md
│   ├── function_documentation.md
│   ├── github_actions_setup.md
│   ├── growth_strategy_engagement_models.md
│   ├── rate_limit_safety.md
│   ├── system_architecture.md
│   └── weekly_email_reporting.md
├── .github/workflows/
│   └── linkedin_automation.yml
├── .env.example
├── post_analysis_history.json
└── README.md
```

## Setup

1. Copy `.env.example` to `.env`.
2. Fill required credentials:
   - `LINKEDIN_ACCESS_TOKEN`
   - `LINKEDIN_AUTHOR_URN`
   - at least one of: `GROQ_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`
   - SMTP fields for weekly report delivery (`SMTP_*`, `RECIPIENT_EMAIL`)

## Run locally

```bash
python core/main.py
```

## GitHub Actions automation

Workflow file: `.github/workflows/linkedin_automation.yml`

- Triggered daily at `0 14 * * *` and via manual workflow dispatch.
- Injects all required secrets from repository Actions secrets.
- Executes `python core/main.py`.
- Commits updated `rate_limit_state.json` and `post_analysis_history.json` when changed.

## Documentation index

- Architecture: `docs/system_architecture.md`
- Function reference: `docs/function_documentation.md`
- Content strategy: `docs/content_strategy.md`
- Rate-limit guardrails: `docs/rate_limit_safety.md`
- Engagement strategy: `docs/engagement_module.md`
- Weekly reporting: `docs/weekly_email_reporting.md`
