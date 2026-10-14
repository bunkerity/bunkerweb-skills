---
type: llm
weight: 2
---

Score 1 only if ALL hold:

4. Certificates: `AUTO_LETS_ENCRYPT=yes`, `LETS_ENCRYPT_CHALLENGE=dns`, `LETS_ENCRYPT_DNS_PROVIDER=cloudflare`, and `LETS_ENCRYPT_DNS_CREDENTIAL_ITEM` carrying the token under a key that names the Cloudflare API token (`dns_cloudflare_api_token` or `cloudflare_api_token`). The value may be `abc123` or a variable or secret standing for it. `EMAIL_LETS_ENCRYPT` is `ops@example.com`.
5. The `/admin` rule is kept for that path only: a file with `allow 192.168.1.0/24; deny all;` loaded through `REVERSE_PROXY_INCLUDES_<n>` on a numbered `/admin` entry. Not accepted: dropping the rule, or presenting `WHITELIST_IP` as the ACL.
6. Says what the stock `proxy.conf` did that BunkerWeb does not do by itself, and handles it: `REVERSE_PROXY_WS_<n>=yes` for websockets (SWAG allowed upgrades on every location), the `240` second timeouts set as `REVERSE_PROXY_READ_TIMEOUT` (or the connect or send variant) with a value of `240s`, and that `proxy_redirect` has no BunkerWeb setting ("not carried over"). It names at least one header SWAG sent that needs `REVERSE_PROXY_HEADERS` (`X-Forwarded-Uri`, `X-Forwarded-Method`, `X-Forwarded-Port` or `X-Original-URL`).
