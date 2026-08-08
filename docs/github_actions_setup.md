# GitHub Actions CI/CD Automation Pipeline

## 1. Executive Summary
This document explains the automated GitHub Actions workflow configured in **[linkedin_automation.yml](file:///home/surya/Desktop/Mimic-iit/.github/workflows/linkedin_automation.yml)**. The workflow executes once per day to optimize post distribution timing and ensure strict rate limit safety.

---

## 2. Schedule & Rate Limit Rationale

### Execution Cron: `0 14 * * *` (14:00 UTC / Daily)
- **Posting Cadence**: 1 post per day (7 posts per week).
- **Time Selection**: 14:00 UTC corresponds to 9:00 AM EST and 7:30 PM IST, capturing peak professional reading windows across US and global tech hubs.
- **Quota Safety**: Running once per day utilizes less than **1% of daily API quotas**, keeping the account far below the 80% safety cap.

---

## 3. Required GitHub Repository Secrets

To enable automated posting and weekly email reports, configure the following secrets in GitHub (**Settings > Secrets and variables > Actions**):

| Secret Name | Purpose | Example Value |
|---|---|---|
| `LINKEDIN_ACCESS_TOKEN` | Bearer token for LinkedIn REST API v2 | `AQV...` |
| `LINKEDIN_AUTHOR_URN` | URN identifier for your profile | `urn:li:person:bT4mlIV3WS` |
| `SMTP_HOST` | Hostname for weekly email delivery | `smtp.gmail.com` |
| `SMTP_PORT` | Port number for TLS SMTP | `587` |
| `SMTP_USERNAME` | SMTP account email address | `user@example.com` |
| `SMTP_PASSWORD` | App-specific password or API key | `xxxx xxxx xxxx xxxx` |
| `RECIPIENT_EMAIL` | Target email receiving weekly report | `owner@example.com` |

---

## 4. State Persistence Mechanism
After every execution run, the workflow auto-commits the updated `rate_limit_state.json` file back to the `main` branch using `[skip ci]`. This guarantees that daily post counts and error flags persist across workflow runs without causing infinite CI loops.

---

## 5. Manual Execution (Workflow Dispatch)
You can trigger an immediate post run at any time:
1. Go to your repository on GitHub.
2. Click **Actions > LinkedIn Daily Automation & Weekly Report**.
3. Click **Run workflow > Run workflow**.
