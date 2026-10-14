---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Maps the `/login` stick-table rule to a numbered pair `LIMIT_REQ_URL_<n>` (a regex such as `^/login$`, or `/login`) and `LIMIT_REQ_RATE_<n>` in the form `<count>r/<s|m|h|d>`. It states the source limit: HAProxy denies `/login` when one client IP makes more than 10 requests in 10 seconds. The rate is either equivalent to that limit (`1r/s` or `60r/m`), or the answer says why its value differs, for example that BunkerWeb counts over a different window than HAProxy's 10 seconds. A rate with no stated source limit, or a different rate with no reason (`10r/m` alone), does not pass. It leaves the default `/` rule in place or says it is there (`USE_LIMIT_REQ` defaults to `yes` at `2r/s` on every path).
8. Says the HAProxy `.pem` bundle (certificate and key in one file) must be split into a certificate file and a key file, and maps the certificate to `USE_CUSTOM_SSL=yes` with `CUSTOM_SSL_CERT` and `CUSTOM_SSL_KEY` (original or mounted paths), or to `AUTO_LETS_ENCRYPT=yes`. It also says the files must be readable by the scheduler or mounted into it.
9. Maps `http-request redirect scheme https` to `REDIRECT_HTTP_TO_HTTPS=yes`, or says BunkerWeb already redirects through `AUTO_REDIRECT_HTTP_TO_HTTPS` once a certificate source exists.
10. Recommends a parallel run with `SECURITY_MODE=detect` before cutover and writes down a rollback that restores HAProxy.
