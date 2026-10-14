---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Puts the settings on the application container as labels in the form `bunkerweb.<SETTING>=<value>`. It does not use `<site>_` prefixes or Kubernetes `bunkerweb.io/` annotations.
2. Sets `bunkerweb.SERVER_NAME=blog.example.com`, `bunkerweb.USE_REVERSE_PROXY=yes` and a `bunkerweb.REVERSE_PROXY_HOST` that ends in `:2368`.
3. Sets `bunkerweb.AUTO_LETS_ENCRYPT=yes`, either in the labels or at cutover when the parallel run cannot validate on spare ports.
4. Includes the three autoconf containers (BunkerWeb, the scheduler and `bw-autoconf`) with images pinned to a tag such as `1.6.15`, none on `latest`.
5. Gives the BunkerWeb container the label `bunkerweb.INSTANCE=yes` and the scheduler `MULTISITE=yes`.
6. Mentions a database for the scheduler and autoconf (`DATABASE_URI`) and Docker access for autoconf (`DOCKER_HOST` or a socket proxy).
