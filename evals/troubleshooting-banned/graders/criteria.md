---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Names the bad behavior module (`USE_BAD_BEHAVIOR`), which counts "bad" HTTP status codes per IP in a time window and bans the IP once a threshold is reached, as the likely cause, and connects it to the 404s from the broken image links (404 is in the default `BAD_BEHAVIOR_STATUS_CODES`).
2. Gives a correct v1.6.15 way to unban: `bwcli unban <ip>` run inside the scheduler container (for example `docker exec <scheduler-container> bwcli unban <ip>`), or the Bans page of the web UI, or the API `POST /bans/unban`. A made-up command (`bunkerweb unban`, `bwcli ban remove`, editing a ban file, `docker restart` as the unban) FAILS, and so does a double-dash `--service`: the per-service flag of `bwcli unban` is spelled `-service <name>`.
3. Fixes the root cause rather than disabling every protection: repair or stop requesting the broken links, or tune the module (remove 404 from `BAD_BEHAVIOR_STATUS_CODES`, raise `BAD_BEHAVIOR_THRESHOLD`, lower `BAD_BEHAVIOR_COUNT_TIME` or `BAD_BEHAVIOR_BAN_TIME`). Setting `USE_BAD_BEHAVIOR=no` is acceptable only as a last resort stated with its cost, and turning off BunkerWeb or other protections FAILS. When it says where tuned settings go in the Docker integration, that is the scheduler container, not the `bunkerweb` container.
4. Every BunkerWeb setting name it uses exists at v1.6.15: `USE_BAD_BEHAVIOR`, `BAD_BEHAVIOR_STATUS_CODES`, `BAD_BEHAVIOR_THRESHOLD`, `BAD_BEHAVIOR_COUNT_TIME`, `BAD_BEHAVIOR_BAN_TIME`, `BAD_BEHAVIOR_BAN_SCOPE`. An invented name (`BAD_BEHAVIOR_MAX_REQUESTS`, `BAD_BEHAVIOR_BAN_DURATION`, `BAD_BEHAVIOR_IGNORE_URI`) FAILS.
5. Shows how to confirm the cause: a log line saying the IP is banned with reason `bad behavior`, or the output of `bwcli bans`.
6. Says that BunkerWeb 1.6.15 has no dedicated "banned" page: a banned client receives the normal deny response (the 403 error page by default, a dropped connection when `DENY_HTTP_STATUS=444`). It therefore tells the user to confirm from the log or `bwcli bans` that the message really comes from a BunkerWeb ban. An answer that takes the quoted message as proof of a BunkerWeb ban FAILS.
7. States the unban scope: `bwcli unban <ip>` without `-service` removes the global ban and every service-scoped ban for that IP, while `-service <name>` removes only that service's ban.
