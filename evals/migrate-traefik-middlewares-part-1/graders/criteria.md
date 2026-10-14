---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Puts the settings on the application container as labels in the form `bunkerweb.<SETTING>=<value>`, with `bunkerweb.SERVER_NAME=shop.example.com`, `bunkerweb.USE_REVERSE_PROXY=yes` and an unnumbered `bunkerweb.REVERSE_PROXY_HOST` that ends in `:8080` (numbered `REVERSE_PROXY_HOST_<n>` entries for other locations may end differently). No `<site>_` prefixes and no Kubernetes `bunkerweb.io/` annotations.
2. Scopes the `10.1.2.0/24` allow list to `/admin`. Either `bunkerweb.GREYLIST_URI` with a regex that excludes `/admin` (for example `^(?!/admin)`) next to `bunkerweb.USE_GREYLIST=yes` and `bunkerweb.GREYLIST_IP=10.1.2.0/24`, or a separate `/admin` location (`REVERSE_PROXY_URL_<n>=/admin`) with a `REVERSE_PROXY_INCLUDES_<n>` file holding `allow`/`deny`. It does not map the allow list to `GREYLIST_IP` alone, and it does not use `WHITELIST_IP`.
3. Converts the `/api` strip prefix with a regex location: `bunkerweb.REVERSE_PROXY_URL_<n>=^/api/(.*)$` and a `bunkerweb.REVERSE_PROXY_HOST_<n>` that ends in `/$1$is_args$args` (doubled as `$$` in a compose file is fine). It does not use an include with `rewrite ... break`, and it does not use a host with a trailing `/` as the way to strip the prefix.
4. In compose label values, writes every `$` as `$$`, or says that it must be.
5. Converts the rate limit to `bunkerweb.LIMIT_REQ_URL_<n>=/login` with `bunkerweb.LIMIT_REQ_RATE_<n>=3r/m` (or another explicit per-minute rate), and says Traefik's `burst` has no BunkerWeb setting.
6. Says that in `SECURITY_MODE=detect` the greylist (and basic auth and the request limit) only log and do not refuse, so the allow list and the limit have to be tested with the service in `block`, not in the detect run.
