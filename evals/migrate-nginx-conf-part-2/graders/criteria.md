---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Carries the `map` block into an `http` type custom config (a `CUSTOM_CONF_HTTP_<name>` variable on the scheduler, or a `.conf` file under the scheduler's `/data/configs/http/`), and carries the server-level `proxy_set_header X-Tier $tier` as `X-Tier $tier` in `REVERSE_PROXY_HEADERS` (`_<n>` on numbered entries) of the entries that inherited it. It says that a server-level `proxy_set_header` does not reach BunkerWeb's generated locations.
8. Converts `limit_req` on `/login` to `USE_LIMIT_REQ` with `LIMIT_REQ_URL_2` set to a pattern anchored on `/login` (for example `^/login$`) and `LIMIT_REQ_RATE_2` set to `3r/m`, numbered `_2` because the unnumbered pair is the default `/` rule at `2r/s` that stays in place, and says that BunkerWeb has no `burst` setting. A `<server_name>_` prefix on the setting names is fine.
9. Converts `auth_basic` to `USE_AUTH_BASIC=yes` with `AUTH_BASIC_LOCATION` set to `/reports/` and an `AUTH_BASIC_USER` and `AUTH_BASIC_PASSWORD` pair. It says the `htpasswd` hashes cannot be imported, so passwords are set again, and that `USE_AUTH_BASIC` is not enforced in detect mode, so it must be tested again in block mode.
10. Says HTTPS needs a certificate source and names at least one BunkerWeb setting for it: `AUTO_LETS_ENCRYPT`, `USE_CUSTOM_SSL` with `CUSTOM_SSL_CERT` and `CUSTOM_SSL_KEY`, or `GENERATE_SELF_SIGNED_SSL`. A setting shown as a commented option counts.
11. Recommends a parallel run with `SECURITY_MODE=detect` before cutover and writes down a rollback.
