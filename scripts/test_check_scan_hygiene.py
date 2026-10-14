"""Run: python3 scripts/test_check_scan_hygiene.py"""

from check_scan_hygiene import findings


def rules(text):
    return [rule for _, rule in findings(text)]


def test_latest_tag_is_flagged():
    assert rules("    image: bunkerity/bunkerweb:latest") == ["pull-latest"]


def test_untagged_compose_image_is_flagged():
    assert rules("    image: bunkerity/bunkerweb") == ["untagged-image"]


def test_untagged_third_party_image_is_flagged():
    assert rules("    image: nginx") == ["untagged-image"]


def test_pinned_compose_image_passes():
    assert rules('    image: "bunkerity/bunkerweb:1.6.15"') == []


def test_digest_pinned_image_passes():
    assert rules("    image: bunkerity/bunkerweb@sha256:0123abcd") == []


def test_helm_split_image_passes():
    assert rules("image:\n  repository: bunkerity/bunkerweb\n  tag: 1.6.15") == []


def test_helm_split_image_without_tag_is_flagged():
    assert list(findings("image:\n  repository: bunkerity/bunkerweb\n  pullPolicy: IfNotPresent")) == [(1, "untagged-image")]


def test_helm_split_image_with_empty_tag_is_flagged():
    assert rules('image:\n  repository: bunkerity/bunkerweb\n  tag: ""') == ["untagged-image"]
    assert rules("image:\n  repository: bunkerity/bunkerweb\n  tag:") == ["untagged-image"]


def test_helm_split_image_with_null_tag_is_flagged():
    for null in ("null", "Null", "NULL", "~"):
        assert rules(f"image:\n  repository: bunkerity/bunkerweb\n  tag: {null}") == ["untagged-image"], null
    assert rules("image:\n  repository: bunkerity/bunkerweb\n  digest: ~") == ["untagged-image"]


def test_helm_split_image_with_quoted_null_tag_passes():
    assert rules('image:\n  repository: bunkerity/bunkerweb\n  tag: "null"') == []


def test_helm_split_image_with_latest_tag_is_flagged():
    for tag in ("latest", '"latest"', "'Latest'"):
        assert list(findings(f"image:\n  repository: bunkerity/bunkerweb\n  tag: {tag}")) == [(1, "pull-latest")], tag


def test_helm_split_image_with_pinned_tag_passes():
    assert rules('image:\n  repository: bunkerity/bunkerweb\n  tag: "1.6.15"') == []


def test_helm_split_image_with_comments_passes():
    assert rules("image:  # BunkerWeb\n  repository: bunkerity/bunkerweb\n  # pinned for 1.6\n  tag: 1.6.15  # stable") == []


def test_untagged_docker_run_is_flagged():
    assert rules("docker run -d -p 80:8080 bunkerity/bunkerweb-all-in-one") == ["untagged-image"]


def test_untagged_third_party_docker_run_is_flagged():
    assert rules("$ docker run -d --name web nginx") == ["untagged-image"]


def test_untagged_docker_pull_is_flagged():
    assert rules("sudo docker pull redis") == ["untagged-image"]


def test_pinned_docker_commands_pass():
    assert rules("docker run -d -p 80:8080 -e TZ=UTC bunkerity/bunkerweb-all-in-one:1.6.15") == []
    assert rules("docker pull redis:7.4") == []


def test_health_cmd_value_is_not_taken_for_the_image():
    assert rules('docker run --health-cmd "curl http://localhost:8080" nginx') == ["untagged-image"]


def test_unknown_docker_option_is_reported():
    assert rules("docker run --some-new-flag nginx:1.27") == ["unparsed-docker-option"]


def test_inline_option_values_and_flags_parse():
    assert rules("docker run -it --rm --name=web bunkerity/bunkerweb-all-in-one:1.6.15") == []


def test_continued_docker_run_reports_first_line():
    assert list(findings("docker run -d \\\n  -p 80:8080 \\\n  bunkerity/bunkerweb-all-in-one")) == [(1, "untagged-image")]


def test_prose_mentioning_docker_pull_passes():
    assert rules("Don't let the agent run docker pull without a tag.") == []


def test_pipe_to_shell_is_flagged():
    assert rules("curl -fsSL https://example.com/install | sudo bash") == ["pipe-to-shell"]


def test_verification_curl_passes():
    assert rules("curl -s -o /dev/null -w '%{http_code}' https://app.example.com") == []


def test_clone_and_wget_are_flagged():
    assert rules("git clone https://github.com/coreruleset/coreruleset") == ["runtime-clone"]
    assert rules("wget https://example.com/rules.tar.gz") == ["runtime-download"]


def test_github_link_passes():
    assert rules("See https://github.com/bunkerity/bunkerweb for the source.") == []


def test_line_numbers_are_one_based():
    assert list(findings("ok\n    image: nginx")) == [(2, "untagged-image")]


if __name__ == "__main__":
    for name, test in sorted(globals().items()):
        if name.startswith("test_"):
            test()
    print("OK")
