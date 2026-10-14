---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Writes BunkerWeb Ingresses with `ingressClassName: bunkerweb` and settings as `bunkerweb.io/<SETTING>` annotations with quoted string values (not labels, not `nginx.ingress.kubernetes.io/`), keeps the `tls:` block with `shop-tls`, leaves the original `nginx` Ingresses in place, and sets the chart value `settings.kubernetes.ingressClass: bunkerweb` so that BunkerWeb handles only its own class (a values file with a comment is enough).
2. Maps `whitelist-source-range: 10.0.0.0/8` to `USE_GREYLIST: "yes"` with `GREYLIST_IP` holding `10.0.0.0/8`. It does not map it to `WHITELIST_IP`.
3. Says the greylist would otherwise apply to the whole host (BunkerWeb merges the Ingresses of one host into one service), and limits it to `/admin` with a `GREYLIST_URI` regex that matches every other URI (a negative lookahead such as `^(?!/admin(/|$))`), so `/` and `/api` stay open to other addresses.
4. For `shop-api`, keeps the Ingress path a plain absolute path such as `/api`, puts a regex that starts with `^` in a `bunkerweb.io/REVERSE_PROXY_URL` annotation, and writes `$2` in a `bunkerweb.io/REVERSE_PROXY_HOST` annotation whose value names the `api` Service in `prod` with port `8080`. It does not use `/api(/|$)(.*)` as the path of a BunkerWeb Ingress.
5. For the websockets on `/`, sets `REVERSE_PROXY_WS: "yes"` and `REVERSE_PROXY_READ_TIMEOUT: "3600s"`, with the `s` unit.
6. Maps `limit-rps: "5"` to a `LIMIT_REQ_URL` that names the `/api` path (`/api` or `^/api`) and `LIMIT_REQ_RATE: "5r/s"` (`USE_LIMIT_REQ` is already `yes` by default, so it may be left out).
