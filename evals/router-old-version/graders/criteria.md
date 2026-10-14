---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. States that 1.5.12 is older than the 1.6.x release line, that the guidance it can give targets 1.6.x, and that it therefore cannot vouch for 1.5.12 behaviour (names both 1.5 and 1.6).
2. Recommends upgrading to 1.6.x, or reading the 1.5 documentation for the exact 1.5 procedure, before changing the running 1.5.12 deployment.
3. Gives no configuration to apply to the running 1.5.12 deployment: no compose file, no environment variables to set, and no rate-limiting setting names offered as verified for 1.5.12. Recommending an upgrade, naming a 1.6 image tag as the upgrade target, or offering to write 1.6 configuration afterwards is allowed.
4. Every difference between 1.5 and 1.6 that the answer states appears in this list: settings moved from the `bunkerweb` container to the scheduler (the `bunkerweb` container keeps only the API settings); the scheduler finds instances through `BUNKERWEB_INSTANCES` instead of the Docker socket proxy; templates are new; autoconf namespaces are new. Stating none of them passes. Stating any other difference FAILS.
