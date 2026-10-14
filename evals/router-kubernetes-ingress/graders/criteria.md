---
type: llm
weight: 2
---

Score 1 only if ALL hold:

1. Installs BunkerWeb with the official Helm chart: `helm repo add bunkerweb https://repo.bunkerweb.io/charts` and the chart `bunkerweb/bunkerweb`, with `--version 1.1.0`, the chart release whose appVersion is BunkerWeb 1.6.15. A bare `helm install` without `--version`, or a different chart version, FAILS.
2. The Ingress sets `ingressClassName: bunkerweb`, routes host `shop.example.com` to Service `shop` port 80, and is `networking.k8s.io/v1`.
3. The antibot setting is an annotation on the Ingress (not a label, not an env var, not a ConfigMap, not a Helm value) whose key starts with `bunkerweb.io/` and is scoped to the host: `bunkerweb.io/shop.example.com_USE_ANTIBOT`. The unprefixed `bunkerweb.io/USE_ANTIBOT` is acceptable only if the answer says it applies to every host of that Ingress and the Ingress carries only shop.example.com.
4. The setting is `USE_ANTIBOT` and the value is `captcha`, quoted as a YAML string. `ANTIBOT`, `USE_CAPTCHA`, `ANTIBOT_MODE`, `recaptcha`, `hcaptcha` or `javascript` for the requested "captcha" FAIL.
5. Sets the chart value `settings.kubernetes.ingressClass` to `bunkerweb`, or says that with that value empty the BunkerWeb 1.6.15 controller processes Ingresses of every class (so it would also pick up another controller's Ingresses).
6. Tells the user to replace the chart's default passwords (`changeme` for MariaDB, Redis and the UI admin), by value or through `settings.existingSecret`.
