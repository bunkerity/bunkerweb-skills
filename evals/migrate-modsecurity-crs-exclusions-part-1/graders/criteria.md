---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Puts the paranoia levels in a `modsec-crs` custom config as `SecAction` lines with `setvar` of `tx.blocking_paranoia_level=2` and `tx.detection_paranoia_level=3`. It does not offer a BunkerWeb setting for either level (none exists in 1.6.15).
2. Puts the anomaly thresholds in the same way, in `modsec-crs`: `tx.inbound_anomaly_score_threshold=10` and `tx.outbound_anomaly_score_threshold=10`.
3. Maps `ALLOWED_METHODS=GET POST HEAD OPTIONS` to the BunkerWeb setting `ALLOWED_METHODS` with a pipe-separated value (`GET|POST|HEAD|OPTIONS`), and does not rely on a `tx.allowed_methods` `SecAction` for it (BunkerWeb rewrites that variable from the setting).
4. Maps the two body limits to the exact setting names `MODSECURITY_SEC_REQUEST_BODY_LIMIT` (from `MODSEC_REQ_BODY_LIMIT`) and `MODSECURITY_REQ_BODY_NO_FILES_LIMIT` (from `MODSEC_REQ_BODY_NOFILES_LIMIT`), each with the value `5242880` or `5m`.
5. Places the two rules of the `REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf` file (the `ctl:` rule and the `X-Debug` deny rule) in a `modsec-crs` custom config, and the `SecRuleRemoveById 920300` and `SecRuleUpdateTargetById 942330` lines of the `RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf` file in `modsec` (`modsec-crs` is also accepted for those two lines).
6. Delivers the custom configs per service for `app.example.com` with `MULTISITE=yes`: a scheduler environment variable `app.example.com_CUSTOM_CONF_MODSEC_CRS_<name>` or `app.example.com_CUSTOM_CONF_MODSEC_<name>`, or `.conf` files in a directory named after the service under the scheduler's `/data/configs/modsec-crs/` and `/data/configs/modsec/`. A file name without the `.conf` extension is not accepted.
