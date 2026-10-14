---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

BunkerWeb 1.6.15 in Docker protects app.example.com. Since enabling it, every POST to /api/upload fails with 403. The BunkerWeb logs show:

    ModSecurity: Access denied with code 403 (phase 2). ... [id "949110"] [msg "Inbound Anomaly Score Exceeded (Total Score: 5)"] ... [uri "/api/upload"]
    ModSecurity: Warning. ... [id "920420"] [msg "Request content type is not allowed by policy"] ... [uri "/api/upload"]

The client sends Content-Type: application/vnd.api+json (JSON:API). How do I fix this without weakening protection for the rest of the site?
