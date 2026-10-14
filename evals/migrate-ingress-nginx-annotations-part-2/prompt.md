---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

ingress-nginx is retired and I want to move shop.example.com to BunkerWeb 1.6.15 (Helm chart 1.1.0) in the same cluster, next to ingress-nginx first, then cut over. These are my three Ingresses in the namespace `prod`, all `ingressClassName: nginx`, host `shop.example.com`, TLS secret `shop-tls`:

    metadata:
      name: shop
      annotations:
        nginx.ingress.kubernetes.io/ssl-redirect: "true"
        nginx.ingress.kubernetes.io/proxy-body-size: "5m"
        nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
        nginx.ingress.kubernetes.io/configuration-snippet: |
          more_set_headers "X-Frame-Options: DENY";
    spec: path / (Prefix) -> Service shop, port 80

    metadata:
      name: shop-admin
      annotations:
        nginx.ingress.kubernetes.io/whitelist-source-range: "10.0.0.0/8"
        nginx.ingress.kubernetes.io/auth-type: basic
        nginx.ingress.kubernetes.io/auth-secret: admin-auth
    spec: path /admin (Prefix) -> Service shop, port 80

    metadata:
      name: shop-api
      annotations:
        nginx.ingress.kubernetes.io/use-regex: "true"
        nginx.ingress.kubernetes.io/rewrite-target: /$2
        nginx.ingress.kubernetes.io/limit-rps: "5"
    spec: path /api(/|$)(.*) (ImplementationSpecific) -> Service api, port 8080

The shop uses websockets on `/`. Give me the BunkerWeb Ingresses, what does not carry over, and the cutover.
