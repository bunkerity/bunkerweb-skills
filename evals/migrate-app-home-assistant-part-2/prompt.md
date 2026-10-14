---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I run Home Assistant 2026.9 in Docker behind a plain nginx container and want to move the front end to BunkerWeb 1.6.15 on the same Docker host. This is the nginx server block I use today:

```nginx
server {
    listen 443 ssl;
    http2 on;
    server_name ha.example.com;
    ssl_certificate     /etc/nginx/certs/ha.example.com.pem;
    ssl_certificate_key /etc/nginx/certs/ha.example.com.key;

    client_max_body_size 100m;          # I upload backups of 20 to 80 MB

    location / {
        proxy_pass http://homeassistant:8123;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

In `configuration.yaml` I have `http:` with `use_x_forwarded_for: true` and `trusted_proxies: [192.0.2.5]`, which is the nginx container. I also have scripts that call the REST API: they create and delete entities, render Jinja templates through `POST /api/template`, and read the `/api/stream` event stream. Give me the BunkerWeb settings (Docker Compose environment) and tell me what will break if I only copy the proxy lines. Keep it short: the settings, then one line per thing that breaks.
