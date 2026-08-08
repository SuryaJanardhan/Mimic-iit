# Rate Limit & API Safety Guardrails

## 1. Safety Mandate
LinkedIn strictly monitors API usage. Exceeding daily quota limits can result in API key revocation or account restriction. To prevent this, the automation engine enforces an absolute safety threshold of **80% of maximum daily rate limits**.

## 2. Threshold Calculation Matrix

| Endpoint / Action | LinkedIn Daily Limit | 80% Safety Cap | Recommended Daily Limit |
|---|---|---|---|
| Post Creation (`/rest/posts`) | 100 requests / day | 80 requests / day | 2 to 5 posts / day |
| Engagement (Likes / Comments) | 250 requests / day | 200 requests / day | 15 to 30 actions / day |

## 3. Dedicated Rate Limit Tracker Function (`check_rate_limit_budget`)

The function maintains persistent local JSON state tracking remaining calls:

```python
# Functional rate limiting check
def check_rate_limit_budget(endpoint_key, current_usage, max_daily_quota):
    """
    Evaluates whether an API call is safe to proceed.
    Halts execution if usage reaches 80% threshold.
    """
    safety_threshold = max_daily_quota * 0.80
    remaining_safe_calls = max(0, int(safety_threshold - current_usage))
    
    if current_usage >= safety_threshold:
        return False, 0
    return True, remaining_safe_calls
```

## 4. Error Handling Protocol
- **429 Too Many Requests**: Immediate script abort. No retry loop.
- **403 Forbidden**: Immediate script abort. Alert log recorded.
- **Non-200 Responses**: Halt execution flow immediately to prevent snowballing failures.
