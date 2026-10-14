---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I read my Nginx Proxy Manager 2.16 setup through its API and want to move it to BunkerWeb 1.6.15 (Docker, multisite). One proxy host, `portal.example.com`:

- Forward `http://portal:8080`, Websockets Support on, Block Common Exploits on.
- Force SSL on, HSTS on with subdomains off (the host answers `Strict-Transport-Security: max-age=63072000; preload`). Custom certificate in `/data/custom_ssl/npm-3/fullchain.pem` and `privkey.pem`.
- Access list `staff`, Satisfy All: user `alice` (stored as an `$apr1$...` hash), rules `allow 10.1.2.0/24` and `deny all`.
- One custom location `/api` forwarding to `http://portal-api:9000` with Forward Path `/v2`.
- Advanced tab: `client_max_body_size 5m;`.

A load balancer in front of NPM sends the real client address in `X-Real-IP`, and NPM trusts it. I will run BunkerWeb next to NPM in `SECURITY_MODE=detect` first. Write the BunkerWeb settings, and tell me whether that detect run will show that the access list works.
