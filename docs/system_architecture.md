# System Architecture Analysis

## 1. Overview
This document outlines the architecture for an automated LinkedIn content engine. The system leverages trending GitHub repositories, AI developments, and historical post analytics to generate high-quality LinkedIn posts. The engine operates purely using functional programming in Python and strictly respects LinkedIn API rate limits.

## 2. Core Architectural Pillars

### A. Functional Programming Paradigm
- Implementation uses pure functions without class state side effects.
- Input data flows through deterministic transformation pipelines.
- Data structures are kept as immutable dictionaries or standard primitives.

### B. Safety & Rate Limiting Guardrails
- Implements strict threshold monitoring (< 80% of daily API rate limits).
- Tracks daily request quota per endpoint (Posts, Comments, Engagements).
- Immediate flow halt upon receiving rate limit warning headers or unexpected status codes (429, 403).

### C. Content Pipeline
1. **Trend Ingestion**: Fetches top trending GitHub repositories and AI news.
2. **Performance History**: Reads historical post performance data.
3. **LLM Generation**: Crafts engaging, zero-hashtag posts with professional insights.
4. **Media Handler**: Selects and attaches non-generic relevant images.
5. **Publisher**: Formats payload for LinkedIn API (`https://api.linkedin.com/rest/posts`) and executes dispatch.

---

## 3. Data Flow Diagram

```
[GitHub Trends API / AI News] ----> [Trend Collector] 
                                          |
[Historical Analytics] -------------> [Context Builder]
                                          |
                                    [LLM Generator]
                                          |
                                    [Post Validator] (No Hashtags, <80% Rate Limit)
                                          |
                                    [LinkedIn API Publisher]
```

## 4. LinkedIn API Integration Payload

The core publishing endpoint uses LinkedIn RestLi protocol `2.0.0` and API version `202607`.

```json
{
  "author": "urn:li:person:bT4mlIV3WS",
  "commentary": "Generated post content here",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}
```

## 5. Directory Layout

```
/
├── docs/
│   ├── system_architecture.md
│   ├── content_strategy.md
│   ├── rate_limit_safety.md
│   └── engagement_module.md
├── task.md
├── main.py
└── README.md
```
