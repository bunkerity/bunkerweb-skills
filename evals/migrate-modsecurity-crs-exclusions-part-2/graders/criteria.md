---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Maps `MODSEC_RULE_ENGINE=On` to `SECURITY_MODE=block` or to BunkerWeb's default `MODSECURITY_SEC_RULE_ENGINE=On` (either is accepted), runs the parallel test with `SECURITY_MODE=detect`, and sets `SECURITY_MODE=block` at cutover.
8. States that BunkerWeb 1.6.15 bundles CRS 4.29.0, which is older than the image's 4.30.0, and that the behaviour is to be retested rather than assumed identical.
9. For the parallel run, tells the user to send the same requests to the old container and to BunkerWeb and to compare, for each request, the rule ids each one logged (a total count per side is not enough), and writes a rollback that restores the old container.
