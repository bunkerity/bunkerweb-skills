# Security policy

This repository ships instructions that AI coding agents execute against BunkerWeb deployments. A skill that tells an agent to run the wrong command, weaken a protection, or trust attacker-controlled input is a security issue here, even though no BunkerWeb runtime code lives in this repository.

## Responsible disclosure

If you have found a security bug, please send us an email at security \[@\] bunkerity.com (using a ProtonMail if possible) with technical details so we can resolve it as soon as possible.

Here is a non-exhaustive list of issues we consider as high risk :

- A skill that instructs an agent to run a destructive, exfiltrating, or otherwise unsafe command
- A skill that leads an agent to disable or weaken a BunkerWeb protection beyond what the user asked for
- A prompt-injection payload embedded in a skill, reference file, or eval case
- Credentials, tokens, or real hostnames committed anywhere in the repository
- Risk in the supply chain, including the pinned pre-commit hooks and GitHub Actions

Please do not open a public issue for any of the above.

## Scope

This policy covers the skills, evals and scripts in this repository. Vulnerabilities in BunkerWeb itself belong in the [main project's policy](https://github.com/bunkerity/bunkerweb/blob/master/SECURITY.md), which carries the bounty programme.
