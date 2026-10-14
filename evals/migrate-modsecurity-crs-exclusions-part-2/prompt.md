---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I run `owasp/modsecurity-crs:4.30.0-nginx-202610051210` in front of one app and want to move that WAF layer to BunkerWeb 1.6.15 (Docker, multisite) for app.example.com. The backend is `http://app:3000`. Convert my ModSecurity settings, tell me where each one goes, and how to run both side by side before I cut over.

Container environment:

    BACKEND=http://app:3000
    BLOCKING_PARANOIA=2
    DETECTION_PARANOIA=3
    ANOMALY_INBOUND=10
    ANOMALY_OUTBOUND=10
    ALLOWED_METHODS=GET POST HEAD OPTIONS
    MODSEC_RULE_ENGINE=On
    MODSEC_REQ_BODY_LIMIT=5242880
    MODSEC_REQ_BODY_NOFILES_LIMIT=5242880

Mounted as `/etc/modsecurity.d/owasp-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf`:

    SecRule REQUEST_URI "@beginsWith /search" "id:1000002,phase:1,pass,nolog,ctl:ruleRemoveTargetById=942330;ARGS:q"
    SecRule REQUEST_HEADERS:X-Debug "@streq on" "id:1000200,phase:1,deny,status:403,log,msg:'debug header refused'"

Mounted as `/etc/modsecurity.d/owasp-crs/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf`:

    SecRuleRemoveById 920300
    SecRuleUpdateTargetById 942330 "!ARGS:comment"
