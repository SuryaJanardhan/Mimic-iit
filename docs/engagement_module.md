# Engagement Module (Likes & Comments)

## 1. Scope
With basic LinkedIn API access, direct feed discovery is scoped. This module defines the functional strategy for interacting with high-profile industry leaders and viral tech posts using basic permissions.

## 2. Core Functions

### A. Target Post Identification
- Monitor specified author URNs or tracked topics.
- Filter for posts with high engagement potential (recent, relevant tech topics).

### B. Automated Insightful Commenting
- LLM generates context-aware comments for target posts.
- Comments must add technical value (asking a relevant question or sharing a technical insight).
- Enforces zero hashtag rule in comments as well.

### C. Rate-Limited Liking
- Controlled liking routine respecting the daily < 80% quota cap.

## 3. Workflow Sequence
1. Fetch target post activity.
2. Verify rate limit safety budget.
3. Pass post commentary to LLM for context synthesis.
4. Execute engagement request via LinkedIn REST API.
5. Log activity timestamp and increment daily engagement count.
