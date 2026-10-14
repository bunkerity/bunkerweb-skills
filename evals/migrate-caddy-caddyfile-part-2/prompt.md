---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Convert this Caddy 2.11 Caddyfile to BunkerWeb 1.6.15 (Docker, multisite) for app.example.com. Caddy gets its certificate by itself today, sits behind a load balancer on a private range, and I want to run both side by side before I switch:

    {
        servers {
            trusted_proxies static private_ranges
        }
    }

    app.example.com {
        encode gzip
        request_body {
            max_size 5MB
        }
        header Strict-Transport-Security "max-age=31536000; includeSubDomains"
        redir /old https://app.example.com/new 301

        basic_auth /secure* {
            alice $2a$14$q5Po7nxSMvRLDG8QAlEr0OJ5mYEj2bxNyAM0DiH5ZARlupMuqonQq
        }

        @admin_denied {
            path /admin /admin/*
            not client_ip 10.0.0.0/8
        }
        respond @admin_denied 403

        handle_path /api/* {
            reverse_proxy app:3000
        }
        reverse_proxy app:3000
    }
