---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I self-host Vaultwarden behind nginx on one Docker host and want to move it to BunkerWeb 1.6.15 (Docker). Family members use the web vault and the browser extension, sync over the live notification socket, attach files of up to 25 MB and import big exports from other password managers. Give me the BunkerWeb settings and everything that needs special care before I turn on blocking: which defaults will break it, which OWASP CRS rule ids I should expect in the log, and the exclusion that goes with them. This is the nginx server block in front of it now:

    server {
        listen 443 ssl http2;
        server_name vault.example.com;
        ssl_certificate     /etc/letsencrypt/live/vault.example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/vault.example.com/privkey.pem;
        client_max_body_size 525M;
        location / {
            proxy_pass http://vaultwarden:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        location /notifications/hub {
            proxy_pass http://vaultwarden:80;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
