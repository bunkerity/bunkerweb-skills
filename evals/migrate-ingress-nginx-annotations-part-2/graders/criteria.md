---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Maps `auth-type: basic` to `USE_AUTH_BASIC: "yes"` with `AUTH_BASIC_USER` and `AUTH_BASIC_PASSWORD`, scopes it to `/admin` with `AUTH_BASIC_LOCATION` (the default `sitewide` would protect the whole shop), and says the password hash in the `admin-auth` Secret cannot be imported, so the user needs a new password.
8. Lists `configuration-snippet` as not carried over, with the reason that it holds raw nginx and BunkerWeb has no annotation that carries raw nginx. Re-expressing its one header with a native setting such as `X_FRAME_OPTIONS` or `CUSTOM_HEADER` is fine.
9. Maps `proxy-body-size: "5m"` to `MAX_CLIENT_SIZE: "5m"`, or to `REVERSE_PROXY_MAX_CLIENT_SIZE: "5m"` on the `/` path, and `ssl-redirect` to `REDIRECT_HTTP_TO_HTTPS: "yes"`.
10. Runs BunkerWeb next to ingress-nginx with `SECURITY_MODE` at `detect`, and says detect mode logs the basic-auth, greylist and rate-limit checks without enforcing them, so a pass with `block` is needed before cutover.
11. Writes a rollback for the cutover that points DNS back to the ingress-nginx address, with the original Ingresses and controller left running until the end.
