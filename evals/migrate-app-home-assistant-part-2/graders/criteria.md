---
type: llm
weight: 2
---

Score 1 only if ALL hold. Wording may differ; the facts must be present:

7. Handles `POST /api/template` (Jinja `{{ }}`, CRS rule `934200`) with a ModSecurity exclusion limited to that path and the `template` member, for example `ctl:ruleRemoveTargetById=934200;ARGS:json.template` in a `modsec` custom config.
