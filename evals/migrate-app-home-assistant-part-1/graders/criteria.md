---
type: llm
weight: 2
---

Score 1 only if ALL hold. Wording may differ; the facts must be present:

1. Proxies to `http://homeassistant:8123` with `USE_REVERSE_PROXY=yes` and `REVERSE_PROXY_HOST`.
2. Turns on websockets with `REVERSE_PROXY_WS=yes`, either globally or on a numbered location such as `/api/websocket` (`REVERSE_PROXY_URL_1`, `REVERSE_PROXY_WS_1`).
3. Raises the upload size limit above BunkerWeb's default of `10m` with `MAX_CLIENT_SIZE` or `REVERSE_PROXY_MAX_CLIENT_SIZE`, to 100m or more, so the 20 to 80 MB backups pass.
4. Adds `DELETE` to `ALLOWED_METHODS` (the BunkerWeb default list lacks it).
5. Changes `trusted_proxies` in Home Assistant's `configuration.yaml` so it includes BunkerWeb's address or network.
6. Turns buffering off for `/api/stream` with `REVERSE_PROXY_BUFFERING=no` on its own location.
