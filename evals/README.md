# Evals

Behaviour checks for the skills, run with `claude plugin eval`. The original cases were run against Claude Code 2.1.289 on 2026-10-05; the 13-skill layout was run against 2.1.296 on 2026-10-13 (activation at `--runs 5`, value at `--runs 3`); five strict cases were then split into parts of at most three conditions and the activation gate re-run on the final text. Copy the formats below as written; do not rediscover them.

## Layout

One directory per case, named `<skill-prefix>-<scenario>`. The prefixes are `router` (the `bunkerweb` skill), `troubleshooting`, `crs` and `migrate`. The `migrate` cases cover the source configs (`migrate-nginx-conf`, `migrate-nginx-proxy-manager`, `migrate-traefik-labels`, `migrate-apache-vhost`, `migrate-haproxy-cfg`) and one `migrate-app-<app>` case per app note that was run live (`authentik`, `home-assistant`, `nextcloud`, `vaultwarden`, `wordpress`). Name dedicated-source cases `migrate-<source>-<scenario>`; append `-part-<n>` when splitting a long case. App notes use `migrate-app-<app>`, and the migration router uses `migrate-fallback-<source>`. Keep unrelated prompts in `-negative` cases.

```text
evals/<case>/
  prompt.md
  graders/
    criteria.md     # llm grader, weight 2 (weight 1 on a negative case)
    fired.md        # positive cases only
    not-fired.md    # negative cases, and sibling exclusion on source cases
```

A positive case is a prompt the skill must fire on. A negative case is an unrelated prompt on which no BunkerWeb skill may fire.

## `prompt.md`

```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

<the user prompt>
```

## Graders

`criteria.md` scores correctness. Number the conditions and say "Score 1 only if ALL hold". Limit each case to six numbered conditions. Split longer cases into `-part-<n>` directories, keeping every condition word for word and copying the same prompt, `fired.md` and any `not-fired.md`. Run a new baseline for every split case before the full gates.

```markdown
---
type: llm
weight: 2
---

Score 1 only if ALL hold:
1. ...
```

`fired.md` checks that the skill was invoked. Put it in every positive case:

```markdown
---
type: tool_used
name: fired
tool: Skill
input_match: bunkerweb-modsecurity-crs-tuning
weight: 1
---

The agent invoked the bunkerweb-modsecurity-crs-tuning skill.
```

`not-fired.md` checks that no BunkerWeb skill was invoked. Put it in every negative case:

```markdown
---
type: tool_used
name: not-fired
tool: Skill
input_match: bunkerweb
min: 0
max: 0
weight: 1
---

No BunkerWeb skill was invoked.
```

Dedicated-source positive cases also carry a sibling `not-fired.md`: keep `min: 0` and `max: 0`, and match the sibling skill names with regex alternation. For an nginx case, use `input_match: '"bunkerweb:bunkerweb-migrate-(nginx-proxy-manager|swag|ingress-nginx)"'`. Copy the same sibling grader to each split case; exclude the intended source skill from its alternation.

The `tool_used` keys are `type`, `name`, `tool`, `input_match`, `min`, `max`, `weight` (default 1) and `arm`. Unknown keys are rejected. `min` defaults to 1, so a "did not fire" grader needs both `min: 0` and `max: 0`. Leave `arm` unset.

## What `input_match` matches against

`input_match` is a regular expression searched (not anchored) in the JSON text of the tool input. For a skill call the recorded input is namespaced by the plugin name:

```json
{"skill": "bunkerweb:bunkerweb-modsecurity-crs-tuning"}
```

Results on `crs-scoped-exclusion`, each from a trace in which the Skill call above was recorded:

| `input_match`                                      | Fired grader | Reading                                        |
| -------------------------------------------------- | ------------ | ---------------------------------------------- |
| `bunkerweb-modsecurity-crs-tuning`                 | 1x, passed   | Substring match. Fine for a unique name.       |
| `^bunkerweb-modsecurity-crs-tuning$`               | 0x, failed   | Anchors never match: the text starts with `{`. |
| `'"bunkerweb-modsecurity-crs-tuning"'`             | 0x, failed   | The closing quote is there, the opening one is not: the name follows `bunkerweb:`. |
| `^bunkerweb:bunkerweb-modsecurity-crs-tuning$`     | 0x, failed   | Same anchor problem, namespace or not.         |
| `'"bunkerweb:bunkerweb-modsecurity-crs-tuning"'`   | 1x, passed   | Quote-delimited and namespaced: an exact match. |

To match one skill name exactly, wrap the namespaced name in double quotes, and quote the whole YAML value in single quotes. For the router skill use `'"bunkerweb:bunkerweb"'`; the bare `bunkerweb` also matches every other skill, because `bunkerweb` is a prefix of all of them. A skill called without the plugin prefix would not match the namespaced form; every run recorded here used the prefix.

## Firing counts in the score only without a baseline

Under the default `--ablation with-without`, `tool_used: Skill` graders are indicators outside the score (the report marks them `scored: false`). The baseline arm can never load our skills, so counting them would give every skill a free improvement. Two gates follow from that.

- **Activation gate**: `--ablation none`. There is no baseline arm, so `fired` and `not-fired` count. With `criteria` at weight 2 and `fired` at weight 1, a run in which the skill did not fire scores at most 0.67.
- **Value gate**: the default `with-without`. The with-minus-without delta comes from the correctness graders alone.

Score-drop check, with the skill directory moved out of `skills/` and the case `crs-scoped-exclusion`:

```text
claude plugin eval . --case crs-scoped-exclusion --ablation none --runs 1 --threshold 0.8 --no-publish --trust-plugin --model sonnet --max-cost-usd 3; echo rc=$?
  criteria  PASS PASS FAIL (judge majority: pass)   weight 2
  fired     Skill called 0x (expected 1..∞)         weight 1
  score 0.667 (below 0.8)
rc=1
```

With the skill present the same case scores 1 and exits 0. `min: 0` with `max: 0` is accepted: `crs-negative` scores 1 on `not-fired` when the skill is present but not invoked, and a `not-fired` grader added to a positive case scores 0 ("Skill called 1x (expected 0..0)") and fails the run.

## Commands

Development, one run per arm, one case at a time while writing it:

```bash
claude plugin eval . --case 'crs-*' --runs 1 --no-publish --trust-plugin --model sonnet --max-cost-usd 3
```

Both gates grade with the `sonnet` judge (the default is `haiku`). With about 25 cases the cost caps below are $35 for the activation gate and $70 for the value gate, at three runs per case.

Activation gate. Passes when every case scores at least 0.8 (exit code 0):

```bash
claude plugin eval . --ablation none --runs 3 --threshold 0.8 --no-publish --trust-plugin --model sonnet --judge-model sonnet --max-cost-usd 35
```

Value gate (default `with-without`). Passes when, for each skill, the mean with-minus-without delta over its positive cases is above 0:

```bash
claude plugin eval . --runs 3 --no-publish --trust-plugin --model sonnet --judge-model sonnet --max-cost-usd 70
```

`claude plugin eval` honours only the last `--case`, so several `--case` flags silently run one glob. Bracket globs such as `[ns]` match nothing. Run one command per glob.

Add `--json <file>` to keep the per-run scores. Add `--keep-temp` to keep the run's trace; the kept directory is sealed, so run the `chmod 700` command the runner prints before reading `out/trace.jsonl`. Results land in `evals/results/`, which git ignores.

## Rules

- Verify every criterion at the BunkerWeb release in `BUNKERWEB_REF` before it goes into a grader. Record the source path in the change. A criterion that is wrong at the pin fails correct answers.
- Run a new case without the skill first. A case the baseline already passes proves nothing about the skill; expect the `without` arm to score lower under `with-without`.
- **Split a case whose combined grader fails while every criterion passes on its own.** A "Score 1 only if ALL hold" grader with many conditions is stricter than the same conditions graded one by one. When the per-criterion run passes every condition and the combined run still scores below the threshold, split the case into parts of at most three conditions. Keep every condition word for word and copy the prompt, `fired.md` and `not-fired.md` byte for byte. Name the parts `<case>-a`, `<case>-b` (`<case>-part-1a`, `<case>-part-1b` for a case already named `-part-1`). Check the split mechanically: the parts' conditions, concatenated, equal the original's.
- A judge is a model and votes can split. Treat a case that flips between runs as a case to tighten, not as noise. To find the criterion that flips, run one grader per criterion on that case. Fix the skill text, or tighten the criterion's wording to what a live run proved. Never weaken a criterion to make it pass, and never delete one.
- The skill reads its files and must deliver the whole answer in its last message: the `llm` grader sees the last message only. Each `SKILL.md` carries that rule.
