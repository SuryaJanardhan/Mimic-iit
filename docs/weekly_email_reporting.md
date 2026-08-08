# Automated Weekly Email Reporting System

## 1. Overview
The automation script includes a dedicated reporting routine that generates and emails a weekly performance summary. This report tracks post creation statistics, rate limit consumption, account health, and recommendations for the upcoming week.

## 2. Report Contents & Key Metrics

### A. Account & API Health Status
- Total API calls executed vs daily safety budget (< 80% threshold).
- Error counts (HTTP 429, 403, or connection timeouts).
- Current API token expiration notice and status.

### B. Published Content Performance
- Total posts published in the past 7 days.
- Content category breakdown (Technical Breakdown vs Text Meme vs Image Meme).
- Top performing post by engagement (reactions and comments).

### C. Strategic Recommendations
- LLM generated suggestions based on performance analytics.
- Optimal posting times identified from historical data.

## 3. Email Dispatch Architecture

The reporting module uses Python standard `smtplib` and `email.mime` modules for zero-dependency email delivery (configurable with SMTP or SendGrid/Resend API).

```python
# Functional email dispatch helper
def send_weekly_email_report(smtp_config, recipient_email, report_markdown):
    """
    Formats and dispatches the weekly HTML/Text report to the specified email address.
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "LinkedIn Automation: Weekly Performance & Health Report"
    msg['From'] = smtp_config['sender_email']
    msg['To'] = recipient_email

    part = MIMEText(report_markdown, 'plain')
    msg.attach(part)

    with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
        server.starttls()
        server.login(smtp_config['username'], smtp_config['password'])
        server.sendmail(smtp_config['sender_email'], recipient_email, msg.as_string())
```

## 4. Automated Schedule
- The weekly report routine runs automatically every Sunday at 23:00 UTC.
- Can also be triggered on-demand via `--send-report` command line flag.
