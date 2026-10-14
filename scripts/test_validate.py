"""Run: python3 -B scripts/test_validate.py

Runs a copy of validate.py against a throwaway skills tree, so the check is tested the way CI runs it.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VALIDATE = Path(__file__).resolve().parent / "validate.py"
START = "<!-- migrate-process:start -->"
END = "<!-- migrate-process:end -->"
BLOCK = "## The five steps\n\n1. Inventory.\n2. Map.\n3. Fallback.\n"


def skill(name, block=BLOCK, start=START, end=END):
    return f"---\nname: {name}\ndescription: test skill {name}\n---\n\n# {name}\n\nsource-specific text of {name}\n\n{start}\n{block}{end}\n"


def run(skills):
    """Return (exit code, stderr) of validate.py over a tree holding `skills` ({name: SKILL.md text})."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "scripts").mkdir()
        shutil.copy(VALIDATE, root / "scripts" / "validate.py")
        (root / ".claude-plugin").mkdir()
        (root / ".claude-plugin" / "marketplace.json").write_text("{}")
        (root / ".claude-plugin" / "plugin.json").write_text("{}")
        for name, text in skills.items():
            (root / "skills" / name).mkdir(parents=True)
            (root / "skills" / name / "SKILL.md").write_text(text)
        done = subprocess.run([sys.executable, "-B", str(root / "scripts" / "validate.py")], capture_output=True, text=True)
        return done.returncode, done.stderr


def test_identical_blocks_pass():
    code, err = run(
        {
            "bunkerweb-migrate": skill("bunkerweb-migrate"),
            "bunkerweb-migrate-nginx": skill("bunkerweb-migrate-nginx"),
            "bunkerweb": skill("bunkerweb", block="unrelated\n"),
        }
    )
    assert code == 0, err


def test_one_changed_character_fails_and_names_both_files_and_the_line():
    code, err = run(
        {"bunkerweb-migrate": skill("bunkerweb-migrate"), "bunkerweb-migrate-nginx": skill("bunkerweb-migrate-nginx", block=BLOCK.replace("Map.", "Mop."))}
    )
    assert code == 1, err
    assert "bunkerweb-migrate" in err and "bunkerweb-migrate-nginx" in err, err
    assert "line 4" in err and "Mop." in err, err


def test_missing_end_marker_fails():
    code, err = run({"bunkerweb-migrate": skill("bunkerweb-migrate"), "bunkerweb-migrate-nginx": skill("bunkerweb-migrate-nginx").replace(END, "")})
    assert code == 1, err
    assert "bunkerweb-migrate-nginx" in err and "marker" in err, err


def test_two_start_markers_fail():
    doubled = skill("bunkerweb-migrate-nginx").replace(START, START + "\n" + START)
    code, err = run({"bunkerweb-migrate": skill("bunkerweb-migrate"), "bunkerweb-migrate-nginx": doubled})
    assert code == 1, err
    assert "bunkerweb-migrate-nginx" in err and "marker" in err, err


def with_description(name, description):
    return skill(name).replace(f"description: test skill {name}", f"description: {description}")


def test_unquoted_colon_in_description_fails_and_names_skill_and_field():
    code, err = run({"bunkerweb-foo": with_description("bunkerweb-foo", "Use when X has no effect: use bar instead")})
    assert code == 1, err
    assert "bunkerweb-foo" in err and "description" in err and "strict YAML" in err, err


def test_unquoted_hash_comment_in_description_fails():
    code, err = run({"bunkerweb-foo": with_description("bunkerweb-foo", "Use when X is set #1 priority")})
    assert code == 1, err
    assert "bunkerweb-foo" in err and "description" in err and "comment" in err and "truncated" in err, err


def test_description_ending_in_colon_fails():
    code, err = run({"bunkerweb-foo": with_description("bunkerweb-foo", "Use when X:")})
    assert code == 1, err
    assert "bunkerweb-foo" in err and "description" in err and "strict YAML" in err, err


def test_colon_followed_by_tab_in_description_fails():
    code, err = run({"bunkerweb-foo": with_description("bunkerweb-foo", "Use when X:\tuse bar")})
    assert code == 1, err
    assert "bunkerweb-foo" in err and "description" in err and "strict YAML" in err, err


def test_flow_mapping_in_other_fields_passes():
    skill_md = skill("bunkerweb-foo").replace("---\n\n", "metadata: {author: Bunkerity}\n---\n\n", 1)
    assert "metadata: {author: Bunkerity}" in skill_md
    code, err = run({"bunkerweb-foo": skill_md})
    assert code == 0, err


def test_unclosed_double_quote_in_description_fails():
    code, err = run({"bunkerweb-foo": with_description("bunkerweb-foo", '"Use when X: y')})
    assert code == 1, err
    assert "bunkerweb-foo" in err and "description" in err and "does not close" in err and "strict YAML" in err, err


def test_unclosed_single_quote_in_description_fails():
    code, err = run({"bunkerweb-foo": with_description("bunkerweb-foo", "'Use when X: y")})
    assert code == 1, err
    assert "bunkerweb-foo" in err and "description" in err and "does not close" in err and "strict YAML" in err, err


def test_quoted_or_block_scalar_description_may_hold_colon_and_hash():
    for value in ('"Use when X: y #z"', "'Use when X: y #z'", ">\n  Use when X: y #z"):
        code, err = run({"bunkerweb-foo": with_description("bunkerweb-foo", value)})
        assert code == 0, (value, err)


if __name__ == "__main__":
    for name, test in sorted(globals().items()):
        if name.startswith("test_"):
            test()
            print(f"ok {name}")
    print("OK")
