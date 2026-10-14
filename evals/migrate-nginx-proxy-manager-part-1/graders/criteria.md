---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Includes an inventory of the NPM proxy hosts as step 1, before any mapping. It covers at least the domain, the forward target (upstream) and the access lists, and it asks to read the real host config.
2. Uses `MULTISITE=yes` and a `SERVER_NAME` that lists the domains.
3. Writes per-service settings with the domain as prefix, such as `app1.example.com_USE_REVERSE_PROXY=yes` and `app1.example.com_REVERSE_PROXY_HOST=...`.
4. Runs BunkerWeb next to NPM on spare host ports (not 80 or 443) with `SECURITY_MODE=detect`, and switches 80 and 443 only after testing.
5. Names `AUTO_LETS_ENCRYPT=yes` for the certificates.
6. Says the HTTP challenge needs port 80, which NPM still holds during the parallel run. It offers one way to have a certificate before cutover: `LETS_ENCRYPT_CHALLENGE=dns`, or `USE_CUSTOM_SSL=yes` with `CUSTOM_SSL_CERT` and `CUSTOM_SSL_KEY` to reuse the NPM files.
