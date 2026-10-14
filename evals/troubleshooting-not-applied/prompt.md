---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

BunkerWeb 1.6.15, Docker integration, MULTISITE=yes with two services: app.example.com and api.example.com. I added USE_ANTIBOT=captcha to the bunkerweb container environment to protect only app.example.com, restarted, and nothing changed. Why?
