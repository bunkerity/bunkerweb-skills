---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. `SERVER_NAME` lists the full names `app.example.com` and `photos.example.com`. It does not write `app.*`. A `<server_name>_` prefix on the other settings is fine.
2. Each service has `USE_REVERSE_PROXY=yes` and, on its default `/` entry, a `REVERSE_PROXY_HOST` whose value is exactly `http://myapp:3000` (app) or `http://immich:2283` (photos), with no path after the port. Other numbered entries may repeat the same host.
3. Sets `MAX_CLIENT_SIZE=0` (unlimited) for the services whose SWAG conf had `client_max_body_size 0`, or says BunkerWeb's default `10m` would otherwise cap uploads.
