# Engagement Module (Likes & Comments)

## 1. Scope
Because basic LinkedIn API access does not grant full member feed search permissions, target post URLs or URNs are supplied via configured queues or environment variables. This module converts those post URLs into LinkedIn API URNs and executes automated, value-add engagements (likes and comments).

## 2. Post URL & URN Acquisition Methods

Target post URLs/URNs can be supplied via three mechanisms:

1. **Environment Variable (`TARGET_POST_URLS` in `.env`)**:
   - Provide a comma-separated list of target LinkedIn post URLs in `.env`.
   - Example: `TARGET_POST_URLS=https://www.linkedin.com/posts/username_activity-7123456789012345678-abcd,https://www.linkedin.com/feed/update/urn:li:activity:7987654321098765432`

2. **Target Post Queue (`target_posts.json`)**:
   - Store target posts as a JSON array of objects specifying URL and topic context:
     ```json
     [
       {
         "url": "https://www.linkedin.com/posts/techlead_activity-7123456789012345678-xyz",
         "topic": "Distributed DB Systems & Postgres"
       }
     ]
     ```

3. **Automatic URL-to-URN Parser (`extract_urn_from_linkedin_url`)**:
   - Regex-based parser converts raw LinkedIn post URLs into REST API URNs:
     - `https://www.linkedin.com/posts/user_activity-7123456789012345678-abc` -> `urn:li:activity:7123456789012345678`
     - `https://www.linkedin.com/feed/update/urn:li:activity:7123456789012345678/` -> `urn:li:activity:7123456789012345678`
     - `https://www.linkedin.com/feed/update/urn:li:share:7123456789012345678/` -> `urn:li:share:7123456789012345678`

## 3. Core Functions & Engagement Flow

### A. Automated Insightful Commenting
- Groq LLM generates context-aware technical comments based on post topic.
- Enforces strict constraints: zero hashtags, zero emojis, playful insightful engineering tone.

### B. Rate-Limited Liking
- Sends POST request to `https://api.linkedin.com/rest/socialActions/{post_urn}/likes`.
- Enforces daily rate limit budget checks (< 80% daily quota).

### C. Execution Pipeline (`process_target_engagements`)
1. Reads target posts from `TARGET_POST_URLS` or `target_posts.json`.
2. Extracts API URN for each target URL.
3. Generates value-add comment via Groq LLM.
4. Executes like and comment requests via `engage_with_viral_post`.
5. Updates rate limit state and logs engagement counters.

