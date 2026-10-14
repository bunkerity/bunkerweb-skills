#!/usr/bin/env python3
"""Fail on skill text that public skill scanners flag as an unverifiable external dependency.

Run: python3 scripts/check_scan_hygiene.py

Docker commands are recognised only on lines that start with `docker run` or `docker pull`
(optionally after `$`, `#`, `>` or `sudo`), so write commands in code, not in prose.
"""

import re
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGE_LINE_RE = re.compile(r"\bimage:\s*([^\s#]\S*)")
SPLIT_IMAGE_RE = re.compile(r"^(\s*)image:\s*(?:#.*)?$")
YAML_KEY_RE = re.compile(r"^(\s*)([\w-]+):\s*(.*)$")
# Unquoted YAML scalars that parse as null. A quoted "null" stays a literal string.
YAML_NULLS = {"", "~", "null", "Null", "NULL"}
DOCKER_COMMAND_RE = re.compile(r"^\s*(?:[$#>]\s*)?(?:sudo\s+)?docker\s+(?:run|pull)\b")
# Options of `docker run` / `docker pull` that take a separate value, so the value is not mistaken for the image.
VALUE_OPTIONS = {
    "-p", "--publish", "-v", "--volume", "-e", "--env", "--env-file", "--name", "--network", "--net", "-w", "--workdir",
    "--mount", "--restart", "--add-host", "-u", "--user", "--entrypoint", "-l", "--label", "--platform", "-h", "--hostname",
    "--cpus", "-m", "--memory", "--log-driver", "--log-opt", "--cap-add", "--cap-drop", "--device", "--dns", "--ulimit", "--tmpfs", "--pull",
    "--health-cmd", "--health-interval", "--health-retries", "--health-timeout", "--health-start-period", "--security-opt",
    "--sysctl", "--expose", "--shm-size", "--stop-signal", "--stop-timeout", "--group-add", "--ipc", "--pid", "--gpus",
}  # fmt: skip
# Options that take no value. Any other option, unless written --opt=value, makes the command unparsable here.
FLAG_OPTIONS = {
    "-d", "--detach", "-i", "--interactive", "-t", "--tty", "-it", "-ti", "-dit", "-itd", "--rm", "--privileged", "--init",
    "--read-only", "-P", "--publish-all", "--no-healthcheck", "-q", "--quiet", "-a", "--all-tags", "--disable-content-trust",
}  # fmt: skip
RULES = (
    ("pull-latest", re.compile(r":latest\b")),
    ("pipe-to-shell", re.compile(r"\|\s*(?:sudo\s+)?(?:ba|z)?sh\b")),
    ("runtime-clone", re.compile(r"\bgit\s+clone\b")),
    ("runtime-download", re.compile(r"\bwget\b")),
)


def pinned(image):
    """True when the image reference carries a tag or a digest."""
    last = image.strip("\"'").rsplit("/", 1)[-1]
    return ":" in last or "@" in last


def logical_lines(lines):
    """Yield (first_line_number, text) with backslash continuations joined."""
    start, parts = None, []
    for number, line in enumerate(lines, 1):
        start = start or number
        if line.rstrip().endswith("\\"):
            parts.append(line.rstrip()[:-1])
            continue
        parts.append(line)
        yield start, " ".join(parts)
        start, parts = None, []
    if parts:
        yield start, " ".join(parts)


def docker_command_findings(line):
    """Yield the rule broken by a `docker run` / `docker pull` command line: an untagged image, or an option this check cannot parse."""
    text = line.replace("`", " ")
    if not DOCKER_COMMAND_RE.match(text):
        return
    try:
        words = shlex.split(text)
    except ValueError:
        words = text.split()
    after_subcommand = words.index("docker") + 2
    rest = iter(words[after_subcommand:])
    for word in rest:
        if word in VALUE_OPTIONS:
            next(rest, None)
        elif word in FLAG_OPTIONS or (word.startswith("--") and "=" in word):
            continue
        elif word.startswith("-"):
            yield "unparsed-docker-option"
            return
        else:
            if not pinned(word):
                yield "untagged-image"
            return


def split_image_findings(lines):
    """Flag a YAML `image:` block (Helm style) that names a repository with the tag `latest`, or without a non-empty tag or digest."""
    for index, line in enumerate(lines):
        match = SPLIT_IMAGE_RE.match(line)
        if not match:
            continue
        indent, values = len(match.group(1)), {}
        following = index + 1
        for child in lines[following:]:
            if not child.strip() or child.lstrip().startswith("#"):
                continue
            key = YAML_KEY_RE.match(child)
            if not key or len(key.group(1)) <= indent:
                break
            raw = key.group(3).split(" #", 1)[0].strip()
            values[key.group(2)] = "" if raw in YAML_NULLS else raw.strip("\"'")
        if "repository" not in values:
            continue
        if values.get("tag", "").lower() == "latest":
            yield index + 1, "pull-latest"
        elif not (values.get("tag") or values.get("digest")):
            yield index + 1, "untagged-image"


def findings(text):
    """Yield (line_number, rule) for every scanner-flagged pattern in text."""
    lines = text.splitlines()
    for number, line in logical_lines(lines):
        for rule, pattern in RULES:
            if pattern.search(line):
                yield number, rule
        image = IMAGE_LINE_RE.search(line)
        if image and not pinned(image.group(1)):
            yield number, "untagged-image"
        for rule in docker_command_findings(line):
            yield number, rule
    yield from split_image_findings(lines)


def main():
    errors = 0
    for path in sorted((ROOT / "skills").rglob("*.md")):
        for number, rule in findings(path.read_text(encoding="utf-8")):
            print(f"FAIL {path.relative_to(ROOT)}:{number}: {rule}", file=sys.stderr)
            errors += 1
    if errors:
        return 1
    print("OK no scan-hygiene findings in skills/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
