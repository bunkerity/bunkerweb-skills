---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Convert this Apache httpd vhost to BunkerWeb 1.6.15 (Docker, multisite) for app.example.com:

    <VirtualHost *:443>
        ServerName app.example.com
        SSLEngine on
        SSLCertificateFile /etc/ssl/app.crt
        SSLCertificateKeyFile /etc/ssl/app.key
        LimitRequestBody 20971520
        Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
        RewriteEngine On
        RewriteRule "^/old/?$" "https://app.example.com/new" [R=301,L]
        <Location "/admin">
            Require ip 10.0.0.0/8
        </Location>
        ProxyPreserveHost On
        ProxyPass "/ws" "ws://app:3000/ws"
        ProxyPass "/" "http://app:3000/"
        ProxyPassReverse "/" "http://app:3000/"
    </VirtualHost>
