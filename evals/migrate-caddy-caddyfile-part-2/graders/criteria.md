---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Sets HSTS with the `STRICT_TRANSPORT_SECURITY` setting and the value `max-age=31536000; includeSubDomains`, not with a raw header, and uses `USE_GZIP=yes` for `encode gzip`.
8. Says that BunkerWeb does not obtain a certificate by itself and sets `AUTO_LETS_ENCRYPT=yes` with `EMAIL_LETS_ENCRYPT`, or reuses Caddy's stored certificate files through `USE_CUSTOM_SSL=yes`, `CUSTOM_SSL_CERT` and `CUSTOM_SSL_KEY`. If it reuses the files, it says they must be readable by the scheduler or mounted into it.
9. Says BunkerWeb turns on protections the Caddyfile did not have and names `USE_LIMIT_REQ` with its `2r/s` default, or ModSecurity with the OWASP CRS, as something to review in the detect run.
10. Recommends a parallel run with `SECURITY_MODE=detect` on spare ports before cutover and writes down a rollback that restores Caddy on ports 80 and 443.
