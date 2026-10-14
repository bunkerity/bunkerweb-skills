#!/usr/bin/env python3
"""Fail when a skill names a BunkerWeb setting that does not exist at the pinned release.

Run: python3 scripts/check_settings.py --bunkerweb /path/to/extracted/bunkerweb
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# UPPER_SNAKE with at least one underscore, not glued to a preceding capital or digit,
# so `www.example.com_USE_ANTIBOT` and `bunkerweb.io/USE_ANTIBOT` both yield `USE_ANTIBOT`.
TOKEN_RE = re.compile(r"(?<![A-Z0-9])[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+")
NUMBERED_RE = re.compile(r"_\d+$")


def known_settings(bunkerweb):
    common = Path(bunkerweb) / "src/common"
    names = set(json.loads((common / "settings.json").read_text(encoding="utf-8")))
    for plugin in sorted((common / "core").glob("*/plugin.json")):
        names |= set(json.loads(plugin.read_text(encoding="utf-8")).get("settings", {}))
    return names


def allowlist():
    names = set()
    for path in sorted((ROOT / "scripts/non-settings").glob("*.txt")):
        for line in path.read_text(encoding="utf-8").splitlines():
            token = line.split("#", 1)[0].strip()
            if token:
                names.add(token)
    return names


def unknown_tokens(text, known):
    """Yield (line_number, token) for every UPPER_SNAKE token that is neither known nor a numbered known setting."""
    for number, line in enumerate(text.splitlines(), 1):
        for token in TOKEN_RE.findall(line):
            if token not in known and NUMBERED_RE.sub("", token) not in known:
                yield number, token


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bunkerweb", required=True, help="directory holding src/common of the BunkerWeb release in BUNKERWEB_REF")
    args = parser.parse_args(argv)
    known = known_settings(args.bunkerweb) | allowlist()
    errors = 0
    for path in sorted((ROOT / "skills").rglob("*.md")):
        for number, token in unknown_tokens(path.read_text(encoding="utf-8"), known):
            print(f"FAIL {path.relative_to(ROOT)}:{number}: unknown setting {token}", file=sys.stderr)
            errors += 1
    if errors:
        return 1
    print("OK every UPPER_SNAKE token is a known setting or allowlisted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
