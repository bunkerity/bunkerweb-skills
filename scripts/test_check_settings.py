"""Run: python3 scripts/test_check_settings.py"""

import json
import tempfile
from pathlib import Path

from check_settings import known_settings, unknown_tokens

KNOWN = {"USE_ANTIBOT", "REVERSE_PROXY_HOST", "MULTISITE"}


def test_prefixed_setting_resolves():
    assert list(unknown_tokens("www.example.com_USE_ANTIBOT=captcha", KNOWN)) == []


def test_prefixed_typo_is_reported():
    assert list(unknown_tokens("www.example.com_USE_ANTIBOTS=captcha", KNOWN)) == [(1, "USE_ANTIBOTS")]


def test_numbered_suffix_resolves():
    assert list(unknown_tokens("REVERSE_PROXY_HOST_2=http://app:8080", KNOWN)) == []


def test_typo_is_reported_with_line():
    assert list(unknown_tokens("intro\nset `USE_ANTIBOTS=yes`", KNOWN)) == [(2, "USE_ANTIBOTS")]


def test_words_without_underscore_are_ignored():
    assert list(unknown_tokens("Send GET or POST over HTTP to MULTISITE", KNOWN)) == []


def test_label_and_annotation_forms_resolve():
    assert list(unknown_tokens("bunkerweb.USE_ANTIBOT=captcha\nbunkerweb.io/USE_ANTIBOT: captcha", KNOWN)) == []


def test_known_settings_reads_global_and_plugin_files():
    with tempfile.TemporaryDirectory() as tmp:
        common = Path(tmp) / "src/common"
        (common / "core/antibot").mkdir(parents=True)
        (common / "settings.json").write_text(json.dumps({"MULTISITE": {}}))
        (common / "core/antibot/plugin.json").write_text(json.dumps({"settings": {"USE_ANTIBOT": {}}}))
        assert known_settings(tmp) == {"MULTISITE", "USE_ANTIBOT"}


if __name__ == "__main__":
    for name, test in sorted(globals().items()):
        if name.startswith("test_"):
            test()
    print("OK")
