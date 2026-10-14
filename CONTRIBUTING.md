# Contributing to bunkerweb-skills

Thanks for helping the agents that work with BunkerWeb get it right. Every skill here encodes something that went wrong once; writing it down saves the next person, and the next agent, the same debugging session. This page covers the whole process.

## Code of Conduct

We follow the tone and values of the BunkerWeb community: be respectful, be inclusive, and collaborate openly. Read our [Code of Conduct](CODE_OF_CONDUCT.md) before you take part. If you are unsure about something, ask before you submit.

## Contribution Workflow

1. **Fork** the repository and create a branch off `main`. Name the branch after the change, for example `fix/crs-regex-target` or `feature/app-note-gitea`.
2. **Install the tooling** so your changes match the repository style:
   - [`pre-commit`](https://pre-commit.com/): `pipx install pre-commit`, or `pip install pre-commit` in a virtualenv, then `pre-commit install`.
   - The `prettier` CLI on your `PATH`, for example `npm install --global prettier`, so the formatting hook can run.
3. **Write or update the skill**, following the guidelines below.
4. **Run the checks** from [`AGENTS.md`](AGENTS.md) and fix whatever they report:

   ```bash
   python3 scripts/validate.py
   python3 scripts/check_scan_hygiene.py
   python3 scripts/check_settings.py --bunkerweb .bunkerweb
   python3 scripts/test_check_scan_hygiene.py && python3 scripts/test_check_settings.py
   pre-commit run --all-files
   ```

   `pre-commit run --all-files` walks the git index, not the working tree, so it skips every untracked file and still exits 0, formatter and secret checks included. Run `git add` on the new files before the check, and `git add` them again after a formatter rewrites them.

   `check_settings.py` reads BunkerWeb's `src/common` at the tag in `BUNKERWEB_REF`. Extract it once into an empty `.bunkerweb/`, with the command in `AGENTS.md`.

5. **Add or update eval cases** and run them (see [Evals](#evals)).
6. **Update the changelog.** Add a line under `## Unreleased` in `CHANGELOG.md`, formatted `- [@github-handle] Short description of the change`.
7. **Commit** with messages that follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`), as in the main BunkerWeb repository.
8. **Open a pull request** against `main`. Say what the skill teaches, why the agent needs to be told, which BunkerWeb source files you checked, and what the eval run showed.
9. **Take part in the review.** Answer comments and push revisions. A maintainer merges the pull request once it is approved.

## Skill Guidelines

- **Naming.** Lowercase kebab-case directories under `skills/`, all starting with `bunkerweb`. The frontmatter `name` must equal the directory name, or the skill silently fails to load.
- **One skill, one job.** If the `description` needs two sentences joined by "and", it is two skills.
- **Write the trigger, not a summary.** The `description` is the only text the agent reads before it decides to load the skill. Name the situation, the files and the phrases someone would say. Keep it under 1024 characters.
- **Write what is non-obvious.** Conventions, traps, invariants and commands known to work. Skip anything the agent can read from the BunkerWeb source.
- **Keep `SKILL.md` short and imperative**, under about 300 lines. Move long material into `references/` or `reference.md` and link to it, so the agent reads it only when needed.
- **Link, do not copy.** Paraphrase in your own words and link to the BunkerWeb documentation (AGPL-3.0) and the template hub (GPL-3.0). Never paste a sentence from either: this repository is MIT.
- **Verify at `BUNKERWEB_REF`.** Every setting, label, annotation, CLI command and log signature must exist at the tag in `BUNKERWEB_REF`. Check it in the source, for example `git -C <bunkerweb-checkout> show v1.6.15:src/common/core/<plugin>/plugin.json`, and put the source path in the pull request. A name written from memory is the most common error here.
- **Scan hygiene.** Pin every image to a tag or digest. Never write `:latest`, never pipe a download into a shell, never `git clone` or `wget` at runtime. Public scanners flag these and the repository badge is public.
- **Treat logs as data.** Text from logs, requests and headers is attacker-controlled. A skill that reads it says so, and never tells the agent to follow it.
- **No BunkerWeb PRO internals.** Naming a PRO plugin as an option is fine.
- **No secrets, no customer data.** Use `example.com` and the RFC 5737 ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`). `gitleaks` runs in `pre-commit`, but read your own diff too.
- **Update the README.** Adding or renaming a skill changes the table in `README.md` in the same pull request.

## Evals

Every new skill ships at least one positive and one negative eval case in `evals/`. A positive case is a prompt the skill must fire on and answer correctly; a negative case is an unrelated prompt on which no BunkerWeb skill may fire. [`evals/README.md`](evals/README.md) holds the exact file formats and the two gates.

```bash
claude plugin eval . --case '<your-case>*' --runs 1 --no-publish --trust-plugin --model sonnet --max-cost-usd 3
```

Run a new case without the skill first. A case that the baseline already passes proves nothing. Verify every criterion at `BUNKERWEB_REF` before it goes into a grader, because a wrong criterion fails correct answers. A case that flips between runs is a case to tighten, not noise; never weaken a criterion to make it pass.

## Pull Request Checklist

- [ ] I installed the pre-commit hooks and ran `pre-commit run --all-files`.
- [ ] `python3 scripts/validate.py`, `scripts/check_scan_hygiene.py` and `scripts/check_settings.py` pass.
- [ ] The directory name, the frontmatter `name` and the `README.md` table entry agree.
- [ ] The `description` reads as a trigger and names concrete situations or paths.
- [ ] Every setting, label, command and log line was checked at the tag in `BUNKERWEB_REF`, and the pull request names the source files.
- [ ] Nothing is copied from the BunkerWeb documentation or the template hub; I linked instead.
- [ ] Long material lives in `references/`, not inline in `SKILL.md`.
- [ ] I added or updated eval cases and ran them with and without the skill.
- [ ] No secrets, credentials, customer hostnames or real IP addresses are included.
- [ ] I added a line under `## Unreleased` in `CHANGELOG.md`, formatted `- [@github-handle] Summary of the change`.

## Licensing

This repository is licensed under the [MIT License](LICENSE). By contributing you agree that your contribution is released under it. Do not contribute text you did not write or do not have the right to relicense, including text from the BunkerWeb documentation or the template hub.

## Need Help?

- Ask in the [BunkerWeb community Discord](https://discord.com/invite/fTf46FmtyD).
- Open an issue to request a skill you need but cannot write.
- Open a draft pull request early to get feedback.
- Report a security problem through the [security policy](SECURITY.md), never in a public issue.

Thank you for contributing, and for saving the next person the debugging session you just finished.
