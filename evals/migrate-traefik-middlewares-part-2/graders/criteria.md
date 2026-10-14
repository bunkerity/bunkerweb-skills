---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Warns that BunkerWeb's bad behavior ban (`USE_BAD_BEHAVIOR`, default on) bans the test client's IP after repeated 4xx answers, and says how to lift it (`bwcli unban`) or to disable it for the test.
8. Maps `tls.certresolver` to `bunkerweb.AUTO_LETS_ENCRYPT=yes` with `bunkerweb.EMAIL_LETS_ENCRYPT`, and says Traefik's `acme.json` is not reused, so the certificate is re-issued or converted.
