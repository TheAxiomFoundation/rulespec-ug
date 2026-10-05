from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
JURISDICTION_DIR_RE = re.compile(r"^[a-z]{2}(-[a-z0-9-]+)*$")
CONTENT_DIRS = ("statutes", "regulations", "policies", "legislation")
IGNORED_DIRS = {".git", ".pytest_cache", ".ruff_cache", ".venv", "__pycache__"}
ALLOWED_ROOT_DIRS = {".axiom", ".github", "bulk", "data", "docs", "tests", "ug"}
ALLOWED_ROOT_FILES = {
    ".gitignore",
    "CLAUDE.md",
    "LICENSE",
    "LICENSE-CODE",
    "NOTICE",
    "README.md",
    "known-missing-money-atoms.yaml",
    "known-validation-gaps.yaml",
    "oracle-coverage-pending.yaml",
    "variables.toml",
}


def jurisdiction_dirs() -> list[Path]:
    return sorted(
        child
        for child in ROOT.iterdir()
        if child.is_dir()
        and JURISDICTION_DIR_RE.match(child.name)
        and any((child / marker).is_dir() for marker in CONTENT_DIRS)
    )


def rulespec_content_roots() -> list[Path]:
    return [
        jurisdiction / marker
        for jurisdiction in jurisdiction_dirs()
        for marker in CONTENT_DIRS
        if (jurisdiction / marker).is_dir()
    ]


def iter_rulespec_files() -> list[Path]:
    files: list[Path] = []
    for root in rulespec_content_roots():
        files.extend(
            path
            for path in root.rglob("*.yaml")
            if not path.name.endswith(".test.yaml")
        )
    return sorted(files)


def test_only_uganda_namespace_present() -> None:
    """Uganda is unitary: the only jurisdiction directory is ug/."""
    names = {d.name for d in jurisdiction_dirs()}
    assert names <= {"ug"}, f"unexpected jurisdiction dirs: {names - {'ug'}}"


def test_ug_content_buckets_exist() -> None:
    for marker in ("statutes", "regulations", "policies"):
        assert (ROOT / "ug" / marker).is_dir(), f"missing ug/{marker}"


def test_root_directories_are_allowed() -> None:
    # The org validate-rulespec workflow checks out sibling toolchain repos
    # (axiom-encode, axiom-rules-engine, ...) into a `_axiom/` directory and
    # skips any `_`- or `.`-prefixed directory during shard discovery. Mirror
    # that: ignore underscore/dot-prefixed dirs so CI's transient checkouts do
    # not trip the layout gate.
    found = {
        child.name
        for child in ROOT.iterdir()
        if child.is_dir()
        and child.name not in IGNORED_DIRS
        and not child.name.startswith(("_", "."))
    }
    unexpected = found - ALLOWED_ROOT_DIRS
    assert not unexpected, f"unexpected root directories: {unexpected}"


def test_root_files_are_allowed() -> None:
    # In a git worktree checkout `.git` is a gitdir-pointer file rather than
    # a directory, so exclude it here just as IGNORED_DIRS excludes the
    # `.git` directory in normal clones.
    found = {
        child.name
        for child in ROOT.iterdir()
        if child.is_file() and child.name != ".git"
    }
    unexpected = found - ALLOWED_ROOT_FILES
    assert not unexpected, f"unexpected root files: {unexpected}"


def test_every_rulespec_has_companion_test() -> None:
    """Any encoded rule module must ship a companion .test.yaml alongside it."""
    for path in iter_rulespec_files():
        companion = path.with_name(path.name[: -len(".yaml")] + ".test.yaml")
        assert companion.exists(), f"{path} is missing companion {companion.name}"


def test_money_atom_ratchet_is_nonnegative_int() -> None:
    payload = yaml.safe_load((ROOT / "known-missing-money-atoms.yaml").read_text())
    allowed = payload["total_allowed"]
    assert isinstance(allowed, int) and allowed >= 0


ORACLE_INDEX = ROOT / "data/oracles/oracle-index.json"
SOURCE_MAP = ROOT / "data/coverage/tax-benefit-source-map.json"
# A EUROMOD system name: country code, underscore, policy year (UG_2025).
SYSTEM_RE = re.compile(r"\b([A-Z]{2})_\d{4}\b")
# An Axiom output id as the suites record it: ug:<module path>#<rule name>.
OUTPUT_ID_RE = re.compile(
    r"^ug:(?P<path>[a-z0-9][a-z0-9/_.-]*)#(?P<name>[a-z][a-z0-9_]*)$"
)
# The other SOUTHMOD countries with rulespec repositories, by system prefix,
# with their model names and country names. None of them belongs in this
# repository's oracle data.
OTHER_SOUTHMOD_COUNTRIES = {
    "GH": ("ghamod", "ghana"),
    "ZM": ("microzamod", "zamod", "zambia"),
    "RW": ("rwamod", "rwanda"),
    "ET": ("etmod", "ethiopia"),
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ugamod_oracle() -> dict:
    oracles = load_json(ORACLE_INDEX)["oracles"]
    assert len(oracles) == 1, "expected exactly one oracle (UGAMOD)"
    return oracles[0]


def wired_suites() -> list[dict]:
    return ugamod_oracle()["wired"]["suites"]


def iter_strings(value: object, key: str = "") -> list[tuple[str, str]]:
    """Return (key, string) for every string value in a JSON tree."""
    if isinstance(value, str):
        return [(key, value)]
    if isinstance(value, dict):
        return [pair for k, v in value.items() for pair in iter_strings(v, k)]
    if isinstance(value, list):
        return [pair for item in value for pair in iter_strings(item, key)]
    return []


def rule_names(module: Path) -> set[str]:
    payload = yaml.safe_load(module.read_text(encoding="utf-8"))
    return {rule["name"] for rule in payload.get("rules", [])}


def encoded_modules() -> set[str]:
    """Non-test RuleSpec YAML under ug/, leaving out the ug/programs/ compose specs."""
    ug = ROOT / "ug"
    return {
        path.relative_to(ROOT).as_posix()
        for path in ug.rglob("*.yaml")
        if not path.name.endswith(".test.yaml")
        and path.relative_to(ug).parts[0] != "programs"
    }


def test_oracle_index_is_ug_scoped() -> None:
    payload = load_json(ORACLE_INDEX)
    assert payload["jurisdiction"] == "ug"
    oracle = ugamod_oracle()
    assert (oracle["id"], oracle["name"]) == ("ugamod", "UGAMOD")
    assert oracle["url"].startswith("https://www.wider.unu.edu/about/")
    assert "ugamod" in oracle["url"].lower()
    assert oracle["authority"] == "wired_per_case_parity"
    assert oracle["availability_check"]["status"] == "wired_per_case_parity"


def test_oracle_systems_dataset_and_suites_are_ugandan() -> None:
    oracle = ugamod_oracle()
    wired = oracle["wired"]
    system_texts = [wired["system"], oracle["systems"]] + [
        suite["system"] for suite in wired["suites"] if "system" in suite
    ]
    for text in system_texts:
        prefixes = set(SYSTEM_RE.findall(text))
        assert prefixes == {"UG"}, f"non-Uganda or missing system in {text!r}"
    assert wired["dataset_configuration"].startswith("ug_")
    names = [suite["suite"] for suite in wired["suites"]]
    assert len(names) == len(set(names)), "duplicate suite names"
    assert all(name.startswith("ug-") for name in names), names


def test_wired_counts_are_consistent() -> None:
    wired = ugamod_oracle()["wired"]
    for suite in wired["suites"]:
        name = suite["suite"]
        assert suite["matched"] + suite["dispositioned"] == suite["comparisons"], name
        assert len(suite["axiom_outputs"]) == len(suite["ugamod_variables"]), name
    totals = wired["totals"]
    assert totals["suites"] == len(wired["suites"])
    for key in ("cases", "comparisons", "matched", "dispositioned"):
        assert totals[key] == sum(suite[key] for suite in wired["suites"]), key


def test_wired_axiom_outputs_resolve_to_module_rules() -> None:
    for suite in wired_suites():
        for output in suite["axiom_outputs"]:
            match = OUTPUT_ID_RE.match(output)
            assert match, f"{suite['suite']}: malformed output id {output}"
            module = ROOT / "ug" / f"{match['path']}.yaml"
            assert module.is_file(), f"{output}: no module ug/{match['path']}.yaml"
            assert match["name"] in rule_names(module), (
                f"{output}: ug/{match['path']}.yaml defines no rule {match['name']}"
            )


def test_oracle_data_records_no_local_paths() -> None:
    # The single local_path field names where the licensed bundle sits; no
    # other text may carry a machine path.
    for path in (ORACLE_INDEX, SOURCE_MAP):
        for key, text in iter_strings(load_json(path)):
            if key == "local_path":
                continue
            assert "~/" not in text and "/Users/" not in text, (
                f"{path.name}: local path in {key}"
            )


def test_source_map_tracks_resolve() -> None:
    payload = load_json(SOURCE_MAP)
    assert payload["jurisdiction"] == "ug"
    suites = {suite["suite"] for suite in wired_suites()}
    ids = [track["id"] for track in payload["tracks"]]
    assert len(ids) == len(set(ids)), "duplicate track ids"
    for track in payload["tracks"]:
        assert track["namespace"] == "ug", track["id"]
        assert track["bucket"] in {"statutes", "regulations", "policies"}, track["id"]
        assert track["status"] in {"encoded", "planned"}, track["id"]
        modules = track.get("rulespec_modules", [])
        assert (track["status"] == "encoded") == bool(modules), track["id"]
        for module in modules:
            assert (ROOT / module).is_file(), f"{track['id']}: missing {module}"
        for suite in track.get("oracle_suites", []):
            assert suite in suites, f"{track['id']}: unknown suite {suite}"


def test_source_map_covers_every_encoded_module_and_suite() -> None:
    tracks = load_json(SOURCE_MAP)["tracks"]
    mapped = {
        module for track in tracks for module in track.get("rulespec_modules", [])
    }
    unmapped = encoded_modules() - mapped
    assert not unmapped, f"encoded modules with no source-map track: {sorted(unmapped)}"
    compared = {suite for track in tracks for suite in track.get("oracle_suites", [])}
    assert compared == {suite["suite"] for suite in wired_suites()}


def test_oracle_data_names_no_other_southmod_country() -> None:
    for path in (ORACLE_INDEX, SOURCE_MAP):
        text = path.read_text(encoding="utf-8")
        for code, names in OTHER_SOUTHMOD_COUNTRIES.items():
            assert not re.search(rf"\b{code}_\d{{4}}\b", text), (
                f"{path.name}: names a {code}_YYYY system"
            )
            for name in names:
                assert not re.search(rf"\b{name}\b", text, re.IGNORECASE), (
                    f"{path.name}: names {name}"
                )


def test_toolchain_pins_are_full_shas() -> None:
    import tomllib

    payload = tomllib.loads((ROOT / ".axiom/toolchain.toml").read_text())
    toolchain = payload["toolchain"]
    assert set(toolchain) == {
        "axiom_corpus_release",
        "axiom_corpus_release_content_sha256",
        "validation_waiver_set_sha256",
    }
    assert re.fullmatch(
        r"[a-z]{2}-rulespec-\d{4}-\d{2}-\d{2}", toolchain["axiom_corpus_release"]
    ), "release must be an immutable dated name"
    sha256_re = re.compile(r"^[0-9a-f]{64}$")
    assert sha256_re.match(toolchain["axiom_corpus_release_content_sha256"])
    assert sha256_re.match(toolchain["validation_waiver_set_sha256"])
