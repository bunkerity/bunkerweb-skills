#!/usr/bin/env python3
"""Validate the skills in this repo. Run: python3 scripts/validate.py"""

import json
import re
import sys
from itertools import zip_longest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
MIGRATE_START = "<!-- migrate-process:start -->"
MIGRATE_END = "<!-- migrate-process:end -->"


def frontmatter(text):
    """Parse the simple `key: value` frontmatter a SKILL.md uses. No YAML dep."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def check_skill(directory, fail):
    skill_md = directory / "SKILL.md"
    if not skill_md.is_file():
        return fail(f"{directory.name}: missing SKILL.md")

    fields = frontmatter(skill_md.read_text(encoding="utf-8"))
    if fields is None:
        return fail(f"{directory.name}: SKILL.md has no `---` frontmatter block")

    name = fields.get("name", "")
    if name != directory.name:
        fail(f"{directory.name}: frontmatter name is {name!r}, must match the directory name")
    if not NAME_RE.match(directory.name):
        fail(f"{directory.name}: directory name must be lowercase-kebab-case")

    description = fields.get("description", "")
    if not description:
        fail(f"{directory.name}: frontmatter needs a `description` (this is what makes the skill discoverable)")
    elif len(description) > 1024:
        fail(f"{directory.name}: description is {len(description)} chars, keep it under 1024")


def migrate_block(skill_md, fail):
    """Return the text between the migrate-process markers of one SKILL.md, or None after reporting a marker error."""
    name = f"{skill_md.parent.name}/SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    starts, ends = text.count(MIGRATE_START), text.count(MIGRATE_END)
    if starts != 1 or ends != 1:
        fail(f"{name}: needs exactly one {MIGRATE_START} marker and one {MIGRATE_END} marker, found {starts} start and {ends} end")
        return None
    if text.index(MIGRATE_START) > text.index(MIGRATE_END):
        fail(f"{name}: the {MIGRATE_END} marker comes before the {MIGRATE_START} marker")
        return None
    block = text.split(MIGRATE_START, 1)[1].split(MIGRATE_END, 1)[0]
    return block[1:] if block.startswith("\n") else block


def check_migrate_blocks(skills_dir, fail):
    """Every skills/bunkerweb-migrate*/SKILL.md carries the same shared block, so a skill installed alone stays complete."""
    blocks = {}
    for skill_md in sorted(skills_dir.glob("bunkerweb-migrate*/SKILL.md")):
        block = migrate_block(skill_md, fail)
        if block is not None:
            blocks[f"{skill_md.parent.name}/SKILL.md"] = block
    names = list(blocks)
    for name in names[1:]:
        if blocks[name] == blocks[names[0]]:
            continue
        pairs = zip_longest(blocks[names[0]].splitlines(), blocks[name].splitlines(), fillvalue="<end of block>")
        number, (first, second) = next((n, pair) for n, pair in enumerate(pairs, 1) if pair[0] != pair[1])
        return fail(f"migrate-process block differs between {names[0]} and {name} at line {number} of the block: {first!r} vs {second!r}")


def main():
    errors = []
    fail = errors.append

    for path in (
        ROOT / ".claude-plugin/marketplace.json",
        ROOT / ".claude-plugin/plugin.json",
    ):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            fail(f"{path.relative_to(ROOT)}: {e}")

    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    if not skills:
        fail("skills/ is empty")
    for skill in skills:
        check_skill(skill, fail)
    check_migrate_blocks(ROOT / "skills", fail)

    for error in errors:
        print(f"FAIL {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"OK {len(skills)} skill(s): {', '.join(s.name for s in skills)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
