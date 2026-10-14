---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Tells the user to remove the `traefik.*` labels.
8. Says only one proxy can publish ports 80 and 443 on the host.
9. Uses `bunkerweb.SECURITY_MODE=detect` for the parallel run and says to change it to `block` at cutover.
10. Gives a written rollback that brings Traefik back.
11. Says Traefik's `acme.json` is not reused by BunkerWeb, so the certificate is re-issued or converted.
12. Mentions Let's Encrypt rate limits or `USE_LETS_ENCRYPT_STAGING`.
