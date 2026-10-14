---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

BunkerWeb 1.6.15 installed from the Debian package, one site www.example.com, MULTISITE=no. I created /etc/bunkerweb/configs/modsec/www.example.com/remove-942100.conf containing `SecRuleRemoveById 942100` and reloaded, but requests to /search?q=... are still blocked by rule 942100. Why does my exclusion do nothing?
