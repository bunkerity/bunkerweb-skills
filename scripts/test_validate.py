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


if __name__ == "__main__":
    for name, test in sorted(globals().items()):
        if name.startswith("test_"):
            test()
            print(f"ok {name}")
    print("OK")
