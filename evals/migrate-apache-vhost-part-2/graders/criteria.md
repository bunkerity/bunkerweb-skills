---
type: llm
weight: 2
---

Score 1 only if ALL hold:

7. Maps the certificate to `USE_CUSTOM_SSL=yes` with `CUSTOM_SSL_CERT` and `CUSTOM_SSL_KEY` pointing at the certificate and key files, at their original paths (`/etc/ssl/app.crt`, `/etc/ssl/app.key`) or at the paths where the answer mounts them, or to `AUTO_LETS_ENCRYPT=yes`. It also says the files must be readable by the scheduler (not only the BunkerWeb container) or that they must be mounted into it.
8. Lists `ProxyPassReverse` as having no BunkerWeb setting ("not carried over") and tells the user to check the `Location` header the backend returns in the parallel run.
9. Says BunkerWeb turns on protections the Apache vhost did not have and names `USE_LIMIT_REQ` with its `2r/s` default, or ModSecurity with the OWASP CRS, as something to review in the detect run.
10. Recommends a parallel run with `SECURITY_MODE=detect` before cutover and writes down a rollback that restores Apache.
