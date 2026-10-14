---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Uses the settings `USE_REVERSE_PROXY=yes`, `SERVER_NAME` set to `app.example.com` and `REVERSE_PROXY_HOST` set to `http://app:3000` on the `/` entry. A `<server_name>_` prefix on a setting name is fine. No `REVERSE_PROXY_HOST` value is a fixed path such as `http://app:3000/v2/`; `/v2/` followed by the capture and query variables is expected on the `/api/` entry.
2. Sets `MAX_CLIENT_SIZE` to `50m` (a `<server_name>_` prefix is fine).
3. Sets HSTS with the `STRICT_TRANSPORT_SECURITY` setting and the value `max-age=31536000; includeSubDomains`, and the frame header with `X_FRAME_OPTIONS` set to `DENY`. It does not leave a raw `add_header` for either, and does not add them as `CUSTOM_HEADER`.
