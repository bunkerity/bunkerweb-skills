---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Maps the fail2ban jails to `USE_BAD_BEHAVIOR` with `BAD_BEHAVIOR_THRESHOLD=3` and `BAD_BEHAVIOR_BAN_TIME=3600`. It adds at least one of: bad behavior keeps a counter per client and service, detect mode does not ban, or the test client can ban itself.
8. Covers the default server: sets `DISABLE_DEFAULT_SERVER=yes` and says unknown hosts get 403, and says SWAG's default site (`server_name _`) answered them before.
9. Says the certificate is issued by BunkerWeb itself (not copied from `/config/etc/letsencrypt`), or, if the answer reuses SWAG's files with `USE_CUSTOM_SSL`, says the scheduler must be able to read the key and that it does not renew it.
10. Recommends a parallel run with `SECURITY_MODE=detect` before cutover, and writes down a rollback that restores SWAG on ports 80 and 443.
