---
type: llm
weight: 2
---

Score 1 only if ALL hold. A `<server_name>_` prefix on a setting name is fine.

1. Sets `USE_REVERSE_PROXY=yes` with `REVERSE_PROXY_HOST` pointing at the `nextcloud` container (`http://nextcloud`, with or without `:80`) and sets `MAX_CLIENT_SIZE` (any value; a lower value with a reason is fine).
2. Sets `ALLOWED_METHODS` to a list that keeps GET, POST and HEAD and adds at least the WebDAV verbs `PROPFIND`, `PROPPATCH`, `MKCOL`, `MOVE`, `COPY`, `LOCK`, `UNLOCK`, `REPORT`, plus `PUT` and `DELETE`.
3. Enables the OWASP CRS plugin with `MODSECURITY_CRS_PLUGINS=nextcloud-rule-exclusions`.
