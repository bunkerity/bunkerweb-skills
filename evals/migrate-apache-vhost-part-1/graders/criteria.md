---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Sets `USE_REVERSE_PROXY=yes`, sets `SERVER_NAME` to `app.example.com`, and gives the default `/` entry a `REVERSE_PROXY_HOST` whose value is exactly `http://app:3000` (a path after the port fails). A `<server_name>_` prefix on a setting name is fine. Other numbered entries may repeat the same host.
2. Gives `/ws` its own numbered reverse proxy entry with `REVERSE_PROXY_WS_<n>=yes` and a `REVERSE_PROXY_HOST_<n>` that starts with `http://`. It does not write `ws://app:3000` as a `REVERSE_PROXY_HOST` value, and does not write the `Upgrade` and `Connection` headers by hand.
3. Sets `MAX_CLIENT_SIZE` to `20m` (a `<server_name>_` prefix is fine).
4. Sets HSTS with the `STRICT_TRANSPORT_SECURITY` setting and the value `max-age=31536000; includeSubDomains`, not with a raw header.
5. Keeps the `/admin` rule for that path only: a file with `allow 10.0.0.0/8; deny all;` loaded through `REVERSE_PROXY_INCLUDES_<n>` on a numbered `/admin` entry. Not accepted: dropping the rule, or presenting `WHITELIST_IP` as the ACL. A custom config that holds the whole `/admin` location is accepted only if the answer says that location does not get BunkerWeb's generated proxy settings or protections automatically.
6. Handles the redirect with `REDIRECT_FROM`, `REDIRECT_TO` set to `https://app.example.com/new` and `REDIRECT_TO_STATUS_CODE` set to `301` (the default is also 301), not with a raw nginx `return` in a custom config. A `<server_name>_` prefix is fine.
