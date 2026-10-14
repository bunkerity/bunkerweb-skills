---
type: llm
weight: 2
---

Score 1 only if ALL hold:

4. Gives `/ws` its own numbered reverse proxy entry with `REVERSE_PROXY_WS_<n>=yes`, for example `REVERSE_PROXY_URL_2=/ws`. It does not write the `Upgrade` and `Connection` headers by hand.
5. Keeps the `/admin` allow and deny rule for that path only. Accepted: a file with `allow 10.0.0.0/8; deny all;` loaded through `REVERSE_PROXY_INCLUDES_<n>` on a numbered `/admin` entry, or a `server-http` custom config holding the `/admin` location. Not accepted: dropping the rule, or presenting `WHITELIST_IP` as the ACL. If it uses a custom config location, it says that location does not get BunkerWeb's generated proxy settings or protections automatically.
6. Converts the `/api/` entry with a regex location: `REVERSE_PROXY_URL_<n>=^/api/(.*)$` and `REVERSE_PROXY_HOST_<n>=http://app:3000/v2/$1$is_args$args` (doubled as `$$` in a compose file is fine). It says that a fixed path in the host replaces the whole request URI. It does not use a URI `rewrite` include or a fixed `/v2/` host path as the replacement.
