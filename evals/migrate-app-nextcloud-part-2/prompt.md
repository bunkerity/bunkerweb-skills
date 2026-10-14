---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I run Nextcloud behind nginx on one Docker host today and want to move it to BunkerWeb 1.6.15 (Docker). My desktop and phone clients sync files and calendars over WebDAV, and some of them lock a file while it is edited. Give me the BunkerWeb settings and everything that needs special care, on the BunkerWeb side and on the Nextcloud side. This is the nginx server block in front of it now:

    server {
        listen 443 ssl http2;
        server_name cloud.example.com;
        ssl_certificate     /etc/letsencrypt/live/cloud.example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/cloud.example.com/privkey.pem;
        client_max_body_size 10G;
        proxy_request_buffering off;
        add_header Strict-Transport-Security "max-age=15552000; includeSubDomains" always;
        location / {
            proxy_pass http://nextcloud:80;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 3600s;
        }
        location = /.well-known/carddav { return 301 /remote.php/dav; }
        location = /.well-known/caldav  { return 301 /remote.php/dav; }
    }
