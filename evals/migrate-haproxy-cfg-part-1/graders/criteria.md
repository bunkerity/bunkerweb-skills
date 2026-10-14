---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Sets `USE_REVERSE_PROXY=yes`, sets `SERVER_NAME` to `shop.example.com`, and gives the default `/` entry a `REVERSE_PROXY_HOST` whose value is exactly `http://app:3000` (a path after the port fails). A `<server_name>_` prefix on a setting name is fine. Other numbered entries may repeat the same host.
2. Gives `/socket` its own numbered reverse proxy entry with `REVERSE_PROXY_URL_<n>=/socket` and `REVERSE_PROXY_WS_<n>=yes`. It does not write the `Upgrade` and `Connection` headers by hand.
3. Carries `timeout tunnel 1h` over by setting `REVERSE_PROXY_READ_TIMEOUT_<n>` on that websocket entry to `1h` (or `3600s`). Setting only a send timeout, a connect timeout, or nothing, does not pass.
4. Sets `MAX_CLIENT_SIZE` to `20m` (a `<server_name>_` prefix is fine).
5. Sets HSTS with the `STRICT_TRANSPORT_SECURITY` setting and the value `max-age=31536000; includeSubDomains`, not with a raw header.
6. Keeps the `/admin` rule for that path only: a file with `allow 10.0.0.0/8; deny all;` loaded through `REVERSE_PROXY_INCLUDES_<n>` on a numbered `/admin` entry. Not accepted: dropping the rule, or presenting `WHITELIST_IP` as the ACL.
