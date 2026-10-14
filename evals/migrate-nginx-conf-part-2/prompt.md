---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Convert this nginx config to BunkerWeb 1.6.15 (Docker) for app.example.com:

    map $arg_tier $tier { default standard; gold premium; }
    limit_req_zone $binary_remote_addr zone=login:10m rate=3r/m;

    server {
        listen 443 ssl http2;
        server_name app.example.com;
        client_max_body_size 50m;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options DENY always;
        proxy_set_header X-Tier $tier;
        location / {
            proxy_pass http://app:3000;
        }
        location /ws {
            proxy_pass http://app:3000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
        location /api/ {
            proxy_pass http://app:3000/v2/;
        }
        location /admin {
            allow 10.0.0.0/8;
            deny all;
            proxy_pass http://app:3000;
        }
        location = /login {
            limit_req zone=login burst=2 nodelay;
            proxy_pass http://app:3000;
        }
        location /reports/ {
            auth_basic "Restricted";
            auth_basic_user_file /etc/nginx/htpasswd;
            proxy_pass http://app:3000;
        }
    }
