---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Sets `ALLOWED_METHODS` to a value that includes `PUT` and `DELETE`, for example `GET|POST|HEAD|OPTIONS|PUT|DELETE`, and says the default list would answer `405` to the mobile app.
2. Warns that the BunkerWeb request rate limit (`LIMIT_REQ_RATE`) can be too low for a wp-admin page load, that the `429` answers count as bad behavior and ban the client IP for 24 hours, and says to raise the rate or switch the limit off.
3. Names the CRS plugin `wordpress-rule-exclusions` (setting `MODSECURITY_CRS_PLUGINS`), or says to start from the WordPress template that sets it.
