---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

I run authentik 2026.8 (server container `authentik-server`, port 9000) behind this nginx and want to move it to BunkerWeb 1.6.15 on Docker for `sso.example.com`. Login, the admin UI, API clients, outposts and our OIDC apps must keep working after the switch. Write the BunkerWeb settings I need.

    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    server {
        listen 443 ssl http2;
        server_name sso.example.com;
        client_max_body_size 64m;
        add_header Strict-Transport-Security "max-age=31536000" always;

        location / {
            proxy_pass http://authentik-server:9000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
        }
    }
