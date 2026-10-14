---
type: llm
weight: 2
---

Score 1 only if the answer satisfies every numbered item below. A `<server_name>_` prefix on a setting name is fine, and it does not matter whether the answer says it ran anything.

1. Uses `USE_REVERSE_PROXY=yes`, `SERVER_NAME` set to `sso.example.com` and `REVERSE_PROXY_HOST` set to `http://authentik-server:9000`.
2. Turns WebSockets on with `REVERSE_PROXY_WS=yes`, either for the whole service or in a numbered entry for the path `/ws/` (for example `REVERSE_PROXY_URL_1=/ws/` with `REVERSE_PROXY_WS_1=yes`).
3. Sets `REVERSE_PROXY_INTERCEPT_ERRORS` to `no`.
4. Sets `ALLOWED_METHODS` to a list that includes `PUT`, `PATCH`, `DELETE` and `OPTIONS` besides `GET`, `POST` and `HEAD`.
5. Mentions that ModSecurity CRS exclusions may be needed for authentik admin API endpoints, naming at least one of `/api/v3/policies/expression/`, `/api/v3/core/brands/`, `/api/v3/stages/prompt/prompts/`.
6. Carries the source's `client_max_body_size 64m` over: `MAX_CLIENT_SIZE=64m` for the service, or `REVERSE_PROXY_MAX_CLIENT_SIZE_<n>=64m` on a numbered entry for the file upload path `/api/v3/admin/file/`. It says the default `10m` refuses file uploads with `413`. Leaving `MAX_CLIENT_SIZE` at its default, with no per-path value, fails.
