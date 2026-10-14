---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

My shop runs behind Traefik v3 with these docker labels. The BunkerWeb 1.6.15 autoconf stack is already running, so I only need the labels for the application container, plus how to test them next to Traefik before I switch. Convert them:

    labels:
      - traefik.enable=true
      - traefik.http.services.shop.loadbalancer.server.port=8080
      - traefik.http.routers.shop.rule=Host(`shop.example.com`)
      - traefik.http.routers.shop.tls.certresolver=letsencrypt
      - traefik.http.routers.shop-admin.rule=Host(`shop.example.com`) && PathPrefix(`/admin`)
      - traefik.http.routers.shop-admin.tls.certresolver=letsencrypt
      - traefik.http.routers.shop-admin.middlewares=admin-ips
      - traefik.http.middlewares.admin-ips.ipallowlist.sourcerange=10.1.2.0/24
      - traefik.http.routers.shop-api.rule=Host(`shop.example.com`) && PathPrefix(`/api`)
      - traefik.http.routers.shop-api.tls.certresolver=letsencrypt
      - traefik.http.routers.shop-api.middlewares=api-strip
      - traefik.http.middlewares.api-strip.stripprefix.prefixes=/api
      - traefik.http.routers.shop-login.rule=Host(`shop.example.com`) && Path(`/login`)
      - traefik.http.routers.shop-login.tls.certresolver=letsencrypt
      - traefik.http.routers.shop-login.middlewares=login-rl
      - traefik.http.middlewares.login-rl.ratelimit.average=3
      - traefik.http.middlewares.login-rl.ratelimit.period=1m
      - traefik.http.middlewares.login-rl.ratelimit.burst=3
