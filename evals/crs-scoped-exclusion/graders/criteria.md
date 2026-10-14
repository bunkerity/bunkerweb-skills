---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Identifies rule 920420 (content type policy) as the cause and 949110 as the anomaly-score verdict, not as the cause.
2. Allows application/vnd.api+json, either by extending tx.allowed_request_content_type (the shipped list plus the new type, in a `modsec-crs` custom config; the shipped list at v1.6.15 is `|application/x-www-form-urlencoded| |multipart/form-data| |text/xml| |application/xml| |application/soap+xml| |application/json|`, so a list that drops one of these six fails) or by an exclusion scoped to /api/upload.
3. Ships a rule that arms the JSON request body processor (ctl:requestBodyProcessor=JSON) for application/vnd.api+json requests, whichever route criterion 2 took. An answer without that rule FAILS, even if it explains the risk: without it the body goes uninspected.
4. Does NOT turn ModSecurity or CRS off for the service and does NOT raise the anomaly threshold.
5. Tells the user how to confirm the fix (repeat the request, check the log).
