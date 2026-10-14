---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

My WordPress runs in Docker behind nginx. I want to move it behind BunkerWeb 1.6.15 and keep the same behaviour. The site is blog.example.org. Here is the nginx server block:

    server {
        listen 443 ssl http2;
        server_name blog.example.org;
        client_max_body_size 64m;
        location / {
            proxy_pass http://wordpress:80;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

The editors use the block editor and the old Media > Add New uploader, with videos of about 30 MB. A mobile app talks to /wp-json with PUT and DELETE and uploads photos straight to /wp-json/wp/v2/media with each photo's own content type (image/jpeg). Give me the BunkerWeb settings and say what to watch for when I switch from nginx.
