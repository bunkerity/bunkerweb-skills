# Summary

- <!-- What does this skill teach, and what does the agent get wrong without it? -->

# Verification

- [ ] `python3 scripts/validate.py`
- [ ] `python3 scripts/check_scan_hygiene.py`
- [ ] `python3 scripts/check_settings.py --bunkerweb .bunkerweb`
- [ ] Eval cases added or updated, run with and without the skill (`claude plugin eval . --runs 1 --no-publish --trust-plugin`)
- [ ] Every setting, label, annotation, command and log signature was checked against the BunkerWeb source at the tag in `BUNKERWEB_REF`
- [ ] Other (add details below)

<details>
<summary>Verification details</summary>

- <!-- Source paths checked at BUNKERWEB_REF, and the eval result with and without the skill -->

</details>

# Checklist

- [ ] I installed the pre-commit hooks and ran `pre-commit run --all-files`.
- [ ] The directory name and the frontmatter `name` agree, and the skill is in the `README.md` table.
- [ ] The `description` reads as a trigger and names concrete situations or paths.
- [ ] Long reference material lives in `references/`, not inline in `SKILL.md`.
- [ ] Nothing is copied from the BunkerWeb documentation or the template hub; I linked instead.
- [ ] No secrets, credentials, customer hostnames, or IPs are included.
- [ ] I added a line under `## Unreleased` in `CHANGELOG.md`, formatted `- [@handle] Description`.
- [ ] I linked related issues or discussions and added context for reviewers.
