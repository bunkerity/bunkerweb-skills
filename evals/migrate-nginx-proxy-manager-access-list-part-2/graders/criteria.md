---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Maps Force SSL to `REDIRECT_HTTP_TO_HTTPS=yes` and the certificate to `USE_CUSTOM_SSL=yes` with `CUSTOM_SSL_CERT` and `CUSTOM_SSL_KEY` naming the files, and says the scheduler must be able to read them (a mount into the scheduler).
8. Does not set `STRICT_TRANSPORT_SECURITY` to `max-age=63072000; preload`. It either leaves the default, or uses `max-age=63072000` or `max-age=63072000; includeSubDomains; preload`, and says BunkerWeb refuses `preload` without `includeSubDomains` and falls back to its default.
9. Says the detect run will not prove the access list: in detect, basic auth and the greylist let requests through and only log them (`detected deny access`), so the test belongs in `block` mode, for example on a spare hostname, or with the address rule as an `allow`/`deny` include file on a location.
