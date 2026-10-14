---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I run linuxserver SWAG (lscr.io/linuxserver/swag) in Docker and want to replace it with BunkerWeb 1.6.15 (Docker, multisite). Convert this and tell me how to cut over.

Container environment:

    URL=example.com
    SUBDOMAINS=app,photos
    VALIDATION=dns
    DNSPLUGIN=cloudflare
    EMAIL=ops@example.com

`/config/dns-conf/cloudflare.ini` holds `dns_cloudflare_api_token = abc123`. `/config/nginx/proxy-confs/app.subdomain.conf`:

    server {
        listen 443 ssl http2;
        server_name app.*;
        include /config/nginx/ssl.conf;
        client_max_body_size 0;
        location / {
            include /config/nginx/proxy.conf;
            include /config/nginx/resolver.conf;
            set $upstream_app myapp;
            set $upstream_port 3000;
            set $upstream_proto http;
            proxy_pass $upstream_proto://$upstream_app:$upstream_port;
        }
        location /admin {
            allow 192.168.1.0/24;
            deny all;
            include /config/nginx/proxy.conf;
            include /config/nginx/resolver.conf;
            set $upstream_app myapp;
            set $upstream_port 3000;
            set $upstream_proto http;
            proxy_pass $upstream_proto://$upstream_app:$upstream_port;
        }
    }

`photos.subdomain.conf` is the same shape for `photos` to `immich:2283`. `/config/fail2ban/jail.local` keeps the SWAG defaults except `maxretry = 3` and `bantime = 3600`. `/config/nginx/proxy.conf` is the stock file.
