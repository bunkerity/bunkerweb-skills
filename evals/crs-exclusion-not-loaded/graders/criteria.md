---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Explains that per-service custom config directories are only included when MULTISITE=yes, so this file is never loaded, and fixes it: move the file to the global modsec directory, or enable multisite.
2. Does NOT claim SecRuleRemoveById fails because of its include or load order relative to the CRS. In libmodsecurity v3 it is a runtime exception checked as each rule evaluates.
3. Suggests narrowing the exclusion to /search and the q argument (for example SecRuleUpdateTargetById, or a ctl: rule scoped by path) instead of removing 942100 everywhere, or flags the site-wide removal as the user's explicit choice.
4. Says how to confirm the file is now loaded.
