---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

My service runs behind Traefik with these docker labels. Move it to BunkerWeb 1.6.15 using autoconf:

    labels:
      - traefik.enable=true
      - traefik.http.routers.blog.rule=Host(`blog.example.com`)
      - traefik.http.routers.blog.tls.certresolver=letsencrypt
      - traefik.http.services.blog.loadbalancer.server.port=2368
