---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Says that in the 1.6 Docker integration the scheduler container (`bunkerweb-scheduler`, often named `bw-scheduler`) reads the settings and pushes the generated configuration to the `bunkerweb` container, so a setting placed on the `bunkerweb` container is never read.
2. Points out that under `MULTISITE=yes` a setting without the `app.example.com_` prefix is the global value for every service, so even on the scheduler it would also protect `api.example.com`, not only `app.example.com`.
3. Gives the corrected setting `app.example.com_USE_ANTIBOT=captcha` and puts it on the scheduler container, not on `bunkerweb`. It does not invent a different prefix form (`app_USE_ANTIBOT`, `APP.EXAMPLE.COM_USE_ANTIBOT`, `USE_ANTIBOT_app.example.com`) and does not put a `bunkerweb.` prefix on a plain env var.
4. Says how to confirm it applied: scheduler logs showing the configuration generated and the instance reloaded, and a request to `app.example.com` redirecting to the antibot challenge page (default path `/challenge`) while `api.example.com` serves normally.
5. Names the scheduler log line that exposes a dropped setting: a mistyped name, an invalid value, or a prefix that is not listed in `SERVER_NAME` is discarded with a warning starting `Ignoring variable <name> :`, so the user can search the scheduler log for `Ignoring variable`. The prefix only matches a host that appears in `SERVER_NAME`.
