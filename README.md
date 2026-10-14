<p align="center">
	<img alt="BunkerWeb logo" src="https://github.com/bunkerity/bunkerweb/raw/master/misc/logo.png" height=100 width=350 />
</p>

<p align="center">
	<a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs welcome" /></a>
	<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT license" /></a>
	<br />
	<a href="https://github.com/bunkerity/bunkerweb-skills/blob/main/.github/plumber/README.md"><img src="https://score.getplumber.io/github.com/bunkerity/bunkerweb-skills.svg" alt="Plumber CI/CD security score" /></a>
	<a href="https://scorecard.dev/viewer/?uri=github.com/bunkerity/bunkerweb-skills"><img src="https://api.scorecard.dev/projects/github.com/bunkerity/bunkerweb-skills/badge" alt="OpenSSF Scorecard" /></a>
	<a href="https://github.com/bunkerity/bunkerweb-skills/actions/workflows/codeql.yml"><img src="https://github.com/bunkerity/bunkerweb-skills/actions/workflows/codeql.yml/badge.svg" alt="CodeQL" /></a>
</p>

<p align="center">
	🌐 <a href="https://www.bunkerweb.io/?utm_campaign=self&utm_source=github">Website</a>
	 &#124;
	📓 <a href="https://docs.bunkerweb.io/?utm_campaign=self&utm_source=github">Documentation</a>
	 &#124;
	🧩 <a href="https://github.com/bunkerity/bunkerweb-plugins">Plugins</a>
	 &#124;
	🗂️ <a href="https://github.com/bunkerity/bunkerweb-templates">Templates</a>
</p>

> 🤖 Official [BunkerWeb](https://github.com/bunkerity/bunkerweb) skills for AI coding agents: deploy it, troubleshoot it, tune its WAF, and migrate to it.

A skill is a folder of Markdown that teaches an AI coding agent one job: the settings, the traps and the commands that are known to work. The agent reads each skill's `description`, loads the skill when your request matches, and follows it. You memorise no slash command and paste no context.

Every setting, label, command and log line in these skills was checked against the BunkerWeb source, and every app note was run against a live stack.

## Installation

Any agent that supports [skills.sh](https://skills.sh):

```bash
npx skills add bunkerity/bunkerweb-skills
```

Claude Code, as a plugin:

```text
/plugin marketplace add bunkerity/bunkerweb-skills
/plugin install bunkerweb@bunkerweb
```

One skill only:

```bash
npx skills add bunkerity/bunkerweb-skills --skill bunkerweb-migrate-nginx
```

## Skills

| Skill | The agent loads it when you are |
| --- | --- |
| [`bunkerweb`](skills/bunkerweb/) | Installing, configuring or upgrading BunkerWeb on Docker, autoconf, Kubernetes, Linux or all-in-one; 21 live-tested app notes. |
| [`bunkerweb-troubleshooting`](skills/bunkerweb-troubleshooting/) | Diagnosing blocks, bans, upstream errors, certificate failures, ignored settings or failed reloads. |
| [`bunkerweb-modsecurity-crs-tuning`](skills/bunkerweb-modsecurity-crs-tuning/) | Tuning ModSecurity and OWASP CRS, writing scoped exclusions or checking custom-config loading. |
| [`bunkerweb-migrate`](skills/bunkerweb-migrate/) | Migrating an unsupported source or a mixed estate, and routing supported sources to their dedicated skills. |
| [`bunkerweb-migrate-nginx`](skills/bunkerweb-migrate-nginx/) | Converting hand-written nginx server and location blocks to BunkerWeb settings. |
| [`bunkerweb-migrate-nginx-proxy-manager`](skills/bunkerweb-migrate-nginx-proxy-manager/) | Moving NPM proxy hosts, access lists, custom locations and certificates. |
| [`bunkerweb-migrate-swag`](skills/bunkerweb-migrate-swag/) | Moving SWAG proxy-confs, certificate settings and fail2ban jails. |
| [`bunkerweb-migrate-ingress-nginx`](skills/bunkerweb-migrate-ingress-nginx/) | Converting ingress-nginx Ingress annotations and running both Kubernetes controllers side by side. |
| [`bunkerweb-migrate-traefik`](skills/bunkerweb-migrate-traefik/) | Moving Traefik Docker labels or file-provider routers, services and middlewares to BunkerWeb autoconf labels. |
| [`bunkerweb-migrate-caddy`](skills/bunkerweb-migrate-caddy/) | Moving Caddyfile reverse proxies, handle paths, headers, basic auth and automatic HTTPS. |
| [`bunkerweb-migrate-apache`](skills/bunkerweb-migrate-apache/) | Moving Apache httpd VirtualHosts, proxy directives, rewrites and access rules. |
| [`bunkerweb-migrate-haproxy`](skills/bunkerweb-migrate-haproxy/) | Moving HAProxy HTTP and TCP frontends, ACLs, timeouts, stick-table limits and certificates. |
| [`bunkerweb-migrate-modsecurity`](skills/bunkerweb-migrate-modsecurity/) | Moving standalone ModSecurity rules, CRS configuration and exclusions, then comparing logged rule IDs. |

## Target release

The skills target BunkerWeb 1.6.x and were verified at the tag in [`BUNKERWEB_REF`](BUNKERWEB_REF), currently `v1.6.15`. Each skill says so, and tells the agent to re-check a setting before it relies on another release. On 1.5 or on a 1.7 release candidate the skills warn instead of guessing.

## Related

- [`bunkerweb-mcp`](https://github.com/bunkerity/bunkerweb-mcp): live actions on a running instance (bans, settings, the API).
- [`bunkerweb-helm`](https://github.com/bunkerity/bunkerweb-helm): the Helm chart for Kubernetes.
- [`terraform-provider-bunkerweb`](https://github.com/bunkerity/terraform-provider-bunkerweb): BunkerWeb as code.
- [`bunkerweb-templates`](https://github.com/bunkerity/bunkerweb-templates): ready-made service templates.
- [BunkerWeb documentation](https://docs.bunkerweb.io/).

## Contributing

Fixes and new skills are welcome, from a one-line correction to a whole app note. Read [CONTRIBUTING.md](CONTRIBUTING.md) first, and the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

A skill that makes an agent run an unsafe command or weaken a protection is a security issue. Follow the [security policy](SECURITY.md) and do not open a public issue.

## Licence

[MIT](LICENSE). The skills link to the BunkerWeb documentation and the template hub instead of copying them.
