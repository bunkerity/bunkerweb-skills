# Plumber

CI/CD security scanning for the GitHub Actions workflows in this repository.
[Plumber](https://getplumber.io) statically analyses `.github/workflows/` for
supply-chain and pipeline misconfigurations: unpinned or unvetted actions,
`secrets: inherit`, missing `permissions:` blocks, dangerous triggers,
template injection, cache poisoning and branch protection gaps.

This repository ships no runtime code, only Markdown skills, eval cases and a
few stdlib-only Python checks, so the workflows that validate and scan it are
the whole pipeline Plumber has to cover. It complements CodeQL (the Python
scripts and the workflows themselves) and OpenSSF Scorecard (repository
hygiene); none of the three overlaps with the others.

## Files

| Path | Purpose |
|---|---|
| `.github/plumber/plumber.yaml` | Policy overlay on top of `plumber:default` |
| `.github/plumber/README.md` | This file |
| `.github/workflows/plumber.yml` | Reusable workflow invoked by `validate.yml`, also run weekly |

## Running it locally

```bash
brew install getplumber/tap/plumber        # or download the binary from the releases page
GH_TOKEN=$(gh auth token) plumber analyze --config .github/plumber/plumber.yaml --score
plumber explain ISSUE-713                  # details for a given issue code
```

`plumber analyze` scans the local workflows and queries the GitHub API for
branch protection. That last control needs a token with `Administration: read`;
without it, protection findings are incomplete rather than wrong.

## Policy

`plumber.yaml` extends `plumber:default` and adds nothing. The only third-party
actions in the workflows are `getplumber/plumber` and `ossf/scorecard-action`,
and the default allowlist already trusts both. Add an exact `owner/repo`
under `trustedGithubActions` rather than an owner wildcard when a workflow
starts using another third-party action, so trust cannot spread to other or
future repositories under that account. Every action is pinned by commit SHA,
and Dependabot bumps those pins weekly.

## Gating

`validate.yml` calls the reusable workflow as its own `plumber` job, and the
reusable workflow also runs every Monday. It is gated at `min-score: B` with
`soft-fail: false`, so scores of C, D or E fail the run. Results land in the
Code Scanning tab.

On pull requests the scan still runs and gates the PR, but `upload-sarif` and
`score-push` are off: a PR run sends nothing to Code Scanning and publishes no
score. The run-scoped `plumber-report` artifact is still uploaded and stays
attached to the run.

Every input is set explicitly in `plumber.yml`, including those that match the
action's own defaults, so that an auditor reads the effective configuration
from the workflow alone and never has to diff it against `action.yml` at some
past tag. `verify-attestation: true` keeps the sigstore/SLSA provenance check
on the downloaded binary; `score-push: true` publishes the score used by the
hosted badge service.

Every job in every workflow declares its own `permissions:` block. Keep it
that way: Plumber scores jobs that inherit event-dependent grants lower, and
splitting CI into a per-event caller plus a reusable workflow is what causes
it. A same-repo PR run therefore still holds `security-events: write`, and the
`plumber` job also holds `id-token: write` for the OIDC identity behind
`score-push`. YAML permissions cannot depend on the event; the upload steps
are what is gated.

Each run uploads a `plumber-report` artifact holding the JSON report, the
PBOM, the CycloneDX SBOM and the raw SARIF (`upload-artifacts: true`). The
SARIF is redundant with Code Scanning; the PBOM and SBOM are kept as
per-run evidence of what the pipeline consumed.

The published score is rendered in the repository README as
`https://score.getplumber.io/github.com/bunkerity/bunkerweb-skills.svg`; it
reads `unknown` until a run with `score-push: true` has landed on the default
branch.
