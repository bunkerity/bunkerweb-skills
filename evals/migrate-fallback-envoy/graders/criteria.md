---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Sets `SERVER_NAME` to `api.example.com` and `USE_REVERSE_PROXY=yes`. A `<server_name>_` prefix on a setting name is fine.
2. Maps the two routes to two reverse proxy entries, `/v1/` to `http://api:8080` and `/` to `http://web:3000`, each as a `REVERSE_PROXY_URL` and `REVERSE_PROXY_HOST` pair (the second pair numbered, `_2`). Each host has a scheme and no path after the port.
3. Carries the `120s` route timeout of `/v1/` as `REVERSE_PROXY_READ_TIMEOUT_<n>` on that entry. Setting it on every entry is also accepted.
4. Names a certificate source setting for HTTPS: `USE_CUSTOM_SSL` with `CUSTOM_SSL_CERT` and `CUSTOM_SSL_KEY`, `AUTO_LETS_ENCRYPT`, or `GENERATE_SELF_SIGNED_SSL`. If it uses the custom files, it says the scheduler must be able to read them.
5. Lists the `retry_policy` (`retry_on: 5xx`, two retries) as not carried over, because BunkerWeb's reverse proxy has no retry setting, and does not invent a setting for it.
6. Recommends a parallel run with `SECURITY_MODE=detect` before cutover, and writes down a rollback.
