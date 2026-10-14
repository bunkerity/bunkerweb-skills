---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Sets `USE_REVERSE_PROXY=yes`, sets `SERVER_NAME` to `app.example.com`, and gives the default `/` entry a `REVERSE_PROXY_HOST` whose value is exactly `http://app:3000` (a path after the port fails). A `<server_name>_` prefix on a setting name is fine. Other numbered entries may repeat the same host.
2. Handles `handle_path /api/*` with its own numbered reverse proxy entry: `REVERSE_PROXY_URL_<n>=^/api/(.*)$` and `REVERSE_PROXY_HOST_<n>=http://app:3000/$1$is_args$args` (doubled as `$$` in a compose file is fine). Not accepted: a URI `rewrite` include, a fixed host path as the way to strip the prefix, or a plain `/api/` prefix with no mention of the `/api` request.
3. Sets `MAX_CLIENT_SIZE` to the byte count `5000000`, and says that Caddy's `5MB` is 5,000,000 bytes, so `5m` (5,242,880 bytes) would admit slightly larger bodies. A `<server_name>_` prefix is fine.
4. Handles `redir /old` with `REDIRECT_FROM` as an anchored regex such as `^/old$` (not the bare `/old`, which is a prefix in nginx and also matches `/older`), `REDIRECT_TO` set to `https://app.example.com/new` and `REDIRECT_TO_STATUS_CODE` set to `301`. Not accepted: a raw nginx `return` in a custom config.
5. Keeps the `/admin` rule for that path only: a file with `allow 10.0.0.0/8; deny all;` loaded through `REVERSE_PROXY_INCLUDES_<n>` on a numbered `/admin` entry, together with `USE_REAL_IP=yes`, because the Caddyfile trusts `X-Forwarded-For` from private ranges (`trusted_proxies`) and its `client_ip` matcher follows the real client address. Not accepted: dropping the rule, or presenting `WHITELIST_IP` as the ACL. `API_WHITELIST_IP` (the API allowlist in the stack) is unrelated and does not count against this. A remark that `/api/admin` reaches the upstream without the ACL because Caddy's `handle_path` runs before `respond` is correct (proven live) and does not fail this criterion.
6. Maps `basic_auth` to `USE_AUTH_BASIC=yes` with `AUTH_BASIC_LOCATION=/secure`, `AUTH_BASIC_USER` `alice` and an `AUTH_BASIC_PASSWORD`, says the setting takes a plain-text password so the bcrypt hash cannot be reused, and says basic auth is not enforced in detect mode, so it must be tested in block mode.
