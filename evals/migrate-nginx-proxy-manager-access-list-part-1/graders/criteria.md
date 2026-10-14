---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Maps the access list's user to `USE_AUTH_BASIC=yes` with `AUTH_BASIC_USER` (`alice`) and `AUTH_BASIC_PASSWORD`, and says NPM's `apr1` hash cannot be reused: the user needs a new clear-text password. A `<server_name>_` prefix on a setting name is fine.
2. Maps the address rules (`allow 10.1.2.0/24`, `deny all`) to `USE_GREYLIST=yes` with `GREYLIST_IP` set to `10.1.2.0/24`. It does not present `WHITELIST_IP` as the way to restrict access; naming `WHITELIST_IP` only as the "Satisfy Any" alternative is fine.
3. Sets `USE_REAL_IP=yes` with `REAL_IP_HEADER` set to `X-Real-IP`, and says the default header is `X-Forwarded-For`, so the address rule fails without it.
4. Gives `/api` its own numbered regex entry, `REVERSE_PROXY_URL_<n>=^/api(.*)$` (NPM's custom location is a literal prefix), with `REVERSE_PROXY_HOST_<n>=http://portal-api:9000/v2$1$is_args$args` (doubled as `$$` in a compose file is fine). It does not use a URI `rewrite` include or a fixed `/v2` host path as the replacement. It says a fixed path inside the host value replaces the whole request path.
5. Sets `MAX_CLIENT_SIZE` to `5m` (a `<server_name>_` prefix is fine).
6. Sets `REVERSE_PROXY_WS=yes` on the `/` entry and `REVERSE_PROXY_WS_<n>=yes` on the `/api` entry: Websockets Support covers every path in NPM, and BunkerWeb sets it per location.
