---
type: llm
weight: 2
---

Score 1 only if ALL hold. A `<server_name>_` prefix on a setting name is fine.

4. Says that WebDAV `UNLOCK`, which sends a `Lock-Token` request header, still gets `403` in block mode with that plugin enabled, because CRS rule `920450` restricts that header. It gives a fix of custom config type `modsec-crs` that is limited to the `UNLOCK` method and the `/remote.php/dav/files/` path: either a `setvar` of `tx.restricted_headers_basic` with `/lock-token/` removed from the list, or `ctl:ruleRemoveById=920450` under a rule that tests the method and the path. Not accepted: disabling `920450` for every request, or a path-only exclusion for every method.
5. Recommends running in `SECURITY_MODE=detect` first, reading the BunkerWeb log while the sync clients work, and switching to `block` only after that.
6. Has Nextcloud trust the proxy: `TRUSTED_PROXIES` (or `trusted_proxies`) set to the BunkerWeb network, `OVERWRITEPROTOCOL=https` (or `overwriteprotocol`) and the domain in the trusted domains.
