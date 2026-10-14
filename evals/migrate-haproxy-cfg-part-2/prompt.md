---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Convert this HAProxy config to BunkerWeb 1.6.15 (Docker, multisite) for shop.example.com:

    defaults
        mode http
        option forwardfor
        timeout connect 5s
        timeout client 30s
        timeout server 30s
        timeout tunnel 1h

    frontend fe
        bind :80
        bind :443 ssl crt /etc/haproxy/certs/shop.pem
        http-request redirect scheme https unless { ssl_fc }
        acl host_shop hdr(host) -i shop.example.com
        acl is_admin path_beg /admin
        acl admin_net src 10.0.0.0/8
        acl too_big req.hdr_val(content-length) gt 20971520
        http-request deny deny_status 413 if too_big
        http-request deny deny_status 403 if is_admin !admin_net
        http-request track-sc0 src table login_rate if { path /login }
        http-request deny deny_status 429 if { path /login } { sc_http_req_rate(0) gt 10 }
        http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains"
        use_backend be_ws if host_shop { path_beg /socket }
        use_backend be_app if host_shop

    backend be_app
        server app app:3000

    backend be_ws
        server app app:3000

    backend login_rate
        stick-table type ip size 100k expire 1m store http_req_rate(10s)
