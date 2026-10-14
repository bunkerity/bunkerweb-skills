---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

We run Kubernetes with Helm. I want BunkerWeb as the ingress controller in front of the existing `shop` Service (port 80) for shop.example.com, with antibot captcha enabled only on that host. What do I install and what does the Ingress look like?
