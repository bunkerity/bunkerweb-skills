---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Every BunkerWeb image is pinned to the tag `1.6.15`, and the file has both `bunkerity/bunkerweb:1.6.15` and `bunkerity/bunkerweb-scheduler:1.6.15` (the 1.6 Docker integration needs both). No `:latest`, no untagged BunkerWeb image, no other 1.6.x tag. A file with only one `bunkerity/bunkerweb` service and no scheduler FAILS.
2. The service settings are in the environment of the scheduler container (`bw-scheduler` or equivalent), not only of the `bunkerweb` container: `SERVER_NAME`, `USE_REVERSE_PROXY`, `REVERSE_PROXY_HOST`, `AUTO_LETS_ENCRYPT` and `SECURITY_MODE` (an `app.example.com_` prefix on any of them is fine). `BUNKERWEB_INSTANCES` on the scheduler is the name of the `bunkerweb` service. Service settings only on the `bunkerweb` container FAIL.
3. `API_WHITELIST_IP` is set on BOTH the `bunkerweb` and the scheduler containers and its value includes the subnet the scheduler runs in (the default `127.0.0.0/8` does not admit a scheduler on a Docker network). An `environment` merged from a shared YAML anchor (`<<: *name`) into both services counts as set on both. Omitting it, or setting it on one container only, FAILS.
4. `API_TOKEN` is set to the same non-empty value on BOTH the `bunkerweb` and the scheduler containers (a variable reference such as `${BW_API_TOKEN}`, with or without a `:?` default, counts, and so does a value merged into both services from a shared YAML anchor). An answer that never sets `API_TOKEN` FAILS.
5. The proxy target is `http://myapp:8080` (`USE_REVERSE_PROXY=yes`, `REVERSE_PROXY_HOST=http://myapp:8080`, with or without the `app.example.com_` prefix), `AUTO_LETS_ENCRYPT` is `yes` for app.example.com, `myapp` and `bunkerweb` share a network, and `myapp` has no published `ports`.
6. Recommends starting with `SECURITY_MODE=detect` and switching to `block` after reading the logs, or explains that rollout.
7. Includes at least one curl command whose URL contains app.example.com (or 127.0.0.1 with a `Host: app.example.com` header), and states the HTTP status code or response header the user should see from it.
