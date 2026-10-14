# Changelog

All notable updates to the skill collection live here. Keep the newest entries at the top.

## Unreleased

- [@TheophileDiot] Name the JSON-body target the log shows instead of a wildcard in the Vaultwarden note, ask its answers for a one-line exclusion scope, and move the certificate condition of the Vaultwarden eval into its own case.
- [@TheophileDiot] Point the nginx migration skill at the per-app notes, give the authentik and Vaultwarden notes answer checklists (error bodies, methods, the `413` limit, the detect-first order with the ban reason), and require ModSecurity custom configs to be written out with their path and full text.

- [@TheophileDiot] Correct migration guidance for private-key permissions, gRPC TLS and WAF coverage, CRS rule placement, and eval-case splitting.

- [@TheophileDiot] Split five strict eval cases into parts of at most three conditions, name the scheduler's real `Generating and sending the configuration before running jobs ...` log line in the troubleshooting skill, add the nginx fixed-host-path and Nextcloud detect-first sentences, and record the `claude plugin eval --case` limits in `evals/README.md`.

- [@TheophileDiot] Tighten skill text after the 13-skill eval gates: label every block in the 1.7 branch, state the 413 upload limit for authentik, the fixed-host-path rule for NPM and nginx, the detect-first order for Vaultwarden and the Nextcloud trust settings, and route "setting added, nothing changed" to troubleshooting.

- [@TheophileDiot] Verify the regex prefix-strip form live for Caddy, nginx, NPM and SWAG, and the rewrite bypass matrix; correct the NPM prefix regex and document the bare-path, lookalike and encoded-slash limits.

- [@TheophileDiot] Replace URI rewrite migration includes with regex-and-capture proxy mappings, explain the Lua access-check bypass, preserve live-test caveats, and update migration graders and troubleshooting.

- [@TheophileDiot] Split migration guidance into 13 operator skills, record live parity tests for every migration source, split long eval cases into groups of at most six conditions, and clarify single-site ModSecurity paths, Kubernetes reload traps and authentik uploads.

- [@TheophileDiot] Initial public release: `bunkerweb`, `bunkerweb-troubleshooting`, `bunkerweb-modsecurity-crs-tuning`, `bunkerweb-migrate`, verified against BunkerWeb v1.6.15, with live-tested notes for 21 self-hosted apps, migration from nginx, Nginx Proxy Manager, Traefik, Caddy, Apache httpd, HAProxy and standalone ModSecurity, CI gates for manifests, scanner hygiene and setting names, and a `claude plugin eval` suite.
