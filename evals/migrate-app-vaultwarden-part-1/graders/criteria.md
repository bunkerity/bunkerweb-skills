---
type: llm
weight: 2
---

Score 1 only if ALL hold. A `<server_name>_` prefix on a setting name is fine.

1. Sets `USE_REVERSE_PROXY=yes` with `REVERSE_PROXY_HOST` pointing at the `vaultwarden` container on port 80 (`http://vaultwarden` or `http://vaultwarden:80`), and `REVERSE_PROXY_WS=yes` for the notification socket. It does not add a second port or a second upstream for it.
2. Sets `ALLOWED_METHODS` so that it keeps GET, POST and HEAD and adds `PUT` and `DELETE` (the skill's tested value `GET|POST|HEAD|OPTIONS|PUT|DELETE`, which also adds `OPTIONS` and drops `QUERY`, qualifies), and says why: the default list (`GET|POST|HEAD|QUERY`) makes the web vault's item and folder edits fail with `405`.
3. Sets `MAX_CLIENT_SIZE` high enough for the 25 MB attachments (any value from `30m` up to the old `525m`) and says the default `10m` gives `413`.
4. Raises `MODSECURITY_REQ_BODY_NO_FILES_LIMIT` (the default `131072` is far below a big JSON import) and says a large import is otherwise refused with `400`, ModSecurity rule `200002`. Raising `MAX_CLIENT_SIZE` alone does not count.
5. Warns that in block mode the OWASP CRS gives `403` on ordinary saves of vault items, because the clients send every field as an encrypted base64 string that CRS can mistake for a shell, file-access or XSS payload, and names at least two of the rules `932125`, `932370`, `932380`, `930120`, `941120`. It adds that attachment uploads trip rule `920120` on the filename.
6. Tells the user to run `SECURITY_MODE=detect` first, read the BunkerWeb log while the web vault and extension are used, and write the exclusion before switching to `block`. The reason it gives includes that repeated `403` answers count towards the bad-behavior ban (about ten within a minute bans the client IP for a day).
